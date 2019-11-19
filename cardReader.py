#############################
# Vision component for Whist AI
# Asher Gingerich
#############################
#Debugging Modules
# from matplotlib import pyplot as plt
import pyqrcode

#Standard Modules
import numpy as np
import cv2 as cv
from pyzbar import pyzbar as qr

def cameraInit():
    print("Begin opening camera")
    cap = cv.VideoCapture(0)
    if cap.isOpened():
        print("Successfully opened camera")
    else:
        print("Did not open camera")
        return -1
    # cap.set(3, 720) #set width
    # cap.set(4, 720) #set height
    focus = 0.0
    cap.set(28, focus)# Set Focus
    return cap

# Generate a QR code based on content provided
def genQR(content, location):
    generated_qr = pyqrcode.create(content)
    generated_qr.png(location, scale=6)


def qr_read(image):
    code = qr.decode(image)
    known_strings = []
    if len(code) > 0:
        for found in code:
            datum = str(found.data)[2:-1]
            known_strings.append(datum)
    return known_strings

def variance_of_laplacian(frame):
    """
    Compute the Laplacian of the image. Used to determine blur level of an image
    Taken from https://github.com/geaxgx/playing-card-detection/blob/master/creating_playing_cards_dataset.ipynb
    frame: OpenCV Mat object
    """
    return cv.Laplacian(frame, cv.CV_64F).var()

def extract_card(frame, output_fn=None, min_focus=120, debug=False):
    """
    Extract a card from a given image frame
    Taken from https://github.com/geaxgx/playing-card-detection/blob/master/creating_playing_cards_dataset.ipynb
    Modified for my own use
    """
    # Global Variables
    #region
    ZOOM=4
    cardW = int(57 * ZOOM)
    cardH = int(87 * ZOOM)
    cornerXmin = int(2 * ZOOM)
    cornerXmax = int(10.5 * ZOOM)
    cornerYmin = int(2.5 * ZOOM)
    cornerYmax = int(23 * ZOOM)

    refCard=np.array([[0,0],[cardW,0],[cardW,cardH],[0,cardH]],dtype=np.float32)
    refCardRot=np.array([[cardW,0],[cardW,cardH],[0,cardH],[0,0]],dtype=np.float32)
    refCornerHL=np.array([[cornerXmin,cornerYmin],[cornerXmax,cornerYmin],[cornerXmax,cornerYmax],[cornerXmin,cornerYmax]],dtype=np.float32)
    refCornerLR=np.array([[cardW-cornerXmax,cardH-cornerYmax],[cardW-cornerXmin,cardH-cornerYmax],[cardW-cornerXmin,cardH-cornerYmin],[cardW-cornerXmax,cardH-cornerYmin]],dtype=np.float32)
    refCorners=np.array([refCornerHL,refCornerLR])

    bord_size=2
    alphamask=np.ones((cardH,cardW),dtype=np.uint8)*255
    cv.rectangle(alphamask,(0,0),(cardW-1,cardH-1),0,bord_size)
    cv.line(alphamask,(bord_size*3,0),(0,bord_size*3),0,bord_size)
    cv.line(alphamask,(cardW-bord_size*3,0),(cardW,bord_size*3),0,bord_size)
    cv.line(alphamask,(0,cardH-bord_size*3),(bord_size*3,cardH),0,bord_size)
    cv.line(alphamask,(cardW-bord_size*3,cardH),(cardW,cardH-bord_size*3),0,bord_size)
    if debug: cv.imshow("alphamask", alphamask)
    #endregion

    imgwarp=None
    # Check if the image is too blurry
    focus = variance_of_laplacian(frame)
    if focus < min_focus:
        if debug: print("Focus too low:", focus)
        return False, None
    # Grayscale transform
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Noise reducing and edge preserving filter
    gray = cv.bilateralFilter(gray, 11, 17, 17)
    # Gaussian filter
    gray = cv.GaussianBlur(gray, (3, 3), 0)
    if debug: cv.imshow("Grayscale - smoothed", gray)

    # Edge detection
    edges = cv.Canny(gray, 30, 200)
    se = np.ones((3, 3), dtype='uint8')
    # Close any gaps that may have formed during edge detection
    # edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, se)
    if debug: cv.imshow("Edges", edges)
    # Find contours
    cnts,_ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # We suppose that the contour with largest area corresponds to the contour delimiting the card
    cnt = sorted(cnts, key=cv.contourArea, reverse=True)[0]
    if debug:
        contoured = frame.copy()
        cv.drawContours(contoured, [cnt], -1, (0, 0, 255), -1)
        cv.imshow("Contours", contoured)
    # Create an image mask based on the detected cards to pull out their information later
    mask = np.zeros(frame.shape[:2], np.uint8)
    cv.drawContours(mask, [cnt], -1, 255, -1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, se)
    if debug: cv.imshow("Mask", mask)
    # Make a NEW contour set from the mask
    cnts,_ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Check for rectangle shape
    # TODO: Find out if this is actually necessary for our system.
    rect = cv.minAreaRect(cnts[0])
    box = cv.boxPoints(rect)
    box = np.int0(box)
    areaCnt = cv.contourArea(cnt)
    areaBox = cv.contourArea(box)
    valid = areaCnt/areaBox > 0.95
    if debug: print("Valid:", valid)

    if valid:
        ((xr, yr), (wr, hr), thetar) = rect
        #Determine transform matrix to turn image into reference rectangle
        if wr>hr:
            Mp = cv.getPerspectiveTransform(np.float32(box), refCard)
        else:
            Mp = cv.getPerspectiveTransform(np.float32(box), refCardRot)
        imgwarp = cv.warpPerspective(frame, Mp, (cardW, cardH))
        if debug: cv.imshow("Warped", imgwarp)
        # Add alpha channel to the image
        imgwarp = cv.cvtColor(imgwarp, cv.COLOR_BGR2BGRA)
        # Apply Mp to the contour
        cnta = cnt.reshape(1, -1, 2).astype(np.float32)
        cntwarp = cv.perspectiveTransform(cnta, Mp)
        cntwarp = cntwarp.astype(np.int)
        # Initialize transparency
        alphachannel = np.zeros(imgwarp.shape[:2], dtype=np.uint8)
        # Fill in contour to make opaque zone of card
        cv.drawContours(alphachannel, cntwarp, 0, 255, -1)

        # Apply the alphamask onto the alpha channel to clean it
        alphachannel = cv.bitwise_and(alphachannel, alphamask)

        # Add the alphachannel to the warped image
        imgwarp[:, :, 3] = alphachannel

        if debug: cv.imshow("Final image", imgwarp)
        if output_fn is not None:
            cv.imwrite(output_fn, imgwarp)

    k=-1
    if debug:
        cv.drawContours(frame, [box], -1, (0, 0, 0), 2)
        cv.imshow("Frame", frame)
        while(k!=27):
            k = cv.waitKey(5) & 0xFF
    return valid, imgwarp

# Retrieve individual frames from a video input
def video(cap):
    print("Beginning scan")
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        found_codes = qr_read(frame)
        if(found_codes):
            break

        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the resulting frame
    # plt.imshow(frame), plt.show()
    # print(found_codes)
    return found_codes


def findQR(frame):
    found_codes = qr_read(frame)
    return found_codes

def card_detection(frame):
    """
    Find the cards present within the given image frame
    frame: OpenCV Mat object
    """
    cards_found = findQR(frame)
    # Blur the image
    gauss = cv.GaussianBlur(frame, (3,3), 0)
    # Edge Detection
    edges = cv.Canny(gauss, 100, 300)
    se = np.ones((5, 5), dtype='uint8')
    # Close any gaps that may have formed during edge detection
    image_close = cv.morphologyEx(edges, cv.MORPH_CLOSE, se)
    image_close = edges
    # From the edges detected, create an image heierarchy of contours
    contours, _ = cv.findContours(image_close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #TODO: Filter out unwanted contours (countourArea?)
    #TODO: Approximate the contours using approxPolyDP
    approxContours = []
    for cnt in contours:
        perimeter = cv.arcLength(cnt, True)
        epsilon = 0.002*perimeter
        approxCnt = cv.approxPolyDP(cnt, epsilon, True)
        approxContours.append(approxCnt)
    print(approxContours)
    # contours = approxContours
    #TODO: Fit lines to these points, get 4 biggest lines
    #TODO: Find the intersection
    #TODO: Perspective transformation (getPerspectiveTransform, warpPerspective)
    # Create an image mask based on the detected cards to pull out their information later
    mask = np.zeros(frame.shape[:2], np.uint8)
    cv.drawContours(mask, contours, -1, 255, -1)
    cv.imshow("Mask", mask)
    image_mask = cv.bitwise_and(frame,frame, mask=mask)
    # Draw the contours onto the image itself for reference
    # cv.drawContours(frame, contours, -1, (0,0,255), 1)
    #Iterate through the contours detected
    for cnt in contours:
        rect = np.int0(cv.boxPoints(cv.minAreaRect(cnt)))
        print(rect)
        cv.drawContours(frame, [rect], -1, (0,0,0),2)
    # Show the image
    cv.imshow("Frame", frame)
    cv.imshow("Masked image", image_mask)
    return cards_found

def obtainCards(cap, useQR=True):
    print("BEGIN CARD DETECTION")
    cards_found = []
    if useQR:
        cards_found = video(cap)
    else:
        cards_found = card_detection(cap)
    cap.release()
    return cards_found

def videoHost():
    cap = cameraInit()
    if cap == -1:
        return -1
    print(cap.get(18))
    k=-1
    while(k!=27):
        ret, frame = cap.read()
        k = cv.waitKey(5) & 0xFF
        card_detection(frame)
        cv.imshow('frame', frame)
    #Close out the display window.
    cv.destroyAllWindows()

def generateCardFiles():
    image = cv.imread("images/playingCardImages/*.png")
    print(image)

def testingHost():
    print("Begin")
    image = cv.imread("images/playingCardImages/IMG_0108.jpg")
    # cv.imshow("Image", image)
    valid, imgwarp = extract_card(image, output_fn="images/testOutput.png", debug=True)   
    cv.destroyAllWindows()

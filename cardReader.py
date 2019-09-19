#############################
# Vision component for Whist AI
# Asher Gingerich
#############################
#Debugging Modules
from matplotlib import pyplot as plt
import pyqrcode

#Standard Modules
import numpy as np
import cv2 as cv
from pyzbar import pyzbar as qr

# Generate a QR code based on content provided
def genQR(content, location):
    generated_qr = pyqrcode.create(content)
    generated_qr.png(location, scale=2)


def qr_read(image):
    code = qr.decode(image)
    known_strings = []
    if len(code) > 0:
        for found in code:
            datum = str(found.data)[2:-1]
            known_strings.append(datum)
    return known_strings


# Retrieve individual frames from a video input
def video():
    cap = cv.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    if cap.isOpened():
        print("Successfully opened camera")
        print(cap.get(3))
    else:
        print("Did not open camera")
        return -1

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
    cap.release()
    return found_codes


def pollVideo():
    cap = cv.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)
    if cap.isOpened():
        print("Successfully opened camera")
    else:
        print("Did not open camera")
        return -1
    
    ret, frame = cap.read()
    print(ret)
    found_codes = qr_read(frame)
    cap.release()
    return found_codes


def main():
    img = cv.imread('images/testQR.png', 0)

    # Initiate ORB detector
    orb = cv.ORB_create()
    # find the keypoints with ORB
    keys = orb.detect(img, None)
    # compute the descriptors with ORB
    keys, des = orb.compute(img, keys)
    # draw only keypoints location,not size and orientation
    img2 = cv.drawKeypoints(img, keys, None, color=(0, 255, 0), flags=0)
    plt.imshow(img2), plt.show()

print(pollVideo())

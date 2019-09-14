# --------------------------------------
# Project:  Whist AI Project
# Author1:  Stephen Boxerman
# Author2:  Asher Gingerich
# --------------------------------------

import random
import os
import Player

players = [[],[],[],[]]
GOAL_POINTS = 1
POSSIBLE_BIDS = {'p': -1, '1': 1, '1no': 2, '2': 3, '2no': 4, '3': 5, '3no': 6, '4': 7, '4no': 8, '5': 9, '5no': 10,
                 '6': 11, '6no': 12, '7': 13, '7no': 14}
CARD_VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 't':10, 'J':11, 'Q':12, 'K': 13, 'A':14}

player_suits = [{'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0},
                {'h':0, 'd':0, 's':0, 'c':0}]

# a helper function to find the next player
def next_player(player):
    return (player + 1) % 4

def is_legal(card, suit):
    return card[0] == suit


# a helper function to remove the files we created
# to hold the persons hand information
def remove_files():
    for i in range(4):
        fn = 'player' + str(i) + '.txt'
        if os.path.exists(fn):
            os.remove(fn)

# a helper function to retrieve the suit of a card
def get_card_suit(card):
    suit = card[0]
    return suit

# a function to create a deck of 52 cards
def create_deck():
    deck = []
    suits = ['h','d','s','c']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 't', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for value in values:
            card = suit + str(value)
            deck.append(card)
    return deck

# a function to deal out the cards;
# 13 per player, one at a time
def deal(deck, dealer):
    player_suits = [{'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0},
                {'h':0, 'd':0, 's':0, 'c':0}]

    #shuffle the deck
    random.shuffle(deck)

    #deals to the player to the left of the dealer first
    currentPlayer = next_player(dealer)

    #main body of the function
    while len(deck) != 0:
        card = deck.pop()
        players[currentPlayer].append(card)
        suit = get_card_suit(card)
        player_suits[currentPlayer][suit] += 1
        currentPlayer = next_player(currentPlayer)

# a recursive function to handle the bidding process
def bid(currentPlayer, dealer):

    #get the bid of the current player
    current_bid = input("player" + str(currentPlayer) + " bid: -> ")

    # logic to handle a faulty bid
    if current_bid not in POSSIBLE_BIDS:
        raise Exception("Incorrect Bid")
    #base case
    elif currentPlayer == dealer:
        return [current_bid]
    #recusive case
    else:
        status = bid(next_player(currentPlayer), dealer)
        build = [current_bid]
        build.extend(status)
        return build

# a function that handles the setup of a round of Whist
def setup(dealer):
    # keeps looping till at least one player has made a bid other than pass
    while True:
        #create deck
        deck = create_deck()
        #deal cards
        deal(deck, dealer)
        #right out each players hand to a file
        for i in range(4):
            players[i].sort()
            fn = 'player' + str(i) + '.txt'
            file = open(fn, "x")
            file.write(str(players[i]))
            file.close()
        # set currentPlayer to the player on the dealer left
        currentPlayer = next_player(dealer)

        #loops through till all players have made a legal bid
        while True:
            try:
                bids = bid(currentPlayer, dealer)
                if (bids == ['p', 'p', 'p', 'p']):
                    print('All players passed.')
                    bids = bid(currentPlayer, dealer)
            except:
                #need function to handle an incorrect bid
                print("Incorrect Bid.  Please try again")
                continue
            break

        if bids != ['p', 'p', 'p', 'p']:
            return bids

# a function for finding the winning bid
def getWinningBid(bids, dealer):

    bidValues = [] #variable to hold the values of the bids that have been made (see POSSIBLE_BIDS for the bid values)
    for bid in bids:
        bidValues.append(POSSIBLE_BIDS.get(bid))
    winningBid = bidValues.index(max(bidValues))
    # set leading player to be the player that own the bid
    leadingPlayer = (winningBid + 1 + dealer) % 4

    # set the winning criteria for winning a trick
    if bidValues[winningBid] % 2 == 0:
        restriction = input("High or low? (asc or desc) -> ")
        while restriction not in ['asc', 'desc']:
            print('Invalid.  Must enter asc or desc.')
            restriction = input("High or low? (asc or desc) -> ")
    else:
        restriction = input("What's trump? (h, d, s, c) -> ")
        while restriction not in ['h', 'd', 's', 'c']:
            print('Invalid.  Must enter h, d, s, or c.')
            restriction = input("What's trump? (h, d, s, c) -> ")

    return leadingPlayer, restriction, winningBid

# function for a player to play a card
def play_card(player):
    card = ''
    while True:
        card = input('player' + str(player) + ' play a card. -> ')
        #logic to determin if the player has the card in hand
        if card not in players[player]:
            print("You do not have that card in hand. Please play a legal card.")
        else:
            return card

# helper function for determining if a suit is in a players hand
def has_suit(player, suit):
    return player_suits[player][suit] != 0

# helper function to remove a card from a players hand
def remove_card(player, card):
    card_index = players[player].index(card)
    players[player].pop(card_index)

#a function to find the number of of cards played that are of a given suit an thier values
def findSuit(played, suit, default = -1):
    card_values = []
    for card in played:
        if get_card_suit(card) == suit:
            value = CARD_VALUES[card[1]]
            card_values.append(value)
        else:
            card_values.append(default)

    return card_values

# a function for finding the winning card of a trick 
def findWinningCard(playedCards, restriction, leadSuit):

    if restriction == "desc":
        values = findSuit(playedCards, leadSuit, 30)
        winningCard = min(values)
    elif restriction == "asc":
        values = findSuit(playedCards, leadSuit)
        winningCard = max(values)
    else:
        values = findSuit(playedCards, restriction)
        if values == [-1, -1, -1, -1]:
            values = findSuit(playedCards, leadSuit)
            winningCard = max(values)

        winningCard = max(values)
    #return the index of the winning card to determin what player that card belonged to
    return values.index(winningCard)

# a function to exicute the game play for a single hand
def play(leadingPlayer, restriction):
    for i in range(13):
        tricks = [0, 0]
        playedCards = []

        card = play_card(leadingPlayer) # have the leading player play a card
        playedCards.append(card)
        leadSuit = get_card_suit(card) #set the suit that all other players must play if posable
        current_player = next_player(leadingPlayer) #set current player to the curent players left
        for i in range(3):
            card = play_card(current_player) #have a player play a card

	    # logic to determin if player has played a legal card
            while get_card_suit(card) != get_card_suit(playedCards[0]): 
                if has_suit(current_player, get_card_suit(playedCards[0])):
                    print('You must follow suit.')
                    card = play_card(current_player)
                else:
                    break

            playedCards.append(card)
            remove_card(current_player, card)
            current_player = next_player(current_player)

        winningCard = findWinningCard(playedCards, restriction, leadSuit)

        winningPlayer = (leadingPlayer + winningCard) % 4  #find who won the hand
        print("Player " + str(winningPlayer) + " won the trick.\n")

        tricks[winningPlayer % 2] += 1 #acumulate tricks for winning team
        leadingPlayer = winningPlayer

    return tricks


# a function that calculates the sore for both teams after a hand is finished
def calcScores(tricks, winningBid, leadingPlayer, restriction):

    leadingTeam = leadingPlayer % 2 # leadingTeam[0] = player0, player2 - Asher Gingerich
    nonLeadingTeam = (leadingTeam+1) % 2 # nonLeadingTeam = player1, player3
    
    # set the number of points that the team who won the bid must make to gain points, else the lose that many points
    trickGoal = int(winningBid[0])
    
    # takes into acount the book rule
    trickPotential = [tricks[0]-6,tricks[1]-6]

    points = [0, 0]

    #point calculation
    if trickPotential[leadingTeam] > trickGoal:
        points[leadingTeam] += trickPotential[leadingTeam]
	#NOTE: if the leadingTeam made thier bid, it is imposable for the other team to have made points
    else:
        points[leadingTeam] -= trickGoal
	#NOTE: If leadingTeam did NOT make thier bid, it is posable that the other team made points
        if trickPotential[nonLeadingTeam] > 0:
            points[nonLeadingTeam] += trickPotential[leadingTeam]

    # double points gained/lost if no trump
    if restriction in ["asc", "desc"]:
        points[leadingTeam] *= 2
    print(points)
    return points


def main(debug = False):
    #remove any files made by previous runs
    remove_files()

    #dealer is default as 0
    dealer = 0
    team1Score = 0
    team2Score = 0
    while True:

        bids = setup(dealer)# go through pre-play setup
	
        leadingPlayer, restriction, winningIndex = getWinningBid(bids, dealer)# determine leading player and index of winning bid

        winningBid = bids[winningIndex]

        tricks = play(leadingPlayer, restriction)

        points = calcScores(tricks, winningBid, leadingPlayer, restriction)# get points won by teams

        team1Score += points[0]
        team2Score += points[1]

        print("Team 1: " + str(team1Score) + "\nTeam2: " + str(team2Score))
	
	# logic for determining winner of the game
        if team1Score >= GOAL_POINTS or team2Score <= -GOAL_POINTS:
            print("Team 1 Won!!!")
            break

        if team2Score >= GOAL_POINTS or team1Score <= -GOAL_POINTS:
            print("Team 2 Won!!!")
            break

    remove_files() #remove files at end of game

main()

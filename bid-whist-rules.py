# --------------------------------------
# Project:  Whist AI Project
# Author1:  Stephen Boxerman
# Author2:  Asher Gingerich
# --------------------------------------

import math
import random
import numpy as np
import os

players = [[],[],[],[]]
GOAL_POINTS = 10
POSSIBLE_BIDS = {'p': -1, '1': 1, '1no': 2, '2': 3, '2no': 4, '3': 5, '3no': 6, '4': 7, '4no': 8, '5': 9, '5no': 10,
                 '6': 11, '6no': 12, '7': 13, '7no': 14}
CARD_VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 't':10, 'J':11, 'Q':12, 'K': 13, 'A':14}

player_suits = [{'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0},
                {'h':0, 'd':0, 's':0, 'c':0}]

# a helper function to find the next player
def next_player(player):
    return (player + 1) % 4

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


def getWinningBid(bids, dealer):

    bidValues = []
    for bid in bids:
        bidValues.append(POSSIBLE_BIDS.get(bid))
    winningBid = bidValues.index(max(bidValues))
    leadingPlayer = (winningBid + 1 + dealer) % 4
    if bidValues[winningBid] % 2 == 0:
        trump = False
        restriction = input("High or low? (asc or desc) -> ")
        while restriction not in ['asc', 'desc']:
            print('Invalid.  Must enter asc or desc.')
            restriction = input("High or low? (asc or desc) -> ")
    else:
        trump = True
        restriction = input("What's trump? (h, d, s, c) -> ")
        while restriction not in ['h', 'd', 's', 'c']:
            print('Invalid.  Must enter h, d, s, or c.')
            restriction = input("What's trump? (h, d, s, c) -> ")
    return leadingPlayer, restriction, winningBid


def play_card(player):
    card = ''
    while True:
        card = input('player' + str(player) + ' play a card. -> ')
        if card not in players[player]:
            print("You do not have that card in hand. Please play a legal card.")
        else:
            return card


def has_suit(player, suit):
    return player_suits[player][suit] != 0


def remove_card(player, card):
    card_index = players[player].index(card)
    players[player].pop(card_index)


def findSuit(played, suit, default = -1):
    card_values = []
    for card in played:
        if get_card_suit(card) == suit:
            value = CARD_VALUES[card[1]]
            card_values.append(value)
        else:
            card_values.append(default)

    return card_values


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

    return values.index(winningCard)


def play(leadingPlayer, restriction):
    for i in range(13):
        team1 = [0,2]
        team2 = [1,3]
        tricks = [0, 0]
        playedCards = []

        card = play_card(leadingPlayer)
        playedCards.append(card)
        leadSuit = get_card_suit(card)
        current_player = next_player(leadingPlayer)
        for i in range(3):
            card = play_card(current_player)
            while get_card_suit(card) != get_card_suit(playedCards[0]):
                if has_suit(current_player, get_card_suit(playedCards[0])):
                    print('You must follow suit.')
                    card = play_card(current_player)
                else:
                    break

            playedCards.append(card)
            remove_card(current_player, card)
            current_player = next_player(current_player)

        winningCard = findWinningCard(playedCards, restriction)

        winningPlayer = (leadingPlayer + winningCard) % 4

        tricks[winningPlayer % 2] += 1

    return tricks


def calcScores(tricks, winningBid, leadingPlayer, restriction):

    leadingTeam = leadingPlayer % 2 # leadingTeam[0] = player0, player2
    nonLeadingTeam = leadingTeam+1%2

    trickGoal = int(winningBid[0])

    trickPotential[tricks[0]-6,tricks[1]-6]

    points = [0, 0]

    if trickPotential[leadingTeam] > trickGoal:
        points[leadingTeam] += trickPotential[leadingTeam]
    else:
        points[leadingTeam] -= trickGoal
        if trickPotential[nonLeadingTeam] > 0:
            points[nonLeadingTeam] += trickPotential[leadingTeam]
    if restriction in ["asc", "desc"]:
        points[leadingTeam] *= 2
    return points


def main():
    remove_files()
    dealer = 0
    while True:

        bids = setup(dealer)
        leadingPlayer, restriction, winningIndex = getWinningBid(bids, dealer)
        winningBid = bids[winningIndex]
        tricks = play(leadingPlayer, restriction)
        points = calcScores(tricks, winningBid, leadingPlayer, restriction)
        team1Score += points[0]
        team2Score += points[1]

        if team1Score >= GOAL_POINTS or team2Score <= -GOAL_POINTS:
            print("Team 1 Won!!!")
            break

        if team2Score >= GOAL_POINTS or team1Score <= -GOAL_POINTS:
            print("Team 2 Won!!!")
            break

        remove_files()

main()

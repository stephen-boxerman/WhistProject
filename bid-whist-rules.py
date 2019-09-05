#--------------------------------------
#Project:  Whist AI Project
#Author1:  Stephen Boxerman
#Author2:  Asher Gingerich
#--------------------------------------

import math
import random
import numpy as np
import os

players = [[],[],[],[]]
POSSIBLE_BIDS = {'p': -1, '1': 1, '1no': 2, '2': 3, '2no': 4, '3': 5, '3no': 6, '4': 7, '4no': 8, '5': 9, '5no': 10,
                 '6': 11, '6no': 12, '7': 13, '7no': 14}
CARD_VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K': 13, 'A':14}

def next_player(player):
    return (player + 1) % 4

def remove_files():
    for i in range(4):
        fn = 'player' + str(i) + '.txt'
        if os.path.exists(fn):
            os.remove(fn)

def create_deck():
    deck = []
    suits = ['h','d','s','c']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    for suit in suits:
        for value in values:
            card = str(value) + suit
            deck.append(card)
    return deck

def deal(deck, dealer):
    random.shuffle(deck)
    
    currentPlayer = next_player(dealer)
    while len(deck) != 0:
        players[currentPlayer].append(deck.pop())
        currentPlayer = next_player(currentPlayer)

def bid(currentPlayer, dealer):

    current_bid = input("player" + str(currentPlayer) + " bid: -> ")
        
    if current_bid not in POSSIBLE_BIDS:
        raise Exception("Incorrect Bid")
    elif currentPlayer == dealer:
        return [current_bid]
    else:
        status = bid(next_player(currentPlayer), dealer)
        build = [current_bid]
        build.extend(status)
        return build

def setup(dealer):
    while True:
        deck = create_deck()
        deal(deck, dealer)
        for i in range(4):
            fn = 'player' + str(i) + '.txt'
            file = open(fn, "x")
            file.write(str(players[i]))
            file.close()

        currentPlayer = next_player(dealer)
        while True:
            try:
                bids = bid(currentPlayer, dealer)
                if (bids == ['p', 'p', 'p', 'p']):
                    print('All players passed.')
                    bids = bid(currentPlayer, dealer)
            except:
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
    else:
        trump = True
        restriction = input("What's trump? (h, d, s, c) -> ")
    return leadingPlayer, trump, restriction

def play_card(player):
    card = ''
    while True:
        card = input('player' + str(player) + ' play a card. -> ')
        if card not in players[player]:
            print("You do not have that card in hand. Please play a legal card.")
        else:
            card_index = players[player].index(card)
            return players[player].pop(card_index)

def get_card_suit(card):
    suit = card[-1]
    return suit

def play(leadingPlayer, trump, restriction):
    print(leadingPlayer, trump, restriction)
    for i in range(13):
        playedCards = []
        playedCards.append(play_card(leadingPlayer))

        current_player = next_player(leadingPlayer)
        for i in range(3):
            card = play_card(current_player)
            while get_card_suit(card) != get_card_suit(playedCards[0]):
                print('You must follow suit.')
                card = play_card(current_player)
            playedCards.append(card)
            current_player = next_player(current_player)
        print(playedCards)


def main():
    remove_files()
    dealer = 0
    while True:

        bids = setup(dealer)
        leadingPlayer, trump, restriction = getWinningBid(bids, dealer)
        play(leadingPlayer, trump, restriction)
        remove_files()

main()

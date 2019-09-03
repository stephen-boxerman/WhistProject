import math
import random
import numpy as np

players = [[],[],[],[]]

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
    
    currentPlayer = (dealer + 1)%4
    while len(deck) != 0:
        players[currentPlayer].append(deck.pop())
        currentPlayer = (currentPlayer + 1)%4

def bid():
    bids = []
    possible_bids = ['p', 1, '1no', 2, '2no', 3, '3no', 4, '4no',
                    5, '5no', 6, '6no', 7, '7no']
    for i in range(4):
        try:
            bid = input("player" + str(i) + "bid: ->")
        if bid not in possible_bids:
            raise Exception("Incorrect Bid")
        except:
            print("Incorrect Bid.  Please try again")
            bid = input("player" + str(i) + "bid: ->")

def main():
    deck = create_deck()
    deal(deck, 0)
    for i in range(4):
        fn = 'player' + str(i) + '.txt'
        file = open(fn, "x")
        file.write(str(players[i]))
        file.close()
    bid()
    #play()

main()

# --------------------------------------
# Project:  Whist AI Project
# Author1:  Stephen Boxerman
# Author2:  Asher Gingerich
# --------------------------------------

import random
import os
from Player import randomPlayer as RP
import function_map

players = []
GOAL_POINTS = 50
player_suits = [{'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0},
                {'h':0, 'd':0, 's':0, 'c':0}]
cards = []

def get_bid_key(search_val):
    for bid, value in function_map.POSSIBLE_BIDS.items():
        if value == search_val:
            return bid

def remove_files():
    for i in range(4):
        fn = 'player' + str(i) + '.txt'
        if os.path.exists(fn):
            os.remove(fn)

def create_deck():
    deck = []
    minmaxDeck = {}
    suits = ['h','d','s','c']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 't', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for value in values:
            card = suit + str(value)
            deck.append(card)
            minmaxDeck.add(card)
    return deck, minmaxDeck

def deal(deck, dealer):
    player_suits = [{'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0}, {'h':0, 'd':0, 's':0, 'c':0},
                {'h':0, 'd':0, 's':0, 'c':0}]

    random.shuffle(deck)

    currentPlayer = function_map.next_player(dealer)

    while len(deck) != 0:
        card = deck.pop()
        players[currentPlayer].hand.append(card)
        suit = function_map.get_card_suit(card)
        player_suits[currentPlayer][suit] += 1
        currentPlayer = function_map.next_player(currentPlayer)

def bid(currentPlayer, dealer):

    current_bid = players[currentPlayer].get_bid()
    current_bid = get_bid_key(current_bid)

    if current_bid not in function_map.POSSIBLE_BIDS:
        raise Exception("Incorrect Bid")

    elif currentPlayer == dealer:
        return [current_bid]

    else:
        status = bid(function_map.next_player(currentPlayer), dealer)
        build = [current_bid]
        build.extend(status)
        return build

def setup(dealer):

    while True:

        deck, minmaxDeck = create_deck()

        deal(deck, dealer)

        for i in range(4):
            players[i].hand.sort()

        currentPlayer = function_map.next_player(dealer)

        bids = bid(currentPlayer, dealer)
        if (bids == ['p', 'p', 'p', 'p']):
            print('All players passed.')
            bids = bid(currentPlayer, dealer)

        if bids != ['p', 'p', 'p', 'p']:
            return bids, minmaxDeck

def getWinningBid(bids, dealer):

    bidValues = []
    for bid in bids:
        bidValues.append(function_map.POSSIBLE_BIDS.get(bid))
    winningBid = bidValues.index(max(bidValues))

    leadingPlayer = (winningBid + 1 + dealer) % 4

    restriction = players[leadingPlayer].get_trump()

    return leadingPlayer, restriction, winningBid

def play_card(player):
    card = players[player].play()
    return card

def has_suit(player, suit):
    return player_suits[player][suit] != 0

def remove_card(player, card):
    card_index = players[player].hand.index(card)
    players[player].hand.pop(card_index)

def play(leadingPlayer, restriction, minmaxDeck):
    tricks = [0, 0]
    for i in range(13):
        winningData = [0,0,0,0]
        playedCards = []

        card = play_card(leadingPlayer)
        playedCards.append(card)
        leadSuit = function_map.get_card_suit(card)
        current_player = function_map.next_player(leadingPlayer)
        for i in range(3):
            card = play_card(current_player)

            while function_map.get_card_suit(card) != function_map.get_card_suit(playedCards[0]):
                if has_suit(current_player, function_map.get_card_suit(playedCards[0])):
                    card = play_card(current_player)
                else:
                    break

            playedCards.append(card)
            remove_card(current_player, card)
            current_player = function_map.next_player(current_player)

        winningCard = function_map.findWinningCard(playedCards, restriction, leadSuit)

        winningPlayer = function_map.getWinningPlayer(leadingPlayer, winningCard)
        print("Player " + str(winningPlayer) + " won the trick.\n")
        tricks[winningPlayer % 2] += 1
        leadingPlayer = winningPlayer
        winningData[winningPlayer] = 1
        playedCards += winningData
        cards.append(playedCards)


    return tricks

def calcScores(tricks, winningBid, leadingPlayer, restriction):

    leadingTeam = leadingPlayer % 2 # leadingTeam[0] = player0, player2 - Asher Gingerich
    nonLeadingTeam = (leadingTeam+1) % 2 # nonLeadingTeam = player1, player3

    trickGoal = int(winningBid[0])

    trickPotential = [tricks[0]-6,tricks[1]-6]
    points = [0, 0]

    if trickPotential[leadingTeam] > trickGoal:
        points[leadingTeam] += trickPotential[leadingTeam]
    #NOTE: if the leadingTeam made thier bid, it is imposable for the other team to have made points
    else:
        points[leadingTeam] -= trickGoal
    #NOTE: If leadingTeam did NOT make thier bid, it is posable that the other team made points

    if trickPotential[nonLeadingTeam] > 0:
        points[nonLeadingTeam] += trickPotential[nonLeadingTeam]

    if restriction in ["asc", "desc"]:
        points[leadingTeam] *= 2
    print(points)
    return points


def main(debug = False, verbose = False):
    if verbose:
        print("\nBeginning new game...")
    remove_files()

    dealer = 0
    team1Score = 0
    team2Score = 0
    while True:
        for i in range(4):
            players.append(RP())
        if verbose:
            print("Dealing new hand...\nBidding...")
        bids, minmaxDeck = setup(dealer)

        leadingPlayer, restriction, winningIndex = getWinningBid(bids, dealer)

        winningBid = bids[winningIndex]
        if verbose:
            print("Beginning new hand...\n")
        tricks = play(leadingPlayer, restriction, minmaxDeck)
        for player in players:
            player.hand = []

        points = calcScores(tricks, winningBid, leadingPlayer, restriction)

        team1Score += points[0]
        team2Score += points[1]

        print("Team 1: " + str(team1Score) + "\nTeam2: " + str(team2Score) + "\n")

        if team1Score >= GOAL_POINTS or team2Score <= -GOAL_POINTS:
            print("Team 1 Won!!!\n")
            break

        if team2Score >= GOAL_POINTS or team1Score <= -GOAL_POINTS:
            print("Team 2 Won!!!\n")
            break

    remove_files()


def whist_tourny(numGames = 1):
    hand = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for item in hand:
        index = hand.index(item)
        hand.pop(index)
        hand.insert(index, item)
        print(item)



whist_tourny()


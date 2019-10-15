POSSIBLE_BIDS = {'p': 0, '1': 1, '1no': 2, '2': 3, '2no': 4, '3': 5, '3no': 6, '4': 7, '4no': 8, '5': 9, '5no': 10,
                 '6': 11, '6no': 12, '7': 13, '7no': 14}
CARD_VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 't':10, 'J':11, 'Q':12, 'K': 13, 'A':14}

def next_player(player):
    return (player + 1) % 4

def is_legal(card, suit):
    return card[0] == suit

def get_card_suit(card):
    suit = card[0]
    return suit

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
    elif restriction == "asc":
        values = findSuit(playedCards, leadSuit)
    else:
        values = findSuit(playedCards, restriction)
        if values == [-1, -1, -1, -1]:
            values = findSuit(playedCards, leadSuit)

    winningCard = max(values)
    #return the index of the winning card to determin what player that card belonged to
    return values.index(winningCard)

def getWinningPlayer(leadingPlayer, winningCard):
    winningPlayer = (leadingPlayer + winningCard) % 4
    return winningPlayer
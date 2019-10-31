import function_map
import random
import copy

class Minmax:
    def __init__(self, player, restriction = 'asc'):
        self.player = player
        self.restriction = restriction

    def suitInCards(self, suit, cards):
        numSuit = 0

        for card in cards:
            if card[0] == suit:
                numSuit += 1

        return numSuit

    def testTrick(self, state):
        if len(state['trick']) == 4:
            state['numTricks'] += 1
            #print("Number of Tricks -> " + str(state['numTricks']))
            winningCard = function_map.findWinningCard(state['trick'], self.restriction, function_map.get_card_suit(state['leadCard']))
            leadingPlayer = function_map.getWinningPlayer(state['leadingPlayer'], winningCard)
            state['player'] = leadingPlayer
            if leadingPlayer % 2 == 0:
                state['points'][0] += 1
            else:
                state['points'][1] += 1
            state['trick'] = []
            state['leadingPlayer'] = leadingPlayer
            state['leadCard'] = ''

    def isLegal(self, card, leadCard, cards, cardsPlayed):
        if leadCard == '':
            return True

        # elif len(cards) == 1:
        #     return True

        elif self.suitInCards(leadCard[0], cards) == 0:
            return True

        elif card not in cards:
            return False

        elif card in cardsPlayed:
            return False

        elif card[0] != leadCard[0]:
            return False

        else:
            return True

    def evalTricks(self, points):
        #print("Evaluating Tricks...")

        leadingTeam = self.player % 2

        score = points[leadingTeam]

        return score

    def minmax(self,alpha, beta, state):
        # print("Beginning minmax")

        state['player'] = function_map.next_player(state['player'])

        self.testTrick(state)

        #print('\n', 'Length of deck ->', len(state['deck']), 'Length of hand ->', len(state['hand']))
        if state['player'] % 2 == self.player % 2:
            isMax = True
        else:
            isMax = False

        if isMax:
            bestVal = -float('inf')
        else:
            bestVal = float('inf')

        if state['hands'] == [[],[],[],[]]:
            #print("End of branch")
            return self.evalTricks(state['points'])

        bestCard = ''
        cards = state['hands'][state['player']][:]
        hand = state['hands'][state['player']]

        if state['leadCard'] == '':
            card = cards[0]
            state['trick'].append(card)
            state['leadCard'] = card
            state['cardsPlayed'].append(card)
            hand.remove(card)
            # print('Points before recursion', state['points'])
            bestVal = self.minmax(alpha, beta, copy.deepcopy(state))

        else:
            for card in cards:

                index = cards.index(card)
                if self.isLegal(card, state['leadCard'], cards, state['cardsPlayed']):

                    state['cardsPlayed'].append(card)
                    state['trick'].append(card)
                    index = cards.index(card)
                    hand.remove(card)
                    # print('Points before recursion', state['points'])
                    value = self.minmax(alpha, beta, copy.deepcopy(state))
                    # print('Points after recursion', state['points'])

                    hand.insert(index, card)
                    state['trick'].remove(card)
                    state['cardsPlayed'].remove(card)

                    if isMax:
                        if value > beta:
                            bestVal = value
                            break
                        elif value > bestVal:
                            bestVal = value
                            alpha = value
                    else:
                        if value < alpha:
                            bestVal = value
                            break
                        elif value < bestVal:
                            bestVal = value
                            beta = value

        # print("Ending minmax", bestVal)
        return bestVal



    def getOptimalCard(self, state):

        alpha = -float('inf')
        beta = float('inf')
        playCard = ''

        cards = state['hands'][state['player']][:]
        hand = state['hands'][state['player']]

        for card in cards:
            if self.isLegal(card, state['leadCard'], cards, state['cardsPlayed']):
                if state['leadCard'] == '':
                    state['leadCard'] = card
                    state['trick'].append(state['leadCard'])
                    state['cardsPlayed'].append(card)
                else:

                    state['cardsPlayed'].append(card)
                    state['trick'].append(card)
                    index = hand.index(card)
                    hand.remove(card)
                    value = self.minmax(alpha, beta, copy.deepcopy(state))
                    #print('Value for owning plauer ->', value)
                    hand.insert(index, card)
                    state['trick'].remove(card)
                    state['cardsPlayed'].remove(card)

                if value > alpha:
                    alpha = value
                    playCard = card

                print('\n',"Value ->", value, '\n', "Card->", card)

        return playCard

def main():
    card = 'noCard'
    # deck = ['hJ', 'hQ', 'hK']
    # hand = ['hA']
    
    #deck = ['h4', 'h5', 'h6', 'h7', 'h9', 'hJ', 'hQ', 'hK']
    #hand = ['h2', 'hA', 'h3']

    # hands = [['s8', 'c2', 'cA'], ['c8', 's2', 'd8'], ['sA', 'h2', 'hA'], ['dA', 'h8']]
    # leadCard = 'd2'

    deck = []
    hands = [[], [], [], []]

    for suit in ['h', 's', 'd', 'c']:
        for value in ['2', '4', '5', '7', '8', 't', 'J', 'K', 'A']:
            card = suit + value
            deck.append(card)

    random.shuffle(deck)
    random.shuffle(deck)

    while len(deck) != 0:
        for hand in hands:
            card = deck.pop()
            hand.append(card)

    leadCard = hands[3].pop()
    print("My hand ->", hands[0], '\n', "Partners hand ->", hands[2], '\n', "Lead Card ->", leadCard, '\n')

    minmax = Minmax(0, 's')
    state = {'hands': hands[:], 'player': minmax.player, 'leadCard': leadCard,
             'leadingPlayer': 3, 'trick': [leadCard], 'points': [0, 0], 'numTricks': 0, 'cardsPlayed': []}
    card = minmax.getOptimalCard(state)
    print(card)

main()

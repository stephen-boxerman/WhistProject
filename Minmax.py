import function_map
import random
import copy

class Minmax:
    def __init__(self, hand, player, restriction = 'asc'):
        self.player = player
        self.hand = hand
        self.restriction = restriction
        self.cardsPlayed = []
        self.numBranches = 0

    def suitInCards(self, suit, cards):
        numSuit = 0

        for card in cards:
            if card[0] == suit:
                numSuit += 1

        return numSuit

    def testTrick(self, state):
        if len(state['trick']) == 4:
            state['numTricks'] += 1
            print("Number of Tricks -> " + str(state['numTricks']))
            winningCard = function_map.findWinningCard(state['trick'], self.restriction, function_map.get_card_suit(state['leadCard']))
            leadingPlayer = function_map.getWinningPlayer(state['leadingPlayer'], winningCard)
            state['player'] = leadingPlayer
            if leadingPlayer % 2 == 0:
                state['points'][0] += 1
            else:
                state['points'][1] += 1
            state['trick'] = []
            state['leadingPlayer'] = leadingPlayer

    def isLegal(self, card, leadCard, cards):
        if leadCard == '':
            return True

        elif self.suitInCards(leadCard[0], cards) == 0:
            return True

        elif card not in cards:
            return False

        elif card in self.cardsPlayed:
            return False

        elif card[0] != leadCard[0]:
            return False

        else:
            return True

    def evalTricks(self, points):
        print("Evaluating Tricks...")

        leadingTeam = self.player % 2

        score = points[leadingTeam]

        return score

    def setCards(self, hand, deck, isMax, player):
        if isMax and player == self.player:
            cards = hand
        else:
            cards = deck

        return cards

    # def isBranching(self, alpha, beta, value, isMax):
    #     if isMax and value < alpha

    def minmax(self,alpha, beta, isMax, state):
        # print("Beginning minmax")
        state['player'] = function_map.next_player(state['player'])

        self.testTrick(state)
        print('\n', 'Length of deck ->', len(state['deck']), 'Length of hand ->', len(state['hand']))
        if state['leadingPlayer'] % 2 == self.player % 2:
            isMax = True
        else:
            isMax = False

        if len(state['deck']) == 0 and len(state['hand']) == 0:
            print("End of branch")
            return self.evalTricks(state['points'])

        bestCard = ''
        bestVal = -float('inf')
        cards = self.setCards(state['hand'], state['deck'], isMax, state['player'])
        if state['leadCard'] == '':
            card = cards[0]
            state['trick'].append(card)
            self.cardsPlayed.append(card)
            index = cards.index(card)
            cards.remove(card)
            # print('Points before recursion', state['points'])
            bestVal = self.minmax(alpha, beta, not isMax, copy.deepcopy(state))

        else:
            for card in cards:

                cardVal = function_map.CARD_VALUES[card[1]]
                index = cards.index(card)
                if self.isLegal(card, state['leadCard'], cards):

                    self.cardsPlayed.append(card)
                    state['trick'].append(card)
                    index = cards.index(card)
                    cards.remove(card)
                    # print('Points before recursion', state['points'])
                    value = self.minmax(alpha, beta, not isMax, copy.deepcopy(state))
                    # print('Points after recursion', state['points'])

                    cards.insert(index, card)
                    state['trick'].remove(card)
                    self.cardsPlayed.remove(card)

                    if value > bestVal:
                        bestVal = value

        # print("Ending minmax", bestVal)
        return bestVal



    def getOptimalCard(self, deck, hand, leadCard, leadingPlayer):

        alpha = -float('inf')
        beta = float('inf')
        playCard = ''

        state = {'hand': hand[:], 'deck':deck[:], 'player':self.player, 'leadCard':leadCard,
                 'leadingPlayer':leadingPlayer, 'trick':[], 'points':[0,0], 'numTricks': 0}

        for card in state['hand']:
            if self.isLegal(card, state['leadCard'], state['hand']):
                if leadCard == '':
                    state['leadCard'] = card
                else:
                    state['trick'].append(state['leadCard'])

                    self.cardsPlayed.append(card)
                    state['trick'].append(card)
                    index = state['hand'].index(card)
                    state['hand'].remove(card)
                    value = self.minmax(alpha, beta, False, copy.deepcopy(state))
                    print('Value for owning plauer ->', value)
                    state['hand'].insert(index, card)
                    state['trick'].remove(card)
                    self.cardsPlayed.remove(card)

                if leadCard == '':
                    state['leadCard'] = ''

                if value > alpha:
                    alpha = value
                    playCard = card

        return playCard

def main():
    card = 'noCard'
    # deck = ['hJ', 'hQ', 'hK']
    # hand = ['hA']

    deck = ['h5','hJ','ht','h7', 'h9', 'h4', 'hQ', 'h3', 'hK']
    hand = ['hA', 'h6', 'h2']

    minmax = Minmax(hand, 0)
    card = minmax.getOptimalCard(deck, hand, 'h8', 3)
    print(card)

main()

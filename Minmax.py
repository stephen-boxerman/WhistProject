class Minmax:
    def __init__(self, hand, player):
        self.player = player
        self.hand = hand

    def isLegal(self, card, leadCard, deck):
        if card not in deck:
            return False

        if card[0] != leadCard[0]:
            return False

        return True

    def minmax(self, player, hand, isMax, deck, maxDepth, leadCard, restriction = 'none', trick = [],):
        '''
            if len(trick) == 4
                eval trick
                minmax()
            if maxDepth or deck is empty
                eval node
                return val

            if isMax
                for card in hand


            if isMax

        '''
        pass
import random

class Player():
    def __init__(self):
        self.hand = []
        self.bid = ''
        self.trump = ''

    def bid(self):
        return random.randint(0,15)


class randomPlayer(Player):
    def __init__(self):
        self.lastPlayedCard = -1

    def play(self, legalCard):
        if not legalCard:
            self.lastPlayedCard += 1
            return self.hand[lastPlayedCard]
	

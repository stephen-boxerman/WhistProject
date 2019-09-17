import random

class Player:
    def __init__(self):
        self.hand = []
        self.bid = ''
        self.trump = ''

    def get_bid(self):
        pass

    def play(self):
        pass

    def get_trump(self):
        pass

class randomPlayer(Player):
    def __init__(self):
        super().__init__()
        self.lastPlayedCard = -1


    def play(self):
        self.lastPlayedCard += 1
        if self.lastPlayedCard > len(self.hand) - 1:
            self.lastPlayedCard = 0

        return self.hand[self.lastPlayedCard]

    def get_bid(self):
        self.bid = random.randint(0, 14)
        return self.bid

    def get_trump(self):
        no_trump = ['asc','desc']
        trump = ['h','d','c','s']
        if self.bid % 2 == 0:
            return no_trump[random.randint(0,1)]
        else:
            return trump[random.randint(0,3)]

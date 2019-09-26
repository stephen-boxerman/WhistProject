def next_player(player):
    return (player + 1) % 4

def is_legal(card, suit):
    return card[0] == suit
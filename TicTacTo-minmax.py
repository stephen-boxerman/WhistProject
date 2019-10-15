import math

def minmax(curDepth, nodeIdx, maxTurn, scores, targetDepth):
    if curDepth == targetDepth:
        return scores[nodeIdx]

    if maxTurn:
        return max(minmax(curDepth + 1,
                          nodeIdx * 2,
                          False, scores,
                          targetDepth),
                   minmax(curDepth + 1,
                          nodeIdx * 2 + 1,
                          True, scores,
                          targetDepth))
    else:
        return min(minmax(curDepth + 1,
                          nodeIdx * 2,
                          True, scores,
                          targetDepth),
                   minmax(curDepth + 1,
                          nodeIdx * 2 + 1,
                          True, scores,
                          targetDepth))

def createBoard():
    board = [[],[],[]]
    for i in range(3):
        for j in range(3):
            board[i].append('-')
    return board

def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                return True
    return False

def getOppPlayer(players, player):
    index = players.index(player)

    oppIndex = (index + 1) % len(players)

    oppPlayer = players[oppIndex]

    return oppPlayer

def eval(player, players, board):
    oppPlayer = getOppPlayer(players, player)
    for row in range(3):
        if board[row] == [player, player, player]:
            return 10
        elif board[row] == [oppPlayer, oppPlayer, oppPlayer]:
            return -10

    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == player:
                return 10
            elif board[0][col] == oppPlayer:
                return -10
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == player:
            return 10
        elif board[0][0] == oppPlayer:
            return -10

    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == player:
            return 10
        elif board[0][2] == oppPlayer:
            return -10

    return 0


def ticTacToMinMax(board, isMax, player, players):

    score = 0
    oppPlayer = getOppPlayer(players, player)

    if eval(player, players, board) == 10:
        score += 1
    elif eval(player, players, board) == -10:
        score -= 1

    if isMax:

        for i in range(3):
            for j in range(3):

                if board[i][j] == '-':
                    board[i][j] = player
                    score += ticTacToMinMax(board, not isMax, player, players)
                    board[i][j] = '-'

        return score
    else:

        for i in range(3):
            for j in range(3):

                if board[i][j] == '-':
                    board[i][j] = oppPlayer
                    score += ticTacToMinMax(board, not isMax, player, players)
                    board[i][j] = '-'

        return score


def findBestMove(board, player, players):
    bestVal = -float('inf')
    moveVal = 0
    bestMove = []

    for row in range(3):
        for col in range(3):

            if board[row][col] == '-':
                board[row][col] = player
                moveVal = ticTacToMinMax(board, False, player, players)
                board[row][col] = '-'

                if moveVal > bestVal:
                    bestVal = moveVal
                    bestMove = [row, col]

    print(bestMove)
    return bestMove


def main():
    board = createBoard()
    players = ['x','o']

    hasWon = False
    playerIdx = 1

    while isMovesLeft(board):
        player = players[playerIdx]
        move = findBestMove(board, player, players)
        board[move[0]][move[1]] = player

        playerIdx = (playerIdx + 1) % 2

        for row in board:
            print(row)
        print('\n')

        if eval(player, players, board) != 0:
            break


main()
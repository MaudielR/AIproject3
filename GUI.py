import random

import pygame as p
import math
import random
import sys
from itertools import product
import copy
import time

from pip._vendor.distlib.compat import raw_input


class Node(object):
    # Maximizing player is true if Agent, False if User
    # userPieces and opponentPieces is a list of all pieces
    def __init__(self, maximizingPlayer, agentPieces, playerPieces):
        self.maximizingPlayer = maximizingPlayer
        self.agent = agentPieces
        self.player = playerPieces


# Builds a Grid where EE is Empty and TT is for Pit, Agent occupies the top row and Player occupies the bottom row
def buildGrid(D):
    grid = [["EE " for i in range(D)] for j in range(D)]

    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE ":
                grid[row][col] = "TT "
                pits -= 1

    count = 0
    for row in range(0, D):
        if count == 0:
            grid[0][row] = "AW "
            grid[D - 1][row] = "PW "
            count += 1
        elif count == 1:
            grid[0][row] = "AH "
            grid[D - 1][row] = "PH "
            count += 1
        else:
            grid[0][row] = "AM "
            grid[D - 1][row] = "PM "
            count = 0

    return grid


# Select Valid Coordinates
def selectValid(grid, D, user):
    print("What piece would you like to move? Enter: (row,col)")
    row, col = tuple(map(int, raw_input().split(',')))
    while not isValid(row, D) or not (isValid(col, D)):
        print(grid[row][col])
        print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + str(D))
        row, col = tuple(map(int, raw_input().split(',')))

    cur = grid[row][col]
    if cur[0] != user and cur[1] != user:
        print(cur)
        if cur[0] == "E":
            print("This is an empty cell")
        elif cur[1] == "T":
            print("This is a pit")
        else:
            print("You have selected your opponents piece")
        selectValid(grid, D, user)
    else:
        print("The piece you have selected is: " + cur + " at the coordinates (" + str(row) + "," + str(col) + ")")
        return row, col
# 1 is Win, -1 is Lose, 0 is Tie
def fight(user, opponent):
    if user == opponent:
        return 0
    elif user == "W":
        if opponent == "M":
            return 1
        else:
            return -1
    elif user == "H":
        if opponent == "W":
            return 1
        else:
            return -1
    else:
        if opponent == "H":
            return 1
        else:
            return -1


def isValid(index, D):
    return 0 <= index < D


def distance(x1, y1, x2, y2):
    return int(math.sqrt((((x2 - x1) ** 2) + ((y2 - y1) ** 2))))


def neighborsSet(D, cell):
    n = []
    for x in product(*(range(coords - 1, coords + 2) for coords in cell)):
        if x != cell and all(0 <= n < D for n in x):
            n.append(x)
    return n

def neighborSetScalable(D, cell):
    n = []
    for x in product(*(range(coords - (D//3), coords + 1 + (D//3)) for coords in cell)):
        if x != cell and all(0 <= n < D for n in x):
            n.append(x)
    return n

# If someone has fallen in a pit TT is changed to T[User who fell in] if both users have fallen in it just becomes EE
def move(cords, grid, D, user, node):
    print("Where would you like to move? Enter: (row,col)")
    cR, cC = cords
    nR, nC = tuple(map(int, raw_input().split(',')))
    curr = grid[cR][cC]
    while not (isValid(nR, D)) or not (isValid(nC, D)) or distance(nR, nC, cR, cC) != 1:
        if distance(cR, nR, cC, nC) != 1:
            print("Invalid coordinate, please input (row,col) within 1 cell of " + str(cords))
        else:
            print("Invalid coordinate, please input (row,col) within the bounds of 0 and " + str(D))
        nR, nC = tuple(map(int, raw_input().split(',')))

    next = grid[nR][nC]

    # Decides what happens to the targeted cell
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        move(cords, grid, D, user, node)
    # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[:2]
            updatePosition(user, node, cords, (nR, nC))
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user, node, (nR, nC))
            grid[nR][nC] = "EE "
            loseAuto(user, node, cords)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            loseAuto(user, node, cords)
    # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
        updatePosition(user, node, cords, (nR, nC))
    # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            winAuto(user, node, (nR, nC))
            loseAuto(user, node, cords)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            winAuto(user, node, (nR, nC))
            updatePosition(user, node, cords, (nR, nC))
        else:
            loseAuto(user, node, cords)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid


# Assume these coords are always valid
def moveAuto(cords, moveTo, grid, user, node):
    cR, cC = cords
    nR, nC = moveTo
    curr = grid[cR][cC]
    next = grid[nR][nC]
    # print("User: " + user + " Cords: " + str(cords) + " moveTo: " + str(moveTo))
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[:2]
            updatePosition(user, node, cords, moveTo)
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user, node, moveTo)
            grid[nR][nC] = "EE "
            loseAuto(user, node, cords)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            loseAuto(user, node, cords)
        # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
        updatePosition(user, node, cords, moveTo)
        # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            winAuto(user, node, moveTo)
            loseAuto(user, node, cords)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            winAuto(user, node, moveTo)
            updatePosition(user, node, cords, moveTo)
        else:
            loseAuto(user, node, cords)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid


# The user who wins causes the other user to lose points
def winAuto(user, node, cord):
    if user == "P":
        node.agent.remove(cord)
    else:
        node.player.remove(cord)


# Is Win but reversed
def loseAuto(user, node, cord):
    if user == "P":
        node.player.remove(cord)
    else:
        node.agent.remove(cord)


def updatePosition(user, node, cord, moveTo):
    if user == "P":
        node.player.remove(cord)
        node.player.append(moveTo)
    else:
        node.agent.remove(cord)
        node.agent.append(moveTo)


# Minimax algorithm without Alpha-Beta pruning, still uses the evaluation method. But it's slow
def NoPruningMinmax(node, depth, grid):
    global valid
    if depth == 0 or (len(node.agent) == 0 or len(node.player) == 0):
        return evaluatePosition(node, grid), depth
    if node.maximizingPlayer:
        maxVal = -10000000
        bestMove, origin = None, None
        # Look at every piece the current user possesses
        for piece in node.agent:
            # Filter Valid Coordinates by List of User Pieces
            for validMove in list(filter(lambda x: x not in node.agent, valid[piece])):
                tempGrid = copy.deepcopy(grid)  # Shallow copy of the Grid so as not to effect the actual game
                next = Node(False, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                # Here we updated user and opponent lists within the next node on the temporary grid
                moveAuto(piece, validMove, tempGrid, "A", next)
                # Now we get the Max, we stay on the temporary grid cause algorithm isn't finished
                val = NoPruningMinmax(next, depth - 1, tempGrid)[0]
                maxVal = max(maxVal, val)
                if maxVal == val:
                    origin = piece
                    bestMove = validMove

        return maxVal, origin, bestMove
    else:
        minVal = 100000000
        bestMove, origin = None, None
        for piece in node.player:
            for validMove in list(filter(lambda x: x not in node.player, valid[piece])):
                tempGrid = copy.deepcopy(grid)
                next = Node(True, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                moveAuto(piece, validMove, tempGrid, "P", next)
                val = NoPruningMinmax(next, depth - 1, tempGrid)[0]
                minVal = min(minVal, val)
                if minVal == val:
                    origin = piece
                    bestMove = validMove
        return minVal, origin, bestMove


# Minimax with alpha-beta pruning and evaluation method
def minmax(node, depth, grid, alpha, beta):
    global valid
    if depth == 0 or (len(node.agent) == 0 or len(node.player) == 0):
        return evaluatePosition(node, grid), depth
    if node.maximizingPlayer:
        maxVal = -10000000
        bestMove, origin = None, None
        # Look at every piece the current user possesses
        for piece in node.agent:
            # Filter Valid Coordinates by List of User Pieces
            for validMove in list(filter(lambda x: x not in node.agent, valid[piece])):
                tempGrid = copy.deepcopy(grid)  # Shallow copy of the Grid so as not to effect the actual game
                next = Node(False, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                # Here we updated user and opponent lists within the next node on the temporary grid
                moveAuto(piece, validMove, tempGrid, "A", next)
                # Now we get the Max, we stay on the temporary grid cause algorithm isn't finished
                val = minmax(next, depth - 1, tempGrid, alpha, beta)[0]
                maxVal = max(maxVal, val)
                alpha = max(alpha, maxVal)
                if maxVal == val:
                    origin = piece
                    bestMove = validMove
                if beta <= alpha:
                    break
        return maxVal, origin, bestMove
    else:
        minVal = 100000000
        bestMove, origin = None, None
        for piece in node.player:
            for validMove in list(filter(lambda x: x not in node.player, valid[piece])):
                tempGrid = copy.deepcopy(grid)
                next = Node(True, copy.deepcopy(node.agent), copy.deepcopy(node.player))
                moveAuto(piece, validMove, tempGrid, "P", next)
                val = minmax(next, depth - 1, tempGrid, alpha, beta)[0]
                minVal = min(minVal, val)
                beta = min(beta, minVal)
                if minVal == val:
                    origin = piece
                    bestMove = validMove
                if beta <= alpha:
                    break
        return minVal, origin, bestMove

def evaluatePosition(node, gird):
    evaluation = 0
    for piece in node.agent:
        pR, pC = piece
        pieceType = gird[pR][pC]
        if pieceType[0] == "T":
            pT = pieceType[2]
        else:
            pT = pieceType[1]
        # Every player piece near agent piece
        for nearPlayer in list(filter(lambda x: x not in node.agent and x in node.player,neighborSetScalable(D,piece))):
            nR, nC = nearPlayer
            nearType = gird[nR][nC]
            if nearType[0] == "T":
                nT = nearType[2]
            else:
                nT = nearType[1]
            evaluation += fight(pT, nT)
    return evaluation + ((len(node.agent) - len(node.player))*1.5)


print("What size board would you like?")
width, height = 400, 400
margin = 5
global W, H, M, cellSize, valid, playerPieces, agentPieces, D, select
valid = {}
playerPieces, agentPieces = [], []
pCord, pMove = (-1, -1), (-1, -1)


def setGlobals(IO):
    global W, H, M, cellSize, valid, playerPieces, agentPieces, D
    D = IO
    while D%3 != 0:
        print("Size of the board must be a multiple of 3")
        D = int(input())
    cellSize = (width // D) - margin
    W = p.transform.scale(p.image.load("Wumpus.png"), (cellSize, cellSize))
    H = p.transform.scale(p.image.load("Hero.png"), (cellSize, cellSize))
    M = p.transform.scale(p.image.load("Mage.png"), (cellSize, cellSize))
    for x in range(0, D):
        for y in range(0, D):
            valid[(x, y)] = neighborsSet(D, (x, y))
    for i in range(0, D):
        playerPieces.append((D - 1, i))
        agentPieces.append((0, i))


# Builds a Grid where EE is Empty and TT is for Pit, Agent occupies the top row and Player occupies the bottom row
def buildGrid(D):
    grid = [["EE " for i in range(D)] for j in range(D)]
    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE ":
                grid[row][col] = "TT "
                pits -= 1

    count = 0
    for row in range(0, D):
        if count == 0:
            grid[0][row] = "AW "
            grid[D - 1][row] = "PW "
            count += 1
        elif count == 1:
            grid[0][row] = "AH "
            grid[D - 1][row] = "PH "
            count += 1
        else:
            grid[0][row] = "AM "
            grid[D - 1][row] = "PM "
            count = 0

    return grid


def main():
    setGlobals(int(input()))
    grid = buildGrid(D)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    p.init()
    clock = p.time.Clock()
    screen = p.display.set_mode((width, height))
    screen.fill(p.Color("black"))
    running = True
    node = Node(True, agentPieces, playerPieces)
    AI = 0
    while running:
        if len(node.player) == 0 or len(node.agent) == 0:
            break
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                if AI == 0:
                    print("Starting MinMax Algo")
                    first, cord, moveTo = minmax(node,4, grid, -100000, 1000000)
                    moveAuto(cord, moveTo, grid, "A", node)
                    AI += 1
                else:
                    print("You may now select a piece")
                    pos = p.mouse.get_pos()
                    pC = pos[0] // (cellSize + margin)
                    pR = pos[1] // (cellSize + margin)

                    if AI == 1:
                        cur = grid[pR][pC]
                        if cur[0] != "P":
                            if cur[0] == "E":
                                print("This is an empty cell")
                            elif cur[0] == "T":
                                if cur[1] == "P" and cur[2] != " ":
                                    print("You have selected a piece!")
                                    pCord = (pR, pC)
                                    AI += 1
                                else:
                                    print("This is a pit")
                            else:
                                print("You have selected your opponents piece")
                        else:
                            print("You have selected a piece!")
                            pCord = (pR, pC)
                            AI += 1
                    elif (pR,pC) in list(filter(lambda x: x not in node.player, valid[pCord])):
                        pMove = (pR, pC)
                        moveAuto(pCord, pMove, grid, "P", node)
                        AI = 0
                    else:
                        print("This is an invalid piece")
        clock.tick(15)
        screen = drawBoard(screen, grid)
        p.display.flip()
    if len(node.player) == 0 and len(node.agent) == 0:
        print("TIE!")
    elif len(node.agent) == 0:
        print("Player Won!")
    else:
        print("Player Lost!")
    p.quit



# Draw board state
def drawBoard(screen, grid):
    for r in range(D):
        for c in range(D):
            type = grid[r][c]
            if type[0] != "T":
                p.draw.rect(screen, p.Color("White"),
                            [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize])
                loadPiece(screen, type[1], r, c)
            else:
                if type[1] == "P":
                    p.draw.rect(screen, p.Color("Green"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize,
                                 cellSize])
                elif type[1] == "A":
                    p.draw.rect(screen, p.Color("Red"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize,
                                 cellSize])
                else:
                    p.draw.rect(screen, p.Color("Grey"),
                                [(margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize])
                loadPiece(screen, type[2], r, c)
    return screen

def loadPiece(screen, type, r, c):
    if type == "W":
        screen.blit(W, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize))
    elif type == "H":
        screen.blit(H, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize))
    elif type == "M":
        screen.blit(M, p.Rect((margin + cellSize) * c + margin, (margin + cellSize) * r + margin, cellSize, cellSize))


if __name__ == '__main__':
    main()


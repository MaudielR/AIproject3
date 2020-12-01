import math
import random
import sys
from itertools import product

from pip._vendor.distlib.compat import raw_input


class Node(object):
    # Valid must be initalized with valid[cell] before hand
    # Value should be a tuple (playerScore, agentScore)
    def __init__(self, alpha, beta, maximizingPlayer, initalScore, valid):
        self.alpha = alpha
        self.beta = beta
        self.maximizingPlayer = maximizingPlayer
        self.value = initalScore
        self.childnodes = valid
        self.children()


def buildGrid(D):
    # Grid size is DxD
    # EE is Empty and TT is for Pit
    grid = [["EE " for i in range(D)] for j in range(D)]

    for col in range(1, D - 1):
        pits = (D / 3) - 1
        while pits != 0:
            row = random.randint(0, D - 1)
            if grid[row][col] == "EE ":
                grid[row][col] = "TT "
                pits -= 1

    count = 0;
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


# If someone has fallen in a pit TT is changed to T[User who fell in] if both users have fallen in it just becomes EE
def move(cords, grid, D, user):
    global playerScore, agentScore
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
        move(cords, grid, D, user)
    # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[0, 1]
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                win(user)
            grid[nR][nC] = "EE "
            lose(user)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            lose(user)
    # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
    # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            win(user)
            lose(user)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            win(user)
        else:
            lose(user)

    # Decides what current cell should be
    if curr == "T":
        grid[cR][cC] = "T" + user + " "
    else:
        grid[cR][cC] = "EE "
    return grid


# Assume these coords are always valid
# Return 9 if invalid move
def moveAuto(cords, moveTo, grid, user, node):
    cR, cC = cords
    nR, nC = moveTo
    curr = grid[cR][cC]
    next = grid[nR][nC]
    if next[0] == user:
        print("Invalid coordinate, you are trying to move into your own piece")
        return False
    # It is a trap!
    elif next[0] == "T":
        if next[1] == user:  # The user has already fallen so they just step over it
            grid[nR][nC] = "T" + curr[0, 1]
        elif next[1] != "T":  # The user falls, but at this point both have fallen in so we change to EE
            if next[2] != " ":  # The user has found an opponent over a trapped space so they both die!
                winAuto(user, node)
            grid[nR][nC] = "EE "
            node.value = loseAuto(user, node)
        else:  # No one has fallen, and the user falls in
            grid[nR][nC] = "T" + user + " "
            node.value = loseAuto(user, node)
    # It is empty
    elif next[0] == "E":
        if curr == "T":
            grid[nR][nC] = curr[1:] + " "
        else:
            grid[nR][nC] = curr
    # It is the opposing user
    else:
        if fight(curr[1], next[1]) == 0:
            grid[nR][nC] = "EE "
            node.value = winAuto(user, node)
            node.value = loseAuto(user, node)
        elif fight(curr[1], next[1]) == 1:
            grid[nR][nC] = curr
            node.value = winAuto(user, node)
        else:
            node.value = loseAuto(user, node)
    return True


# The user who wins causes the other user to lose points
def winAuto(user, node):
    if user == "P":
        return node.value[0], node.value[1] - 1
    else:
        return node.value[0] - 1, node.value[1]


# Is Win but reversed
def loseAuto(user, node):
    global playerScore, agentScore
    if user == "P":
        return node.value[0] - 1, node.value[1]
    else:
        return node.value[0], node.value[1] - 1

# The user who wins causes the other user to lose points
def win(user):
    global playerScore, agentScore
    if user == "P":
        agentScore -= 1
    else:
        playerScore -= 1


# Is Win but reversed
def lose(user):
    global playerScore, agentScore
    if user == "P":
        playerScore -= 1
    else:
        agentScore -= 1


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


def neighborsSet(grid, D, cell):
    n = []
    for x in product(*(range(coords - 1, coords + 2) for coords in cell)):
        if x != cell and all(0 <= n < D for n in x):
            n.append(x)
    neighbors = {cell: n}
    return neighbors

# maximizingPlayer just needs to a boolean in this case, if user true, if not false
def minmax(node, depth, maximizingPlayer, grid):
    global valid
    if depth == 0 or node.value == 0:
        return node.value

    if maximizingPlayer:
        maxVal = sys.maxsize * -1
        # This is only cords at this point
        for child in node:
            tempGrid = grid
            next = Node(0, 0, "P", node.value, valid[child])  # Ignoring alpha and beta for now
            change = moveAuto(node.root, child, tempGrid, node.maximizingPlayer, next)
            if change:
                maxVal = max(maxVal, minmax(next, depth - 1, False))
                return maxVal
    else:
        minVal = sys.maxsize
        for child in node:
            tempGrid = grid
            #This needs to be a node
            minVal = min(minVal, minmax(child, depth - 1, True))



def main():
    global playerScore, agentScore
    listOfN = []
    for x in range(0, 3):
        for y in range(0, 3):
            listOfN.append(neighborsSet(3, (x, y)))


    """
    print("Input Grid Size")
    D = int(input())
    while D % 3 != 0 or D <= 0:
        print("Grid Size must be a multiple of 3 and greater than 0 ")
        D = int(input())
    print(D)
    grid = buildGrid(D)
    global playerScore, agentScore
    playerScore, agentScore = D, D
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print("Player Score: " +str(playerScore)+ " Agent Score: " +str(agentScore))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print("Player Score: " + str(playerScore) + " Agent Score: " + str(agentScore))

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid[4][5] = "TT "
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    cords = selectValid(grid, D, "P")
    grid = move(cords, grid, D, "P")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    """


if __name__ == '__main__':
    main()

class gameBoard:
    def __init__(self, initialState = None):
        if initialState == None:
            self.state = ["*", "*", "*", "*", "*", "*", "*", "*", "*",]
        else:
            self.state = initialState
    def __str__(self):
        rString = "%s %s %s\n" % (self.state[0], self.state[1], self.state[2])
        rString = rString + "%s %s %s\n" % (self.state[3], self.state[4], self.state[5])
        rString = rString + "%s %s %s\n" % (self.state[6], self.state[7], self.state[8])
        return rString
    def isOver(self):
        possibleWins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for posible in possibleWins:
            if (self.state[posible[0]] == self.state[posible[1]]) and (self.state[posible[1]] == self.state[posible[2]]):
                if self.state[posible[0]] != "*":
                    return [True, self.state[posible[0]]]
        for x in range(len(self.state)):
            if self.state[x] == "*":
                return [False]
        return [True, "T"]

def expandMe(gState, player):
    returnList = []
    for x in range(len(gState)):
        if gState[x] == "*":
            tempList = gState.copy()
            tempList[x] = player
            returnList += [tempList]
    return returnList
    
class Tree(object):
    def __init__(self, parent, state, player, playerTree):
        self.parent = parent
        self.state = state
        self.player = player #The player deciding what move to make
        self.playerTree = playerTree #Whose Tree does this belong to
        isItOver = self.state.isOver()
        if isItOver[0]:
            if isItOver[1] == "T":
                self.value = 0
            else:
                if isItOver[1] == playerTree:
                    self.value = 10
                else:
                    self.value = -10
        else:
            self.children = []
            childStates = expandMe(self.state.state, self.player)
            #Loop create children
            for childS in childStates:
                if player == "X":
                    self.children += [Tree(self, gameBoard(childS), "O", playerTree)]
                else:
                    self.children += [Tree(self, gameBoard(childS), "X", playerTree)]
            if player != playerTree:
                #find min of children and set as value
                self.value = 20
                for x in range(len(self.children)):
                    if self.children[x].value < self.value:
                        self.value = self.children[x].value
            else:
                #find max of children
                self.value = -20
                for x in range(len(self.children)):
                    if self.children[x].value > self.value:
                        self.value = self.children[x].value
    
def miniMaxSearch(gState, playerTurn):
    """
    1) Set given state to head of tree
    Begin Loop
    2) Is game over? No == The node should expand its children
        1) List put appropiate value X or O in each available * for each new child
        2) Make child with parent, alteredState, oposite player of creator
        3) Child asks is game over Yes- if Player == playerTurn value = -10 else value = 10, if T value = 0
            No == time to make more children
    3) Check scores of children and make value correct one min or max"""
    root = Tree(None, gState, playerTurn, playerTurn)
    #find root child with value == root value
    for child in root.children:
        if child.value == root.value:
            return child.state
    print("No Child Error", gState, playerTurn, root.value)
    return None

import random

def start():
    newGame = gameBoard()
    newGame.state[random.randint(0, 8)] = "X"
    playerTurn = "O"
    isItOver = newGame.isOver()
    while not isItOver[0]:
        print(newGame, "")
        newGame = miniMaxSearch(newGame, playerTurn)
        if playerTurn == "O":
            playerTurn = "X"
        else:
            playerTurn = "O"
        isItOver = newGame.isOver()
    print(newGame, "")
    if newGame.isOver()[1] == "T":
        print("Result: Draw Game")
    else:
        print("Result: %s" % (isItOver[1]))

test = gameBoard()
test.state = ["O", "*", "X", "X", "*", "*", "X", "O", "O",]
print(test.isOver())
root = Tree(None, test, "X", "X")
print(root.value)
print("")
print(test, "")
print(miniMaxSearch(test, "X"))
print("\nEnd of test\n\n\n")

#You are not Allowed to modify the code below this line.
#you need to implement print_result function to print out the result according to the required format
start()

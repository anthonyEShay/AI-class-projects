#The following variables must be used in your program. You can change the location values for testing purposes
numberOfRows = 10
numberOfCols = 10
stoneLocation=[2, 8]  #[row, column]
positiveTerminalLocation = [0,9,2]  #[row, column, reward value]
nagativeTerminalLocation = [1,9, -2]  #[row, column, reward value]
iteration=20
noise=0.15
discount=0.91

'''
numberOfRows = 3
numberOfCols = 4
stoneLocation=[1, 1]  #[row, column]
positiveTerminalLocation = [0,3, 1]  #[row, column, reward value]
nagativeTerminalLocation = [1,3, -1]  #[row, column, reward value]
noise=0.2
discount=0.9'''

symbol = {"n": "^", "e":">", "s":"v", "w":"<"}

class square:
    def __init__(self, letter = "-", score = 0.00):
        self.rep = letter
        self.score = score
        self.direction = "n"

class gState:
    def __init__(self, boardX, boardY): #(rows, cols)
        self.sizeX = boardX + 2
        self.sizeY = boardY + 2
        self.reward = positiveTerminalLocation[2]
        self.negative = nagativeTerminalLocation[2]
        self.board = [[None for _ in range(self.sizeY)] for _ in range(self.sizeX)]
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                temp = square()
                self.board[x][y] = temp
        self.board[stoneLocation[0] + 1][stoneLocation[1]+ 1].rep = "S"
        self.board[positiveTerminalLocation[0]+ 1][positiveTerminalLocation[1]+ 1].rep = "P"
        self.board[positiveTerminalLocation[0]+ 1][positiveTerminalLocation[1]+ 1].score = self.reward
        self.board[nagativeTerminalLocation[0]+ 1][nagativeTerminalLocation[1]+ 1].rep = "N"
        self.board[nagativeTerminalLocation[0]+ 1][nagativeTerminalLocation[1]+ 1].score = self.negative
        for x in range(self.sizeY):
            self.board[0][x].rep = "W"
            self.board[self.sizeX - 1][x].rep = "W"
        for y in range(self.sizeX):
            self.board[y][0].rep = "W"
            self.board[y][self.sizeY - 1].rep = "W"
    def __str__(self):
        rString = ""
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                if self.board[x][y].rep == "-":
                    rString += "%s " % (symbol[self.board[x][y].direction])
                else:
                    rString += "%s " % (self.board[x][y].rep)
            rString += "\n"
        return rString
    def finalString(self):
        rString = ""
        for x in range(1, self.sizeX - 1):
            for y in range(1, self.sizeY - 1):
                if self.board[x][y].rep == "S":
                    rString += "STONE   "
                else:
                    rString += "%.2f(%s) " % (self.board[x][y].score, self.board[x][y].direction)
            rString += "\n"
        return rString

class iterationTree:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state

def sScore(state, add, old):
    if state.board[add[0]][add[1]].rep == "W" or state.board[add[0]][add[1]].rep == "S":
        return state.board[old[0]][old[1]].score
    else:
        return state.board[add[0]][add[1]].score
    
def updateScore(state, x, y):
    if state.board[x][y].rep != "-":
        return [state.board[x][y].score, "n"]
    nn = 1.0 - noise
    score = [0, 0, 0, 0]
    leter = ["n", "e", "s", "w"]
    score[0] = (sScore(state,[x-1,y], [x,y])*nn + sScore(state,[x,y+1], [x,y])*(noise/2) + sScore(state,[x,y-1], [x,y])*(noise/2)) * discount
    score[1] = (sScore(state,[x,y+1], [x,y])*nn + sScore(state,[x-1,y], [x,y])*(noise/2) + sScore(state,[x+1,y], [x,y])*(noise/2)) * discount
    score[2] = (sScore(state,[x+1,y], [x,y])*nn + sScore(state,[x,y+1], [x,y])*(noise/2) + sScore(state,[x,y-1], [x,y])*(noise/2)) * discount
    score[3] = (sScore(state,[x,y-1], [x,y])*nn + sScore(state,[x+1,y], [x,y])*(noise/2) + sScore(state,[x-1,y], [x,y])*(noise/2)) * discount
    maxim = max(score)
    return [maxim, leter[score.index(maxim)]]

def updateAll(state):
    temp = gState(state.sizeX - 2, state.sizeY - 2)
    for x in range(1, temp.sizeX - 1):
            for y in range(1, temp.sizeY - 1):
                tempL = updateScore(state, x, y)
                temp.board[x][y].score = tempL[0]
                temp.board[x][y].direction = tempL[1]
    return temp

#Program assumes noise acts similar to examples shown in class where possible states include the direction chosen and to either
#side but not backwards/the opposite direction of the one chosen. The noise is the chance will take one of the side paths so
#1 - noise is chance of going in chosen direction. Discount is assumed to act like lambda from the Bellman equation. It is
#assumed that R(s)/living reward is 0 since a value for it was not provided.
def start():
    test = gState(numberOfRows, numberOfCols)
    print("Initial")
    print(test)
    print(test.finalString())
    for x in range(1, iteration + 1):
        print(x)
        test = updateAll(test)
        #print(test)
        print(test.finalString())

#You are not Allowed to modify the code below this line.
#you need to implement print_result function to print out the result according to the required format
start()

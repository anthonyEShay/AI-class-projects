class gState:
    def __init__(self, boardSize):
        self.size = boardSize
        self.queens = []
        row = []
        for x in range(boardSize):
            row.append("-")
        self.board = []
        for x in range(boardSize):
            self.board.append(row.copy())
    def __str__(self):
        rString = ""
        for x in range(self.size):
            for y in range(self.size):
                rString += "%s " % (self.board[x][y])
            rString += "\n"
        return rString
    def addQueen(self, queen):
        self.board[queen[0]][queen[1]] = "Q"
        self.queens.append(queen)
    def removeQueen(self,queen):
        if queen in self.queens:
            self.queens.remove(queen)
            self.board[queen[0]][queen[1]] = "-"
        else:
            print("Error - Trying to remove a non queen")
    def copy(self):
        temp = gState(self.size)
        for queen in self.queens:
            temp.addQueen(queen)
        return temp
    def isConstraint(self, move): #This is the backtracking check constraints function that prevents the program
                                  #from picking a value which conflicts with previous assignments
        bSize = self.size - 1
        if self.board[move[0]][move[1]] == "Q":
            return True
        
        x = move[0]
        while x != 0: #N
            x-=1
            if self.board[x][move[1]] == "Q":
                return True
        
        x = move[1]
        while x != 0: #W
            x-=1
            if self.board[move[0]][x] == "Q":
                return True
        
        x = move[0]
        y = move[1]
        while x != 0 and y != 0: #NW
            x-=1
            y-=1
            if self.board[x][y] == "Q":
                return True
        
        x = move[0]
        y = move[1]
        while x != 0 and y != bSize: #NE
            x-=1
            y+=1
            if self.board[x][y] == "Q":
                return True
        
        x = move[0]
        while x != bSize:#E
            x+=1
            if self.board[x][move[1]] == "Q":
                return True
        
        x = move[1]
        while x != bSize:#S
            x+=1
            if self.board[move[0]][x] == "Q":
                return True
        
        x = move[0]
        y = move[1]
        while x != bSize and y != bSize: #SE
            x+=1
            y+=1
            if self.board[x][y] == "Q":
                return True
            
        x = move[0]
        y = move[1]
        while x != bSize and y != 0: #SW
            x+=1
            y-=1
            if self.board[x][y] == "Q":
                return True
        
        return False

class moveTree:
    def __init__(self, parent, move, children, depth):
        self.parent = parent
        self.move = move
        self.children = children
        self.depth = depth #what row is the program choosing for

def addChildren(node, board):
    from random import shuffle
    depth = node.depth + 1
    queens = []
    for x in range(board.size):
        if not board.isConstraint((depth, x)):
            queens.append((depth, x))
    node.children = []
    shuffle(queens) #This really speeds up finding solutions for some numbers but it does
                    #come at the cost of losing a consistent first 4 solutions found.
    for queen in queens:
        temp = moveTree(node, queen, None, depth)
        node.children.append(temp)

def solveNQueens(numQueens):
    if numQueens == 2 or numQueens == 3:
        print("No Solution")
        temp = gState(numQueens)
        return [temp]
    if numQueens == 1:
        temp = gState(1)
        temp.addQueen((0,0))
        return [temp]
    qBoard = gState(numQueens)
    root = moveTree(None, None, None, -1)
    addChildren(root, qBoard)
    curNode = root
    solution = []
    while(len(root.children) != 0):
        if len(curNode.children) != 0:
            curNode = curNode.children[0]
            qBoard.addQueen(curNode.move)
            if curNode.depth + 1 == qBoard.size:
                solution.append(qBoard.copy())
                if len(solution) == 4:
                    break
                qBoard.removeQueen(curNode.move)
                curNode = curNode.parent
                del(curNode.children[0])
                continue
            addChildren(curNode, qBoard)
        else:
            qBoard.removeQueen(curNode.move)
            curNode = curNode.parent
            del(curNode.children[0])
    return solution

solution = solveNQueens(8)
x = 1
for board in solution:
    print(x)
    print(board)
    x += 1

def print_result(result):
    for board in result:
        for queen in board.queens:
            print(queen, end=" ")
        print("\n")

#*****************************For final grading test*****************************
"""Must run this cell to create the printable final result for the segment below I am not allowed to modify
Note: I believe I have backtracking programed properly. For some reason on my computer n=21 took about 3 seconds
n=23 took about 10 seconds and n=22 took a very lethargic 2.5 minutes. I'm not sure why that is but I decided to try
shuffling the order the children (new queen positions to try) are added to the tree and it now pretty consistently 
runs faster but no longer returns the same results in the same order each time."""
numberOfQueens= 22
result = solveNQueens(numberOfQueens)

#You are not Allowed to modify the code below this line.
#you need to implement print_result function to print out the result according to the required format
print_result(result)

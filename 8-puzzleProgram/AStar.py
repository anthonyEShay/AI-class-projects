class gState:
    def __init__(self, initialState):
        self.state = tuple(initialState)
    def __str__(self):
        rString = "%d %d %d\n" % (self.state[0], self.state[1], self.state[2])
        rString = rString + "%d %d %d\n" % (self.state[3], self.state[4], self.state[5])
        rString = rString + "%d %d %d\n" % (self.state[6], self.state[7], self.state[8])
        return rString
    def getState(self):
        return self.state

class Tree(object):
    def __init__(self, parent, state, depth = None):
        self.parent = parent
        self.state = state
        self.depth = depth #being reused to equal g(n) = path cost so far
        self.heuristic = findMisplacedTiles(self.state)
    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)
    
class Tree2(object):
    def __init__(self, parent, state, depth = None):
        self.parent = parent
        self.state = state
        self.depth = depth #being reused to equal g(n) = path cost so far
        self.heuristic = findManhattanSum(self.state)
    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)

class resultObject:
    def __init__(self, solution, programSteps, timeTaken):
        self.solution = solution
        self.programSteps = programSteps
        self.solutionSteps = len(solution)
        self.timeTaken = timeTaken
    
def expandIt(stateOb):
    state0 = [[1, 3], [0, 2, 4], [1, 5], [0, 4, 6], [1, 3, 5, 7], [2, 4, 8], [3, 7], [4, 6, 8], [5, 7]]
    stateList = list(stateOb.getState())
    zeroNum = stateList.index(0)
    toExpand = state0[zeroNum]
    toReturn = []
    for x in toExpand:
        temp = stateList[:]
        temp[x], temp[zeroNum] = temp[zeroNum], temp[x]
        toReturn += [gState(temp)]
    return toReturn

def findMisplacedTiles(stateOb):
    stateFinal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    misplacedT = 0
    stateTest = list(stateOb.getState())
    for x in range(len(stateTest)):
        if stateFinal[x] != stateTest[x]:
            misplacedT += 1
    return misplacedT

def findManhattanSquare(stateList, position):
    statePos = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
    stateFinal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    correctIndex = stateList[position]
    disMiss = 0
    disMiss += abs(statePos[correctIndex][0] - statePos[position][0])
    disMiss += abs(statePos[correctIndex][1] - statePos[position][1])
    return disMiss

def findManhattanSum(stateOb):
    manSum = 0
    stateTest = list(stateOb.getState())
    for x in range(len(stateTest)):
        manSum += findManhattanSquare(stateTest, x)
    return manSum

inputTestLine = "8, 7, 5, 4, 1, 2, 3, 0, 6"

#implementation of function "A Star Misplaced"
# h(n) = number of misplaced tiles; g(n) = number of moves taken so far (the depth of the move tree)
def aStarMisplaced(beginningState):
    import time
    import heapq
    startTime = time.process_time()
    stepCount = 0
    lookingFor = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    finalPath = []
    beginningState = beginningState.strip()
    splitInput = beginningState.split(", ")
    for x in range(len(splitInput)):
        splitInput[x] = int(splitInput[x])
    startingState = gState(splitInput)
    root = Tree(None, startingState, 0)
    searched = {}
    frontier = []
    heapq.heappush(frontier, root)
    #begin main loop
    while len(frontier) is not 0:
        """1) get top of heap, which is lowest f(n) option in the frontier and put into temp
        2) if temp is state what looking for get final path and break
        3) if temp is not state looking for check if it is in searched
            if it is in searched (have seen this state before) throw it out, it is a bad path
            4) else expand that state
            5) add all the expanded values to the heap
            6) add temp to searched
            7) continue"""
        curState = heapq.heappop(frontier)
        if list(curState.state.getState()) == lookingFor:
            while curState is not None:
                finalPath += [curState.state]
                curState = curState.parent
            finalPath.reverse()
            break
        if curState.state.getState() in searched:
            stepCount += 1
            continue
        else:
            expanded = expandIt(curState.state)
            for x in range(len(expanded)):
                newTree = Tree(curState, expanded[x], curState.depth + 1)
                heapq.heappush(frontier, newTree)
            searched[curState.state.getState()] = 1
        stepCount += 1
        
    endTime = time.process_time()
    results = resultObject(finalPath, stepCount, endTime - startTime)
    return [results]

#implementation of function "A Star Manhattan Distance"
# h(n) = total Manhattan distance = sum of move distance from current location to desired location for each tile
# g(n) = number of moves taken so far
def aStarManhattan(beginningState):
    import time
    import heapq
    startTime = time.process_time()
    stepCount = 0
    lookingFor = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    finalPath = []
    beginningState = beginningState.strip()
    splitInput = beginningState.split(", ")
    for x in range(len(splitInput)):
        splitInput[x] = int(splitInput[x])
    startingState = gState(splitInput)
    root = Tree2(None, startingState, 0)
    searched = {}
    frontier = []
    heapq.heappush(frontier, root)
    #begin main loop
    while len(frontier) is not 0:
        curState = heapq.heappop(frontier)
        if list(curState.state.getState()) == lookingFor:
            while curState is not None:
                finalPath += [curState.state]
                curState = curState.parent
            finalPath.reverse()
            break
        if curState.state.getState() in searched:
            stepCount += 1
            continue
        else:
            expanded = expandIt(curState.state)
            for x in range(len(expanded)):
                newTree = Tree2(curState, expanded[x], curState.depth + 1)
                heapq.heappush(frontier, newTree)
            searched[curState.state.getState()] = 1
        stepCount += 1
        
    endTime = time.process_time()
    results = resultObject(finalPath, stepCount, endTime - startTime)
    return [results]

#implementation of breadthFirstSearch, not required, used to test A* functions for completeness
def breadthFirstSearch(beginningState):
    import time
    startTime = time.process_time()
    stepCount = 0
    lookingFor = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    finalPath = []
    beginningState = beginningState.strip()
    splitInput = beginningState.split(", ")
    for x in range(len(splitInput)):
        splitInput[x] = int(splitInput[x])
    startingState = gState(splitInput)
    root = Tree(None, startingState)
    searched = {}
    frontier = [root]
    #begin main loop
    while len(frontier) is not 0:
        if list(frontier[0].state.getState()) == lookingFor:
            temp = frontier[0]
            while temp is not None:
                finalPath += [temp.state]
                temp = temp.parent
            finalPath.reverse()
            break
        if frontier[0].state.getState() in searched:
            del frontier[:1]
            stepCount += 1
            continue
        else:
            expanded = expandIt(frontier[0].state)
            for x in range(len(expanded)):
                newTree = Tree(frontier[0], expanded[x])
                frontier.append(newTree)
            searched[frontier[0].state.getState()] = 1
            del frontier[:1]
        stepCount += 1
    
    endTime = time.process_time()
    results = resultObject(finalPath, stepCount, endTime - startTime)
    return [results]

#implementation of function "print_result(result)"
def print_result(result):
    if len(result) > 1:
        print("Solution of the first Scenario:\n")
        for x in range(len(result[1].solution) - 1):
            print(result[1].solution[x])
            print("to\n")
        print(result[1].solution[len(result[0].solution) - 1])
        print("%10s%20s%20s%20s" % (" ", "Average_Steps", "Average_Solution", "Average_Time"))
        print("%10s%20d%20d%20f" % ("Misplaced", result[0].programSteps, result[0].solutionSteps, result[0].timeTaken))
        print("%10s%20d%20d%20f" % ("Manhattan", result[1].programSteps, result[1].solutionSteps, result[1].timeTaken))
        return
    
    for x in range(len(result[0].solution) - 1):
        print(result[0].solution[x])
        print("to\n")
    print(result[0].solution[len(result[0].solution) - 1])
    print("%6s%20s%20s%20s" % (" ", "Average_Steps", "Average_Solution", "Average_Time"))
    print("%6s%20d%20d%20f" % ("Type", result[0].programSteps, result[0].solutionSteps, result[0].timeTaken))

#*****************************For final grading test*****************************
#Run this cell to create the printable final result for the grading segment below I am not allowed to modify

file = open("Input8PuzzleCases.txt", "r")
lines = file.read().split("\n")
lineCounter = 0
idsValues = [0, 0, 0.0]
bfsValues = [0, 0, 0.0]
firstScenario = 0
lineTimer = 0.0
for line in lines:
    result = aStarMisplaced(line)
    idsValues[0] += result[0].programSteps
    idsValues[1] += result[0].solutionSteps
    idsValues[2] += result[0].timeTaken
    lineTimer += result[0].timeTaken
    result = aStarManhattan(line)
    bfsValues[0] += result[0].programSteps
    bfsValues[1] += result[0].solutionSteps
    bfsValues[2] += result[0].timeTaken
    lineTimer += result[0].timeTaken
    if lineCounter == 0:
        firstScenario = resultObject(result[0].solution, result[0]. programSteps, result[0].timeTaken)
    print("Line %d completed in %f" % (lineCounter, lineTimer))
    lineTimer = 0.0
    lineCounter += 1

result = [resultObject([], idsValues[0] / 100, idsValues[2] / 100)]
result[0].solutionSteps = idsValues[1] / 100
result.append(resultObject(firstScenario.solution, bfsValues[0] / 100, bfsValues[2] / 100))
result[1].solutionSteps = bfsValues[1] / 100
    
    
file.close()

#You are not Allowed to modify the code below this line.
#you need to implement print_result function to print out the result according to the required format
print_result(result)

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
        self.depth = depth

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

inputTestLine = "8, 7, 5, 4, 1, 2, 3, 0, 6"

#implementation of function "Iterative_deepening_DFS"
def depthFirstSearch(beginningState, maxDepth = 50000):
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
    root = Tree(None, startingState, 0)
    searched = {}
    frontier = [root]
    
    #begin main loop
    while len(frontier) is not 0:
        index = len(frontier) - 1
        if list(frontier[index].state.getState()) == lookingFor:
            temp = frontier[index]
            while temp is not None:
                finalPath += [temp.state]
                temp = temp.parent
            finalPath.reverse()
            break
        if frontier[index].state.getState() in searched:
            if frontier[index].depth >= searched[frontier[index].state.getState()]:
                del frontier[index]
                stepCount += 1
                continue
            else:
                searched[frontier[index].state.getState()] = frontier[index].depth
                expanded = expandIt(frontier[index].state)       
                for x in range(len(expanded)):
                    newTree = Tree(frontier[index], expanded[x], frontier[index].depth + 1)
                    frontier.append(newTree)
                del frontier[index]
                stepCount += 1
        else:
            searched[frontier[index].state.getState()] = frontier[index].depth
            if frontier[index].depth == maxDepth:
                del frontier[index]
                stepCount += 1
                continue
            expanded = expandIt(frontier[index].state)       
            for x in range(len(expanded)):
                newTree = Tree(frontier[index], expanded[x], frontier[index].depth + 1)
                frontier.append(newTree)
            del frontier[index]
            stepCount += 1

    endTime = time.process_time()
    results = resultObject(finalPath, stepCount, endTime - startTime)
    return [results]

def iterative_deepening_DFS(beginningState):
    import time
    startTime = time.process_time()
    stepCount = 0
    depthCount = 0
    results = []
    while depthCount < 10000000:
        results = depthFirstSearch(beginningState, depthCount)
        if results[0].solution == []:
            depthCount += 1
            stepCount += results[0].programSteps
            continue
        else:
            stepCount += results[0].programSteps
            break
            
    endTime = time.process_time()
    returnVal = resultObject(results[0].solution, stepCount, endTime - startTime)
    return [returnVal]

#implementation of function "breadthFirstSearch"
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
        print("%6s%20s%20s%20s" % (" ", "Average_Steps", "Average_Solution", "Average_Time"))
        print("%6s%20d%20d%20f" % ("IDS", result[0].programSteps, result[0].solutionSteps, result[0].timeTaken))
        print("%6s%20d%20d%20f" % ("BFS", result[1].programSteps, result[1].solutionSteps, result[1].timeTaken))
        return
    
    for x in range(len(result[0].solution) - 1):
        print(result[0].solution[x])
        print("to\n")
    print(result[0].solution[len(result[0].solution) - 1])
    print("%6s%20s%20s%20s" % (" ", "Average_Steps", "Average_Solution", "Average_Time"))
    print("%6s%20d%20d%20f" % ("Type", result[0].programSteps, result[0].solutionSteps, result[0].timeTaken))

#*****************************For final grading test*****************************
#Run this cell to create the printable final result for the segment below I am not allowed to modify
#Note I got BFS down to about 4 seconds on my machine. IDS should in theory be faster but due to my implementation it leaves
#its data tree fully intact like BFS and so it runs substantially slower due to needing to do a lot more work. It was originally
#sub 1 second but I had to make these slower changes because it was too DFS and not complete and was giving solutions that were
#not optimal,they were longer than BFS, and I am unfortunately out of time because I started too late. So, a full run takes 
#about 10 minutes. Sorry about that.

file = open("Input8PuzzleCases.txt", "r")
lines = file.read().split("\n")
lineCounter = 0
idsValues = [0, 0, 0.0]
bfsValues = [0, 0, 0.0]
firstScenario = 0
lineTimer = 0.0
for line in lines:
    result = iterative_deepening_DFS(line)
    idsValues[0] += result[0].programSteps
    idsValues[1] += result[0].solutionSteps
    idsValues[2] += result[0].timeTaken
    lineTimer += result[0].timeTaken
    if lineCounter < 20:
        result = breadthFirstSearch(line)
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
result.append(resultObject(firstScenario.solution, bfsValues[0] / 20, bfsValues[2] / 20))
result[1].solutionSteps = bfsValues[1] / 20
    
    
file.close()

#You are not Allowed to modify the code below this line.
#you need to implement print_result function to print out the result according to the required format
print_result(result)

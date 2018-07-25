#author Matic Verbič

from random import randint

'''
PAGINATION ALOGRITHMS
'''
def leastRecentlyUsed(calls, stackSize):
    # implementation of Least Recently Used (LRU)
    # algorithm, using double stack, one for pagination
    # one for keeping track of order of usage
    stack = []
    useOrder = []
    for call in calls:
        print(stack)
        if len(stack) < stackSize and call not in stack:
            stack.append(call)
            useOrder.append(call)
            #print(call, "-", stack.index(call))
        elif call not in stack:
            stack[stack.index(useOrder[0])] = call
            useOrder.pop(0)
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)
            #print(call, "-", stack.index(call))
        elif call in stack:
            #print(call, "- hit")
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)

    print(stack)
    return stack

def clockPolicy(calls, stackSize):
    # Clock Policy algoritm that implements a pointer and
    # a triple stack - Tracking the actual stack,
    # order at which pages have been called (used for pointer)
    # and the states of each indivdual page

    stack = []
    useOrder = []
    states = []
    pointer = 0
    for call in calls:
        print(stack, states)
        if len(stack) < stackSize and call not in stack:
            stack.append(call)
            states.append(True)
            useOrder.append(call)
            pointer = stack.index(useOrder[0])
        elif len(stack) < stackSize and call in stack:
            print("hit HERE #TODO FIX")
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)
            pointer = stack.index(useOrder[0])
        elif call not in stack:
            pointer = checkStates(states, pointer)
            del useOrder[useOrder.index(stack[pointer])]
            stack[pointer] = call
            states[pointer] = True
            useOrder.append(call)
        else:
            print("hit HERE #TODO FIX")
            pointer = stack.index(call)
            states[stack.index(call)] = True

    print(stack, states)
    return stack

def secondChance(calls, stackSize):
    # Clock Policy algoritm that implements a pointer and
    # a triple stack - Tracking the actual stack,
    # order at which pages have been called (used for pointer)
    # and the states of each indivdual page
    stack = []
    useOrder = []
    states = []
    pointer = 0
    for call in calls:
        print(stack, states)
        if len(stack) < stackSize and call not in stack:
            stack.append(call)
            states.append(True)
            useOrder.append(call)
            pointer = stack.index(useOrder[0])
        elif len(stack) < stackSize and call in stack:
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)
            pointer = stack.index(useOrder[0])
        elif call not in stack:
            pointer = checkStates(states, pointer)
            del useOrder[useOrder.index(stack[pointer])]
            stack[pointer] = call
            states[pointer] = True
            useOrder.append(call)
        else:
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)
            pointer = stack.index(useOrder[0])
            states[stack.index(call)] = True

    print(stack, states)
    return stack

def optimal(calls, stackSize):
    # Optimal (OPT) algorithm using two stacks for tracking
    # the stack and the use order, that is then used to calculate the
    # farthest distance using the call stack
    stack = []
    useOrder = []
    counter = 0
    pointer = 0
    for call in calls:
        print(stack)
        if len(stack) < stackSize and call not in stack:
            stack.append(call)
            useOrder.append(call)
        elif len(stack) < stackSize and call in stack:
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)
            counter += 1
            continue
        elif call not in stack:
            pointer = findOptimal(calls[counter:], stack, useOrder)
            if len(useOrder) == stackSize:
                del useOrder[useOrder.index(stack[pointer])]
                useOrder.append(call)
            else:
                useOrder.append(call)
            stack[pointer] = call
        elif call in stack:
            useOrder = [item for item in useOrder if item != call]
            useOrder.append(call)
        counter += 1
    print(stack)
    return stack

def firstInFirstOut(calls, stackSize):
    # First in First out algorithm using double stack
    # for tracking the stack and the arrival order of the
    # page
    stack = []
    useOrder = []
    for call in calls:
        print(stack)
        if len(stack) < stackSize and call not in stack:
            stack.append(call)
            useOrder.append(call)
        elif call not in stack:
            stack[stack.index(useOrder[0])] = call
            del useOrder[0]
            useOrder.append(call)
        elif call in stack:
            continue
    print(stack)
    return stack

def lastInFirstOut(calls, stackSize):
    # Last in First out algorithm using double stack
    # for tracking the stack and the arrival order of the
    # page

    stack = [calls[0]]
    useOrder = [calls[0]]
    calls = calls[1:]
    i = 0
    while useOrder:
        print(stack)
        if i < len(calls):
            if len(stack) < stackSize and calls[i] not in stack:
                stack.append(calls[i])
                useOrder.append(calls[i])
                i += 1
            elif len(stack) < stackSize and calls[i] in stack:
                i += 1
                continue
            elif calls[i] not in stack:
                stack[stack.index(useOrder[len(useOrder)-1])] = calls[i]
                del useOrder[len(useOrder)-1]
                useOrder.append(calls[i])
                i += 1
            elif calls and calls[i] in stack:
                i += 1
                continue
        else:
            del stack[stack.index(useOrder[len(useOrder) - 1])]
            del useOrder[len(useOrder) - 1]

    return stack

#########
#HELPERS#
#########

def findOptimal(calls, stack, useOrder):
    distances = []
    for page in stack:
        for call in calls:
            if call == page:
                distances.append(calls.index(page))
                break
        else:
            distances.append(len(calls))

    if distances.count(max(distances)) > 1:
        for use in useOrder:
            ind = stack.index(use)
            if distances[ind] in [distance for distance in distances if distance == max(distances)]:
                return ind

    else:
        return distances.index(max(distances))

def checkStates(statesList, pointer):
    while True:
        if statesList[pointer]:
            statesList[pointer] = False
        else:
            return pointer
        if pointer == len(statesList)-1:
            pointer = 0
        else:
            pointer += 1

def generateValues(max, amount):
    #Generates random stack of page calls
    return [randint(0,max) for x in range(0, amount)]

def printFairShare(result, perGroup, perUser):
    for key, value in result.items():
        print("Group", key, "-", str(perGroup) + "%")
        for key, proc in value.items():
            print("\tUser", key, "-", str(perUser)+"%")
            s = ""
            for process, perc in proc.items():
                s += process + ": " + (str(perc) if len(str(perc)) < 5 else str(perc)[:6]) +"% "
            print("\t\t" + s)

'''
SCHEDULING ALGORITHMS
'''
def firstComeFirstServed(bursts):
    #Simple FCFS algorithm implementation
    queues = [0]
    for burst in bursts:
        queues.append(burst + queues[-1])
    return queues

def roundRobin(times, quantum):
    #Round robin algorithm implementation with commentary and stack
    #to disable commentary, comment out all prints.
    stack = [["P0", times["P0"][1], times["P0"][1]]]
    time = 0
    times = [[key, start, execute] for key, [start, execute] in times.items()]
    alreadyHeld = ["P0"]
    print(stack)
    print("P0 enters at 0\n############################")
    s2 = ""
    st = ""
    while stack:
        s = ""
        finished = False
        for key, start, execute in times[1:]:
            if [key, start, execute] not in stack and key not in alreadyHeld:
                if start >= time+quantum:
                    break
                elif start < time+quantum:
                    stack.append([key, start, execute])
                    alreadyHeld.append(key)
                    st = str(key) + " enters at " + str(start) + "\n"
        print("Current stack after arrivals:")
        print(stack)
        procTime = stack[0][2]
        if (stack[0][2] - quantum <= 0):
            s2 = str(stack[0][0]) + " has finished and leaves the Queue\n"
            finished = True
            time += procTime
            del stack[0]
        if stack:
            stack[0][2] -= quantum
            if finished:
               s = s2 + str(stack[0][0]) + " is processed at " + str(time)+"\n" + st
            else:
                s = str(stack[0][0]) + " is processed at " + str(time)+"\n" + st
            st = ""
            if stack[0][2] <= 0:
                s += str(stack[0][0]) + " has finished and leaves the Queue"
                del stack[0]
            else:
                stack.append(stack[0])
                s += "After {0} ms {1} is forced out and replaced with {2}".format(str(time+100), stack[0][0], stack[1][0])
                del stack[0]
        time = time + quantum
        print(s+"\n############################")

def highestResponseRatioNext(times):
    #HRRTN implementation
    newTimes = [[key, arrival, burst, (arrival+burst)/burst, arrival+burst] for key, arrival, burst in times]
    stack = [newTimes[0]]
    newTimes = newTimes[1:]
    while newTimes:
        newTimes = [[key, arrival, burst, ((stack[-1][-1] - arrival) + burst) / burst, stack[-1][-1] + burst]
                    for key, arrival, burst, ratio, end in newTimes]
        bursts = [ratio for key, arrival, burst, ratio, end in newTimes if arrival <= stack[-1][-1]]
        stack.append(newTimes[bursts.index(max(bursts))])
        del newTimes[bursts.index(max(bursts))]
    return {key: {"arrival": arrival, "end": end, "ratio": ratio} for key, arrival, burst, ratio, end in stack}

def shortestProcessNext(proc):
    #SPN
    data = [[key, arrival, execute, service, service - arrival] for key, arrival, execute, service in proc]
    return {key : [arrival, execute, ratio] for key, arrival, execute, service, ratio in sorted(data, key=lambda item: item[4])}

def shortestRemainingTime(proc, quantum):
    #SRT
    time = sum([burst for key, arrival, burst in proc])
    i = 1
    stack = [proc[0]]
    while i < time:
        queues = []

        i+=1
    #TODO
    #TODO

def highestPriority(proc):
    return sorted(proc, key=lambda a: a[3], reverse=True)

def lowestPriority(proc):
    #duh
    return sorted(proc, key=lambda a: a[3])

def fairShareSchedule(numberOfGroups, numberOfUsers, processes):
    #FSS algorithm
    processingPower = 100
    powerPerGroup = processingPower / numberOfGroups
    powerPerUser = powerPerGroup / numberOfUsers
    table = {}
    for group in processes:
        table[group] = {}
        for user in processes[group]:
            table[group][user] = {}
            for process in processes[group][user]:
                table[group][user][process] = powerPerUser / len(processes[group][user])
    return table, powerPerGroup, powerPerUser

'''
HDD OPERATING ALGORITHMS
'''
def cScan(tracks, start, direction):
    #cyclical scan
    tracks = sorted(tracks)
    if direction == "up":
        l = [abs(track1 - track2) for track1, track2 in zip(tracks[start:]+tracks[:start-1], tracks[start+1:]+tracks[:start])]
    else:
        tracks = reversed(tracks)
        l = [abs(track1 - track2) for track1, track2 in
             zip(tracks[start:] + tracks[:start - 1], tracks[start + 1:] + tracks[:start])]
    return int(sum(l)/len(tracks))

def scan(tracks, start, direction = "up"):
    #directional scan
    tracks = sorted(tracks)
    if direction == "up":
        startIndex = tracks.index(start) if start in tracks else  tracks.index(min(tracks, key=lambda x:abs(x-start)))+1
        lup = [abs(track1 - track2) for track1, track2 in zip(tracks[startIndex:], tracks[startIndex+1:])]
        rev = [item for item in reversed(tracks)][len(tracks)-startIndex:]
        ldown = [abs(track1 - track2) for track1, track2 in zip([tracks[-1]] + rev, rev)]
        return (sum(lup) + sum(ldown)) / len(tracks)
    elif direction == "down":
        rev = [item for item in reversed(tracks)]
        startIndex = rev.index(start) if start in rev else  rev.index(min(tracks, key=lambda x:abs(x-start)))
        lup = [abs(track1 - track2) for track1, track2 in zip(tracks[startIndex:], tracks[startIndex+1:])]
        rev = [item for item in reversed(tracks)][len(tracks)-startIndex:]
        ldown = [abs(track1 - track2) for track1, track2 in zip([tracks[-1]] + rev, rev)]
        return (sum(lup) + sum(ldown)) / len(tracks)

def nScan(tracks, start, direction, n):
    #N-queue scan
    stack = []
    for i in range(1, int(len(tracks)/n)+1):
        stack.append(tracks[n*(i-1):(n*i)])
    startIndex, closest = findClosest(stack[0], start, direction)
    startIndex = stack[0].index(closest)
    stack[0].insert(startIndex, start)
    stack[0] = stack[0][startIndex:] + stack[0][:startIndex]
    i = 0
    sums = []
    last = None
    startFlag = True
    while stack:
        s = []
        stack[i] = sorted(stack[i], reverse=True if direction == "up" else False) if not startFlag else stack[i]
        startFlag = False
        for item1, item2 in zip([last] + stack[i] if last else stack[i], stack[i] if  last else stack[i][1:]):
            print(item1, "-", item2, " = ", abs(item1 - item2))
            if item1 < item2:
                direction = "up"
            else:
                direction = "down"
            s.append(abs(item1 - item2))
        last = stack[i][-1]
        del stack[i]
        if s:
            sums.append(s)

    return sum([sum(s) for s in sums]) / len(tracks)

def fScan(tracks, start, direction):
    #F-scan dual queue
    tCount = len(tracks)//2
    stack = [sorted(tracks[:tCount]), tracks[tCount:]]
    index, closest = findClosest(stack[0], start, direction)
    stack[0] = [start] + stack[0][index-1:] + stack[0][:index-1]
    i = 0
    sums = []
    last = None
    startFlag = True
    while stack:
        s = []
        stack[i] = sorted(stack[i], reverse=True if direction == "up" else False) if not startFlag else stack[i]
        startFlag = False
        for item1, item2 in zip([last] + stack[i] if last else stack[i], stack[i] if last else stack[i][1:]):
            print(item1, "-", item2, " = ", abs(item1 - item2))
            if item1 < item2:
                direction = "up"
            else:
                direction = "down"
            s.append(abs(item1 - item2))
        last = stack[i][-1]
        del stack[i]
        if s:
            sums.append(s)
    return sum([sum(s) for s in sums]) / len(tracks)

def findClosest(firsts, target, direction):
    closest = firsts[0]
    index = 0
    i = 0
    for first in firsts:
        if direction == "up":
            if abs(target - first) < closest and target - first < 0:
                closest = first
                index = i
            i += 1
        elif direction == "down":
            if abs(target - first) < closest and target - first > 0:
                closest = first
                index = i
            i += 1
    return index - 1, closest

def shortestSeekFirst(tracks, start):
    #SSF algorithm
    sums = []
    l = len(tracks)
    stack = [start]
    last = start
    tracks = tracks[1:]
    s = 0
    while tracks:
        min = abs(tracks[0] - stack[-1])
        index = 0
        for track in tracks:
            if abs(tracks[0] - start) < min:
                min = abs(tracks[0] - stack[-1])
                index = tracks.index(track)
        stack.append(tracks[index])
        del tracks[index]
        s += min
        #print(stack)
    return s/l


'''
CALLS
'''

###################
#To generate random list of value for page sorting algorithms uncomment next line
###################
calls = generateValues(9, 10)
#print(calls)

###################
#To use the code, find the algorithm you'd like to use and
#Uncomment it's call and accompanying data or create your own data
###################


###############
#PAGINATION
###############


'''LRU'''
'''list of positive integer, number of channels'''
#print(leastRecentlyUsed(calls, 3))

'''Clock Policy'''
'''list of positive integer, number of channels'''
print(calls, clockPolicy(calls, 3))

'''Second Chance'''
'''list of positive integer, number of channels'''
print(calls, secondChance(calls, 3))

'''Optimal algorith'''
'''list of positive integer, number of channels'''
#optimal(calls, 3)

'''FIFO'''
'''list of positive integer, number of channels'''
#firstInFirstOut(calls, 3)

'''LIFO '''
'''list of positive integer, number of channels'''
#lastInFirstOut(calls, 3)

#################
#PROCESSESS
#################

'''First Come First Served'''
'''list of positive integers'''
#calls = generateValues(50, 10)
#i = 0
#print(calls)
#for queue in firstComeFirstServed(calls):
#    print("P"+str(i), "-", queue, "time")
#    i += 1

'''Round Robin'''
'''Dictionary{"processName": [arrival, burst]}'''
proc = {
        "P0": [0, 250],
        "P1": [50, 170],
        "P2": [130, 75],
        "P3": [190, 100],
        "P4": [210, 130],
        "P5": [350, 50]
    }

#roundRobin(proc, 100)

'''Highest Response Ratio Next'''
'''Dictionary{"processName": [arrival, burst]}'''
proc = [
        ["P0", 0, 3],
        ["P1", 2, 6],
        ["P2", 4, 4],
        ["P3", 6, 5],
        ["P4", 8, 2],
    ]

#for key, value in highestResponseRatioNext(proc).items():
#    print("Process", key, "arrived at", value["arrival"], "and ended at", value["end"], "with ratio", value["ratio"])

'''Shortest Process Next'''
'''Dictionary{"processName": [arrival, execute, service]}'''
proc = [
        ["P0", 0, 5,  3],
        ["P1", 1, 3,  1],
        ["P2", 2, 8, 16],
        ["P3", 3, 6,  8],
    ]
#sum = 0
#for key, [arrival, execution, ratio] in shortestProcessNext(proc).items():
#    sum += execution
#    print(key, "arrived at time", arrival, "needed", execution, "and finished at", sum, "with ratio", ratio)

'''Highest Priority First'''
'''Dictionary{"processName": [arrival, execute, priority]}'''

proc = [
        ["P0", 0, 5,  3],
        ["P1", 1, 3,  1],
        ["P2", 2, 8, 16],
        ["P3", 3, 6,  8],
    ]
#print(highestPriority(proc))

'''Lowest Priority First'''
'''Dictionary{"processName": [arrival, execute, priority]}'''

proc = [
        ["P0", 0, 5, -20],
        ["P1", 1, 3,  10],
        ["P2", 2, 8, 16],
        ["P3", 3, 6,  0],
    ]
#print(lowestPriority(proc))

'''Fair Share First'''
'''Dictionary{"GroupName": {"Username": [processes]}}'''

proc = {
          "G0": { "U1": ["P1", "P2", "P3", "P4", "P5"],
                  "U2": ["P1", "P2", "P3", "P4", "P5"],
                  "U3": ["P1", "P2", "P3", "P4", "P5"],
                  "U4": ["P1", "P2", "P3", "P4", "P5"],
                  #"U5": ["P1", "P2", "P3", "P4", "P5"],
                  },
          "G1": { "U1": ["P1", "P2", "P3", "P4", "P5"],
                  "U2": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],
                  "U3": ["P1", "P2", "P3", "P4", "P5", "P6"],
                  "U4": ["P1", "P2", "P3", "P4", "P5"],
                  "U5": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
                  },
          "G2": { "U1": ["P1", "P2", "P3", "P4", "P5"],
                  "U2": ["P1", "P2"],
                  "U3": ["P1", "P2", "P3", "P4", "P5"],
                  "U4": ["P1"],
                  "U5": ["P1", "P2", "P3", "P4", "P5"],
                  },
          "G3": { "U1": ["P1", "P2", "P3", "P4", "P5"],
                  "U2": ["P1", "P2", "P3", "P4", "P5"],
                  "U3": ["P1", "P2", "P3", "P4", "P5"],
                  "U4": ["P1", "P2", "P3", "P4", "P5"],
                  "U5": ["P1", "P2", "P3", "P4", "P5"],
                  },

}

#result, perGroup, perUser = fairShareSchedule(4, 5, proc)

#printFairShare()

'''Scan, N-Step Scan, F-Scan, C-Scan'''
'''[tracks], first track to start on, direction'''
#print([100, 102, 104, 106, 101, 103, 105, 107, 108], scan([100, 102, 104, 106, 101, 103, 105, 107, 108], 106, "down"))
'''[tracks], first track to start on, direction, number of queues'''
#print([100, 102, 104, 103, 102, 100, 108, 107], nScan([100, 102, 104, 103, 102, 100, 108, 107], 101, "up", 2))
'''[tracks], first track to start on, direction'''
#print([100, 102, 104, 103, 102, 100, 108, 107], fScan([100, 102, 104, 103, 102, 100, 108, 107], 101, "up"))
'''[tracks], first track to start on, direction number of queues'''
#print([100, 102, 104, 103, 102, 100, 108, 107], cScan([100, 102, 104, 103, 102, 100, 108, 107], 101, "up", 2))

#print([100, 102, 104, 103, 102, 100, 108, 107], shortestSeekFirst([100, 102, 104, 103, 102, 100, 108, 107], 101))


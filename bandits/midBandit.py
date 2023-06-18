import sys; args = sys.argv[1:]
import math, random


Qn = [0 for i in range(10)]
numCalls = [0 for i in range(10)]
c = 0.78
def bandit(testNum, armIdx, pullVal):
    global Qn
    global numCalls
    global c
    if testNum == 0:
        Qn = [5 for i in range(10)]
        numCalls = [0 for i in range(10)]
        c = 0.78
        return 0
    elif testNum > 0:
        numCalls[armIdx] += 1
        Qn[armIdx] += (pullVal - Qn[armIdx])/numCalls[armIdx]
        if testNum < 20:
            return testNum%10
        A = 0
        argmax = 0
        t = math.log(testNum)
        for i,v in enumerate(Qn):
            val = v + c*math.sqrt(t/numCalls[i])
            if val > argmax:
                A = i
                argmax = val
        return A
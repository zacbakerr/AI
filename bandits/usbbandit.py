import sys; args = sys.argv[1:]
import math, random

def setGlobals():
    global SUMS, COUNTS, AVGS
    # SUMS = [0]*10
    COUNTS = [0]*10
    AVGS = [0]*10

# Qt = current mean
# t = testnum
# c = constnt
# Nta = number of times pulled

def bandit(testNum, armIdx, pullVal):
    if testNum == 0:
        setGlobals()
        return 0
    # SUMS[armIdx] += pullVal
    COUNTS[armIdx] += 1
    # AVGS[armIdx] = SUMS[armIdx] / COUNTS[armIdx]
    AVGS[armIdx] += (pullVal - AVGS[armIdx]) / COUNTS[armIdx]
    if testNum < 20:
        return testNum % 10
    else:
        values = [AVGS[int(i)] + 0.78*math.sqrt((math.log(testNum) / COUNTS[int(i)])) for i in range(10)]
        return values.index(max(values))
    
# Zachary Baker, Pd. 4, 2024
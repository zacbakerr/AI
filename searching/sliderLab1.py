import random
import sys; args = sys.argv[1:]
import time

def getNeighbors(pz):
   neighbors = []
   if ((pz.index('_') + 1) % int(len(pz) ** 0.5)) != 0: neighbors.append(pz[:pz.index('_')] + pz[pz.index('_') + 1] + '_' + pz[pz.index('_') + 2:])
   if ((pz.index('_')) % int(len(pz) ** 0.5)) != 0: neighbors.append(pz[:pz.index('_') - 1] + '_' + pz[pz.index('_') - 1] + pz[pz.index('_') + 1:])
   if pz.index('_') >= int(len(pz) ** 0.5): neighbors.append(pz[:pz.index('_') - int(len(pz) ** 0.5)] + '_' + pz[pz.index('_') - int(len(pz) ** 0.5)+1:pz.index('_')] + pz[pz.index('_') - int(len(pz) ** 0.5)] + pz[pz.index('_')+1:])
   if pz.index('_') + int(len(pz) ** 0.5) < len(pz): neighbors.append(pz[:pz.index('_')] + pz[pz.index('_') + int(len(pz) ** 0.5)] + pz[pz.index('_') + 1:pz.index('_') + int(len(pz) ** 0.5)] + '_' + pz[int(len(pz) ** 0.5) + pz.index('_') + 1:])
   return neighbors

def constructPath(pz, puz, dictSeen):
   path = []
   temp = puz
   while temp != pz:
      path.append(temp)
      temp = dictSeen.get(temp)
   path.append(temp)
   path = path[::-1]

   for i in range(0, len(path)):
      parts = [path[i][k:k+int(len(path[i])**0.5)] for k in range(0, len(path[i]), int(len(path[i])**0.5))]
      path[i] = "\n".join(parts)

   return path

def isSolvable(pz, goal):
   if (int(len(pz) **0.5) % 2 != 0):
      puz = pz.replace("_","")
      gool = goal.replace("_","")

      pzCount = 0
      for i in range(len(puz)-1):
         for j in range(i+1,len(puz)):
            if puz[i] > puz[j]:
               pzCount += 1
      goalCount = 0
      for i in range(len(gool)-1):
         for j in range(i+1,len(gool)):
            if gool[i] > gool[j]:
               goalCount += 1
      return (pzCount % 2 == goalCount % 2)
   else: return True

def shortestPath(pz, goal):
   itmI = 0
   if isSolvable(pz, goal):
      # if pz == goal: finishAndExit(pz, "done", None, None); return [pz]
      if pz == goal: finishAndExit(pz, "done", None, None)
      parseMe = [pz]
      dictSeen = {pz:""}
      while parseMe:
         itm = parseMe[itmI]
         itmI+=1
         for puz in getNeighbors(itm): 
            if not (puz in dictSeen):
               dictSeen.update({puz:itm})
               # if puz == goal: finishAndExit(pz, dictSeen, itm, puz); return
               if puz == goal: return (pz, dictSeen, itm, puz)
               parseMe.append(puz)
   # else: return finishAndExit(pz, "None", None, None)
   else: return (pz, "None", None, None)

def finishAndExit(pz, dictSeen, itm, puz):
   if (dictSeen == "None"):
      for i in range(0, len(pz), int(len(pz)**0.5)):
         print(pz[i:i+int(len(pz)**0.5)])
      print("Steps: -1")
      print(f"Time: {round(time.time()-startTime, 2)} s")
   elif (dictSeen == "done"):
      for i in range(0, len(pz), int(len(pz)**0.5)):
         print(pz[i:i+int(len(pz)**0.5)])
      print("Steps: 0")
      print(f"Time: {round(time.time()-startTime, 2)} s")
   else:
      path = constructPath(pz, puz, dictSeen)
      
      joined = [puzzle.split("\n") for puzzle in path]
      joinedSep = []
      for i in range(0,len(joined),5):
         curr = []
         if (i == len(joined)):
            break
         else:
            for k in range(5):
               if (not(i+k >= len(joined))):
                  curr.append(joined[i+k])
         joinedSep.append(curr)
      for joins in joinedSep:
         puzzles = zip(*joins)
         for i, puzzle in enumerate(puzzles):
            print(" ".join(puzzle))
      print(f"Steps: {len(joined)-1}")
      print(f"Time: {round(time.time()-startTime, 2)} s")

def evaluateLab():
   chars = ["1","2","3","4","5","6","7","8","_"]
   numOfSolvable = 0
   totalPathLen = 0
   for i in range(500):
      random.shuffle(chars)
      pz = "".join(chars)
      random.shuffle(chars)
      goal = "".join(chars)
      argsFinished = shortestPath(pz, goal)
      if argsFinished[1] != "None":
         numOfSolvable += 1
         if argsFinished[1] == "done": totalPathLen += 1
         else:
            path = constructPath(argsFinished[0], argsFinished[3], argsFinished[1])
            joined = [puzzle.split("\n") for puzzle in path]
            totalPathLen += len(joined)
   print(f"Time: {round(time.time()-startTime, 2)} s")
   print(f"Number of impossible: " + str(500-numOfSolvable))
   print("Number of total puzzles: 500")
   print(f"Average path length of solvable puzzles: " + str(totalPathLen / numOfSolvable))

startTime = time.time()
if len(args) > 1: finishedArgs = shortestPath(args[0], args[1]); finishAndExit(finishedArgs[0],finishedArgs[1],finishedArgs[2],finishedArgs[3])
elif len(args) == 1: finishedArgs = shortestPath(args[0], '12345678_'); finishAndExit(finishedArgs[0],finishedArgs[1],finishedArgs[2],finishedArgs[3])
else: evaluateLab()

# Zachary Baker, Pd. 4, 2024
import sys; args = sys.argv[1:]
# import cProfile
# import pprofile

def condensePath(lstPzl):
   path = []
   if len(lstPzl) == 0:
      path.append("X")
   elif len(lstPzl) == 1:
      path.append("G")
   else:
      for i in range(len(lstPzl)-1):
         intI = lstPzl[i].index("_")
         finI = lstPzl[i+1].index("_")
         if (finI == intI+1):
            path.append("R")
         elif (finI+1 == intI):
            path.append("L")
         elif (finI > intI):
            path.append("D")
         else:
            path.append("U")
   return "".join(path)

def swap(list, i1, i2):
   temp = list[i1]
   list[i1] = list[i2]
   list[i2] = temp
   return list

def getNeighbors(pz):
   getNeighbors = []
   uIndex = pz.index("_")
   if ((uIndex + 1) % totPzLen) != 0: getNeighbors.append((pz[:uIndex] + pz[uIndex + 1] + '_' + pz[uIndex + 2:], uIndex))
   if ((uIndex) % totPzLen) != 0: getNeighbors.append((pz[:uIndex - 1] + '_' + pz[uIndex - 1] + pz[uIndex + 1:], uIndex))
   if uIndex >= totPzLen: getNeighbors.append((pz[:uIndex - totPzLen] + '_' + pz[uIndex - totPzLen+1:uIndex] + pz[uIndex - totPzLen] + pz[uIndex+1:], uIndex))
   if uIndex + totPzLen < len(pz): getNeighbors.append((pz[:uIndex] + pz[uIndex + totPzLen] + pz[uIndex + 1:uIndex + totPzLen] + '_' + pz[totPzLen + uIndex + 1:], uIndex))
   return getNeighbors

def constructPath(pz, puz, dictSeen):
   path = []
   if len(dictSeen) == 0:
      return path
   temp = puz
   while temp != pz:
      path.append(temp)
      temp = (dictSeen.get(temp))[1]
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
      goalCount = 0
      for i in range(len(puz)-1):
         for j in range(i+1,len(puz)):
            if puz[i] > puz[j]:
               pzCount += 1
            if gool[i] > gool[j]:
               goalCount += 1
      return (pzCount % 2 == goalCount % 2)
   else: 
      uIndex = pz.index("_")
      lvlPz = (uIndex // totPzLen) + 1

      uIndex = goal.index("_")
      lvlGoal = (uIndex // totPzLen) + 1

      puz = pz.replace("_","")
      gool = goal.replace("_","")

      pzCount = 0
      goalCount = 0

      for i in range(len(puz)-1):
         for j in range(i+1,len(puz)):
            if puz[i] > puz[j]:
               pzCount += 1
            if gool[i] > gool[j]:
               goalCount += 1

      goalTot = lvlGoal + goalCount
      pzTot = lvlPz + pzCount
      return (goalTot % 2 == pzTot % 2)

def initialH(pz, goal):
   manDist = 0
   for i, n in enumerate(pz):
      if n != "_":
         index = i
         goalI = goal.index(n)
         indexyx = divmod(index, totPzLen)
         goalyx = divmod(goalI, totPzLen)
         manDist += abs(goalyx[0] - indexyx[0]) + abs(goalyx[1] - indexyx[1])
   return int(manDist)

def newH(pz, neigh, nci):
   pzI = pz.index(neigh[nci])
   goalI = goal.index(neigh[nci])

   indexyx = divmod(pzI, totPzLen)
   goalyx = divmod(goalI, totPzLen)
   manDist = abs(goalyx[0] - indexyx[0]) + abs(goalyx[1] - indexyx[1])

   indexyx2 = divmod(nci, totPzLen)
   goalyx2 = divmod(goalI, totPzLen)
   manDist2 = abs(goalyx2[0] - indexyx2[0]) + abs(goalyx2[1] - indexyx2[1])

   if manDist2 > manDist: return 1
   else: return -1
   
def astar(pz, goal):
   if isSolvable(pz, goal):
      openset = [[] for x in range(55)]
      initH = initialH(pz, goal) * 1.01
      openset[int(initH-1)].append((pz, initH, 0, ""))
      closeset = {}
      while len(openset) > 0:
         currPzl = ""
         bucketI = 0
         for i, bucket in enumerate(openset):
            if len(bucket) > 0:
               print(i == 0)
               bucketI = i
               currPzl = openset[bucketI].pop()
               break
         if currPzl[0] in closeset: continue

         closeset[currPzl[0]] = (currPzl[2], currPzl[3])
         if currPzl[0] == goal: 
            return closeset
         for nbr in getNeighbors(currPzl[0]):
            neigh = nbr[0]
            if neigh in closeset: continue
            inc = (int(newH(currPzl[0], neigh, nbr[1])) + int(currPzl[1])) * 1.01
            # inc = int(initialH(neigh, goal)) * 1.01
            lvl = currPzl[2] + 1
            f = lvl + inc
            openset[int(f-1)].append((neigh, inc, lvl, currPzl[0]))
   else: return {}

with open(args[0]) as f:
   puzzles = [line.strip() for line in f]
   goal = puzzles[0]
   totPzLen = int(len(goal) ** 0.5)

for puz in puzzles:
   # pr = cProfile.Profile()
   # pr.enable()
   # profiler = pprofile.Profile()
   # with profiler:
   dictSeen = astar(puz, goal)
   # profiler.print_stats()
   # pr.disable()
   # pr.print_stats()
   path = constructPath(puz, goal, dictSeen)
   print(f"{puz} {condensePath(path)}")

#cleanup code, eliminate duplicate computations (h())
# Zachary Baker, Pd. 4, 2024
import sys; args = sys.argv[1:]

dim = int(args[0])
startPzl = "".join(["." for i in range (int(dim)*int(dim))])
seen = []

def isInvalid(pzl):
   for k in range (1,8):
      queenRows = []
      queenCols = []
      queenCords = []
      for i in range (len(pzl)):
         if pzl[i] == str(k):
            queenRows.append(i//dim)
            queenCols.append(i%dim)
            queenCords.append((i//dim, i%dim))
      qRs = {*queenRows}
      qCs = {*queenCols}
      for cord1 in (queenCords):
         for cord2 in (queenCords):
            if cord1 != cord2:
               if (cord1[0] + abs(cord2[1] - cord1[1]) == cord2[0]): return True
      if len(queenRows) != len(qRs) or len(queenCols) != len(qCs): return True
   return False

def isFinished(pzl):
   return pzl.count(".") == 0

def bruteForce(pzl):
   if isInvalid(pzl): return ""
   if isFinished(pzl): return pzl
   subPzl = pzl
   dotI = subPzl.index(".")
   listPzl = list(subPzl)
   for k in range(1,8):
      listPzl[dotI] = str(k)
      subPzl = "".join(listPzl)
      if not (subPzl in seen):
         seen.append(subPzl)
         bF = bruteForce(subPzl)
         if bF: return bF

print(bruteForce(startPzl))
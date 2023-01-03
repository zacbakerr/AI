#           0
#         1   2
#       3   4   5
#     6   7   8   9
#   10  11  12  13  14
# 15  16  17  18  19  20

l = [[0,1,3],[1,3,6],[3,6,10],[6,10,15],[2,4,7],[4,7,11],[7,11,16],[5,8,12],[8,12,17],[9,13,18]]
r = [[0,2,5],[2,5,9],[5,9,14],[9,14,20],[1,4,8],[4,8,13],[8,13,19],[3,7,12],[7,12,18],[6,11,17]]
a = [[3,4,5],[6,7,8],[7,8,9],[10,11,12],[11,12,13],[12,13,14],[15,16,17],[16,17,18],[17,18,19],[18,19,20]]
constraintSets = l + r + a

indexLookUpTable = dict()
for i in range(21): indexLookUpTable[i] = []

for cset in constraintSets:
   for c in cset:
      indexLookUpTable[c].append(cset)

pzl = "||||.||||||||||||||||"
closetset = dict()

def isInvalid(pzl):
   for cset in constraintSets:
      if (pzl[cset[0]] == "|" and pzl[cset[1]] == "|" and pzl[cset[2]] == ".") or (pzl[cset[2]] == "|" and pzl[cset[1]] == "|" and pzl[cset[0]] == "."):
         return False
   return True

def bruteForce(pzl, pzlCount,closedset):
   if isInvalid(pzl): return ""
   if pzl.count("|") == 1: return pzl
   for cset in constraintSets:
      if (pzl[cset[0]] == "|" and pzl[cset[1]] == "|" and pzl[cset[2]] == "."):
         subpzl = list(pzl)
         subpzl[cset[0]] = "."
         subpzl[cset[1]] = "."
         subpzl[cset[2]] = "|"
         subpzl = "".join(subpzl)
         closedset[subpzl] = pzl
         if subpzl.count("|") == 1: return subpzl, closedset
         bf = (bruteForce(subpzl, pzlCount+1,{s:p for s,p in closedset.items()}))
         if bf: return bf
      elif (pzl[cset[2]] == "|" and pzl[cset[1]] == "|" and pzl[cset[0]] == "."):
         subpzl = list(pzl)
         subpzl[cset[2]] = "."
         subpzl[cset[1]] = "."
         subpzl[cset[0]] = "|"
         subpzl = "".join(subpzl)
         closedset[subpzl] = pzl
         if subpzl.count("|") == 1: return subpzl, closedset
         bf = (bruteForce(subpzl,pzlCount+1,{s:p for s,p in closedset.items()}))
         if bf: return bf

def printPath(pzl, finishedPzl, closedSet):
   path = []
   temp = finishedPzl
   while temp != pzl:
      path.append(temp)
      temp = closedSet.get(temp)
   path.append(temp)
   path = path[::-1]
   for p in path:
      print(p)

output = bruteForce(pzl,0,closetset)
(printPath(pzl, output[0], output[1]))
   
print(output[0])

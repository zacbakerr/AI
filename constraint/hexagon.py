import sys; args = sys.argv[1:]
startPzl = "".join(["." for i in range(24)])

hexIs = [[0,1,2,6,7,8],[2,3,4,8,9,10],[5,6,7,12,13,14],[7,8,9,14,15,16],[9,10,11,16,17,18],[13,14,15,19,20,21],[15,16,17,21,22,23]]
rowIs = [[0,1,2,3,4],[5,6,7,8,9,10,11],[12,13,14,15,16,17,18],[19,20,21,22,23],[1,0,6,5,12],[3,2,8,7,14,13,19],[4,10,9,15,16,20,21],[11,18,17,22,23],[5,12,13,19,20],[0,6,7,14,15,21,22],[1,2,8,9,16,17,23],[3,4,10,11,18]]
seen = []

def isInvalid2(pzl):
   for hex in hexIs:
      nums = []
      for i in hex:
         temp = pzl[i]
         if temp != ".":
            nums.append(temp)
      if len(nums) != len(set(nums)): return True
   for hex in rowIs:
      nums = []
      for i in hex:
         temp = pzl[i]
         if temp != ".":
            nums.append(temp)
      if len(nums) != len(set(nums)): return True
   return False

def isInvalid(pzl):
   for hex in hexIs:
      nums = []
      for i in hex:
         temp = pzl[i]
         if temp != ".":
            nums.append(temp)
      if len(nums) != len(set(nums)): return True
   return False

def isFinished(pzl):
   return pzl.count(".") == 0

def bruteForce(pzl):
   if isInvalid2(pzl): return ""
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
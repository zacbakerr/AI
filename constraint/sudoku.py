import sys; args = sys.argv[1:]
import time
# import pprofile

with open(args[0]) as f:
   puzzles = [(line.strip()) for line in f]
   
def setGlobals(pzl):
   global seen; global width; global charSet; global constraintSets
   global indicesConstraints
   seen = []; charSet = set(); width = int(len(pzl) ** 0.5); 
   indicesConstraints = dict()
   for char in pzl: charSet.add(char)
   charSet.remove(".")
   charAdds = "123456789abcdefghij"
   counter = 0
   while len(charSet) < width: 
      while (charAdds[counter] in charSet):
         counter += 1
      charSet.add(charAdds[counter])
   for i in range(len(pzl)): 
      indicesConstraints[i] = []
   rows = [{i+k for k in range(width)} for i in range(0,len(pzl),width)]
   cols = [{i+k for k in range(0,len(pzl),width)} for i in range(width)]
   subs = [{k*width+l for k in range(j, j+int(width**.5)) for l in range(i, i+(width//int(width**.5)))} for i in range(0, width, (width//int(width**.5))) for j in range(0, width, int(width ** .5))]
   constraintSets = rows + cols + subs
   for cset in constraintSets:
      for c in cset:
         indicesConstraints[c].append(cset)

   global nbrs
   nbrs = [set().union(*indicesConstraints[i]) for i in range(len(pzl))]
   global periodNbrs
   periodNbrs = [{i for i in nbrs[pos] if pzl[i] == "."} for pos in range(len(pzl))]

   global possibleChars
   possibleChars = {pos:charSet-{pzl[i] for i in nbrs[pos]} for pos in range(len(pzl)) if pzl[pos] == "."}

   global buckets
   buckets = [[] for i in range(10)]
   for pos, value in possibleChars.items():
      buckets[len(value)].append(pos)

   # global symPos
   # symPos = dict()
   # for cset in constraintSets:
   #    toPlace = charSet-{pzl[i] for i in cset}-{"."}
   #    pers = {i for i in range(len(pzl)) if pzl[i] == "."}
   #    for c in toPlace:
   #       positions = set()
   #       for p in pers:
   #          if not (c in {pzl[i] for i in nbrs[p]}): positions.add(p)
   #       if c in symPos and len(positions) < len(symPos[c]): symPos[c] = positions
   #       elif not (c in symPos): symPos[c] = positions

   # global buckets2
   # buckets2 = [[] for i in range(100)]
   # for pos, value in symPos.items():
   #    buckets2[len(value)].append(pos)

def isFinished(pzl):
   return pzl.count(".") == 0

def getChoices(pzl, index, perLookup, iBuckets):
   if index != "None":
      for i in periodNbrs[index]:
         if pzl[i] == ".":
            temp = perLookup[i]
            if pzl[index] in temp:
               iBuckets[len(temp)].remove(i)
               temp.remove(pzl[(index)])
               iBuckets[len(temp)].append(i)
      if index in perLookup: 
         iBuckets[len(perLookup[index])].remove(index)
         del perLookup[index]
      for bucket in iBuckets:
         if len(bucket) > 0:
            return perLookup[bucket[0]], bucket[0]
   minV = 999
   minI = 0
   returnSet = 0
   for pos, set in perLookup.items():
      if len(set) <= 1: return perLookup[pos], pos
      if len(set) < minV: minV = len(set); minI = pos; returnSet = set
   return returnSet, minI

# def getChoices2(pzl, index, symsPos, iBuckets2):
#    if index != "None":
#       for i in nbrs[index]:
#          if pzl[i] in symsPos: 
#             if pzl[index] in symsPos[pzl[i]]:
#                iBuckets2[len(symsPos[pzl[i]])].remove(i)
#                symsPos[pzl[i]].remove(pzl[index])
#                iBuckets2[len(symsPos[pzl[i]])].append(i)
#       for bucket in iBuckets2:
#          if len(bucket) > 0:
#             return bucket[0], symsPos[bucket[0]]
#    choicesL = 999
#    choices = 0
#    char = 0
#    for c, it in symsPos.items():
#       if len(it) == 1: return c, it
#       if len(it) < choicesL: choicesL = len(it); char = c; choices = it
#    return char, choices

def bruteForce(pzl, index, perLookup, iBuckets):
   if isFinished(pzl): return pzl
   choices = getChoices(pzl, index, perLookup, iBuckets)
   choiceSet = choices[0]; changedI = choices[1]
   for i, c in enumerate(choiceSet):
      subPzl = pzl[:changedI] + c + pzl[changedI+1:]
      if i < (len(choiceSet)-1): bF = bruteForce(subPzl, changedI, {pos:{*perLookup[pos]} for pos in perLookup}, [[*bucket] for bucket in iBuckets])
      else: bF = bruteForce(subPzl, changedI, perLookup, iBuckets)
      if bF: return bF

startF = time.time()
for i, puz in enumerate(puzzles):
   setGlobals(puz)
   print(str(i+1) + ": " + puz)
   start = time.time()
   startI = ""
   endPuz = bruteForce(puzzles[i], "None", possibleChars, buckets)
   end = time.time() - start
   spaces = "".join(" " for i in range(len(str(i+1))))
   checksum = 0
   minChar = 999999
   for char in endPuz:
      if ord(char) < minChar: minChar = ord(char)
      checksum += ord(char)
   checksum -= (minChar*len(endPuz))
   print("  " + spaces + (endPuz) + " " + str(checksum) + " " + str(round(end, 5)) + "s")
print(f"Total time: {round(time.time()-startF, 5)}s")

# Zachary Baker, Pd. 4, 2024
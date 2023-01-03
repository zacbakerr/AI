import sys; args = sys.argv[1:]
import time; start = time.time()
import pprofile

newArgs = []
for a in args:
   newA = ""
   if "X" in a: newA = a.replace("X", "x")
   else: newA = a
   newArgs.append(newA)

i = 0; rect = ""; blocks = []
if "x" in newArgs[0]: rect += newArgs[0]; i += 1
else: rect += newArgs[0] + "x" + newArgs[1]; i += 2
while i < len(newArgs):
   if "x" in newArgs[i]: blocks.append(newArgs[i]); i += 1
   else: blocks.append(newArgs[i]+"x"+newArgs[i+1]); i += 2

pzl = [["" for i in range(int(rect.split("x")[1]))] for j in range(int(rect.split("x")[0]))]

def combinations(lst, pzl):
   maxV = 0
   maxT = ""
   for b in blocks:
      if int(b.split("x")[0]) * int(b.split("x")[1]) > maxV: maxV = int(b.split("x")[0]) * int(b.split("x")[1]); maxT = b
   maxT2 = maxT.split("x")[1] + "x" + maxT.split("x")[0]
   maxV = 0
   maxT3 = ""
   for b in blocks:
      if int(b.split("x")[0]) * int(b.split("x")[1]) > maxV and b != maxT: maxV = int(b.split("x")[0]) * int(b.split("x")[1]); maxT3 = b
   maxT22 = maxT3.split("x")[1] + "x" + maxT3.split("x")[0]
   indexs = []
   for i in range(len(lst)):
      for j in range(len(lst)-i):
         temp = []
         for k in range(j-i, j+1):
            temp.append(k+i)
         indexs.append(temp)
   combs = [[]]
   for y in range(len(lst)):
      newCombs = []
      for comb in combs:
         for z in range(len(comb) + 1):
            blockList = comb[:z] + [lst[y]] + comb[z:]
            if y == len(lst) - 1 and (blockList[0] == maxT):
            #if False:
               for new in indexs:
                  newComb = []
                  newComb = [n for n in blockList]
                  for i in new:
                     newComb[i] = blockList[i].split("x")[1] + "x" + blockList[i].split("x")[0]
                  for i, block in enumerate(newComb):
                     th = int(block.split("x")[0])
                     tw = int(block.split("x")[1])
                     placed = False
                     for h in range(len(pzl)):
                        for w in range(len(pzl[h])):
                           if pzl[h][w] == "" and h+th <= len(pzl) and w+tw <= len(pzl[h]):
                              yn = True
                              for l in range(h, h+int(th)):
                                 for m in range(w, w+int(tw)):
                                    if pzl[l][m] != "": 
                                       yn = False
                                       break
                                    else:
                                       pzl[l][m] == i
                                 if yn == False: 
                                    for i, p in enumerate(pzl):
                                       pzl[i] = p.replace(i, "")
                                    break
                              if yn:
                                 placed = True
                                 break
                        if placed: break
                  toP = True
                  temp = [i for j in pzl for i in j]
                  for i in range(len(blocks)):
                     if not (i in temp): toP = False; break
                  if toP:
                     return pzl, newComb
                  pzl = [["" for i in range(int(rect.split("x")[1]))] for j in range(int(rect.split("x")[0]))]
            else:
               newCombs.append(blockList)
      combs = newCombs
   return combs, "None"

def blockSolver(combs, pzl):
   for comb in combs:
      for i, block in enumerate(comb):
         th = int(block.split("x")[0])
         tw = int(block.split("x")[1])
         placed = False
         for h in range(len(pzl)):
            for w in range(len(pzl[h])):
               if pzl[h][w] == "" and h+th <= len(pzl) and w+tw <= len(pzl[h]):
                  yn = True
                  for l in range(h, h+int(th)):
                     for m in range(w, w+int(tw)):
                        if pzl[l][m] != "": yn = False
                  if yn:
                     for l in range(h, h+int(th)):
                        for m in range(w, w+int(tw)):
                           pzl[l][m] = i
                     placed = True
                     break
            if placed: break
      toP = True
      temp = [i for j in pzl for i in j]
      for i in range(len(blocks)):
         if not (i in temp): toP = False; break
      if toP:
         return pzl, comb
      pzl = [["" for i in range(int(rect.split("x")[1]))] for j in range(int(rect.split("x")[0]))]
   return "None", "None"

def decompose(sol):
   toPass = False
   temp = [i for j in sol[0] for i in j]
   blocksOrder = []
   for i, t in enumerate(temp):
      if t == "" and not (toPass):
         if temp[i-1] == "" or temp[i-int(rect.split("x")[1])] == "":
            continue
         else:
            height = 0
            width = 0
            temp2 = i
            while True:
               if temp2 < len(temp) and temp[temp2] == "": width += 1
               else: break
               temp2 += 1
            temp2 = i
            while True:
               if temp2 < len(temp) and temp[temp2] == "": height += 1
               else: break
               temp2 += int(rect.split("x")[1])
            blocksOrder.append(str(height) + "x" + str(width))
            toPass = True
      if toPass == False:
         if not (sol[1][t] in blocksOrder): 
            blocksOrder.append(sol[1][t])
      else:
         if not (t == ""): toPass = False
   print("Decomposition: " + ' '.join(blocksOrder))

profiler = pprofile.Profile()
with profiler:
   sol = combinations(blocks, pzl)
profiler.print_stats()
# for p in sol[0]:
#    print(p)
if sol[1] == "None": 
   pzl = [["" for i in range(int(rect.split("x")[1]))] for j in range(int(rect.split("x")[0]))]
   sol2 = blockSolver(sol[0], pzl)
   if sol2[0] == "None": print("No Solution")
   else:
      decompose(sol2)
else:
   decompose(sol)

print(f"Time: {time.time()-start}")

# Zachary Baker, Pd. 4, 2024
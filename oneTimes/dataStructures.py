import sys; args = sys.argv[1:]
from time import perf_counter; start = perf_counter()

with open(args[0]) as f:
   list1Lst = [int(line.strip()) for line in f]
   list1 = {*list1Lst}

with open(args[1]) as f:
   list2Lst = [int(line.strip()) for line in f]
   list2 = {*list2Lst}

with open(args[2]) as f:
   list3Lst = [line.strip() for line in f]
   list3 = {*list3Lst}

intersectionStartTime = perf_counter()
intersection = list1.intersection(list2)
print(f"#1: {len(intersection)}; {abs(round(intersectionStartTime-perf_counter(),2))}s\n")

hundrethUniquesStartTime = perf_counter()
uniqueSum = 0
uniqueCount = 0
for i in range(len(list1Lst)):
   if (list1Lst.index(list1Lst[i]) == i):
      uniqueCount += 1
      if (uniqueCount % 100 == 0):
         uniqueSum += int(list1Lst[i])
print(f"#2: {(uniqueSum)}; {abs(round(hundrethUniquesStartTime-perf_counter(),2))}s\n")

intersectionCount = perf_counter()
count = 0
for num in list3Lst:
   count += list1Lst.count(int(num))
   count += list2Lst.count(int(num))
print(f"#3: {(count)}; {abs(round(intersectionCount-perf_counter(),2))}\n")

smallestStartTime = perf_counter()
smalls = []
intSetList1 = {int(num) for num in list1}
for i in range(10):
   smalls.append(min(intSetList1))
   intSetList1.remove(smalls[i])
print(f"#4: {smalls}; {abs(round(smallestStartTime-perf_counter(),2))}s\n")

biggestStartTime = perf_counter()
bigs = []
for i in range(10):
   maxx = max(list2Lst)
   while list2Lst.count(maxx) < 2:
      list2Lst.remove(maxx)
      maxx = max(list2Lst)
   bigs.append(int(maxx))
   list2Lst = [i for i in list2Lst if i != maxx]
print(f"#5: {bigs}; {abs(round(biggestStartTime-perf_counter(),2))}s\n")

multiplesStartTime = perf_counter()
heap = []
count = []
for num in list1Lst:
   num = int(num)
   heap.append(num)
   if num % 53 == 0:
      heap.sort()
      min = heap.pop(0)
      while min in count:
         min = heap.pop(0)
      count.append(min)
print(f"#6: {sum(count)}; {abs(round(multiplesStartTime-perf_counter(),2))}s\n")

print(f"Total time: {round(perf_counter()-start, 2)}s")

# Zachary Baker, Pd. 4, 2024
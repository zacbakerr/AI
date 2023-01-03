lookup = {}

def neighbors(s):
    n=[]; i = s.find('_')
    if i in lookup:
        for p in lookup[i]:
            n.append(swap(s,i,p))
    else:
        temp = []
        if i % 3 < 3-1: 
            n.append(swap(s, i, i+1))
            temp.append(i+1)
        if i % 3 > 0: 
            n.append(swap(s, i-1, i))
            temp.append(i-1)
        if i >= 3: 
            n.append(swap(s, i-3, i))
            temp.append(i-3)
        if i < 3 **2 - 3: 
            n.append(swap(s, i, i+3))
            temp.append(i+3)
        lookup[i] = temp
    return n

def swap(s, l, r):
    st = [*s]
    temp = st[l]
    st[l] = st[r]
    st[r] = temp
    return ''.join(st)

seenPuzzles = []
startingPuzzle = "123_45678"
seenPuzzles.append(startingPuzzle)
levels = {0:[startingPuzzle]}

while True:
   currLevel = len(levels)
   if (len(levels[currLevel-1])) == 0:
      break
   levels[currLevel] = []
   for pz in levels[currLevel-1]:
      if (pz in [i for list in levels for i in list]):
        neighs = neighbors(pz)
        for n in neighs:
            if not (n in seenPuzzles):
                seenPuzzles.append(n)
                levels[currLevel].append(n)
   print(f"level: {currLevel}, numofn: {len(levels[currLevel])}")
            
   
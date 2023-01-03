from ast import parse


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
parseMe = []
startingPuzzle = "1_2345678"
seenPuzzles.append(startingPuzzle)
parseMe.append(startingPuzzle)
itmI = 0
twotonob, otoob, nototwob, threetonob, twotoob, ototwob, notothreeb, fourtonob, threetoob, twototwob, otothreeb, notofourb = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

print(twotonob, otoob)
while itmI < len(parseMe):
   itm = parseMe[itmI]
   itmI+=1
   neighs = neighbors(itm)
   seen = 0
   unseen = 0
   for n in neighs:
      if n in seenPuzzles:
         seen += 1
      else:
         unseen += 1
         seenPuzzles.append(n)
         parseMe.append(n)
   if seen == 0:
      if unseen == 2:
         nototwob += 1
      elif unseen == 3:
         notothreeb += 1
      elif unseen == 4:
         notofourb += 1
   if seen == 1:
      if unseen == 1:
         otoob += 1
      elif unseen == 2:
         ototwob += 1
      elif unseen == 3:
         otothreeb += 1
   if seen == 2:
      if unseen == 0:
         twotonob += 1
      elif unseen == 1:
         twotoob += 1
      elif unseen == 2:
         twototwob += 1
   if seen == 3:
      if unseen == 0:
         threetonob += 1
      elif unseen == 1:
         threetoob += 1
   if seen == 4:
      if unseen == 0:
         fourtonob += 1
   if itmI % 20000 == 0:
      print(twotonob, otoob, nototwob, threetonob, twotoob, ototwob, notothreeb, fourtonob, threetoob, twototwob, otothreeb, notofourb)

print(twotonob, otoob, nototwob, threetonob, twotoob, ototwob, notothreeb, fourtonob, threetoob, twototwob, otothreeb, notofourb)

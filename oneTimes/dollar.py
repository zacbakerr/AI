# def change(n, coinlist, coins):
#    if n == 0: return coins
#    count = list()
#    for coin in coinlist:
#       if (n-coin) >= 0: 
#         further = change(n-coin,coinlist, coins + [coin])
#         if len(further) > 1 and not ((further[0]) in coinlist) and len(further[0]) > 1 and not ((further[0][0]) in coinlist):
#            count = count + further
#         else:
#            count.append(further)
#    temp = count[::-1]
#    while len(temp) > 0 and len(temp) < 2:
#       temp = temp[0]
#    return temp

# lists = []
# print(change(10,[100,50,25,10,5,1],list()))
# for l in change(10,[100,50,25,10,5,1],list()):
#    if not (l[0] in [1,5,10,25,50,100]):
#       for k in l:
#          yes = True
#          for i in range(len(k)):
#             if i > 0 and (k[i] > k[i-1]): yes = False
#          if yes == True: lists.append(k)
#          else: yes = True
#    else:
#       yes = True
#       for i in range(len(l)):
#          if i > 0 and l[i] > l[i-1]: yes = False
#       if yes == True: lists.append(l)
#       else: yes = True

# print(len(lists))

import sys
sys.setrecursionlimit(100000)
key = (n,*coinlist)
if key not in CACHE:
   CACHE[key] = recurse
return CAHCE[key]
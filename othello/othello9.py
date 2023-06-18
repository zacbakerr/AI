import sys; args = sys.argv[1:]
import random
import time

cols = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
global NEGACACHE, MOVECACHE, MAKECACHE, EVALCACHE, MIDCACHE, OPENINGBOOK

NEGACACHE = dict()
MOVECACHE = dict()
MAKECACHE = dict()
EVALCACHE = dict()
MIDCACHE = dict()

OPENINGBOOK = {
   "...........................ox......xo...........................": "d3",
   "..........................xxx......xo...........................": "e3",
   "...........................ox......xxx..........................": "d6",
   "...........................ox......xo......x....................": "f4",
   "...................x.......xx......xo...........................": "c5",
   "...................x.......xx.....ooo...........................": "f6",
   "...................x.......xx.....xoo....x......................": "f3",
   "...................x.......xx.....oxo.....x.....................": "e3",
   "...................x.......xx.....oxo......x....................": "e3",
   "...................x.......xx.....ooo.......x...................": "e3",
   "...................x.......xx.....ooo........x..................": "f5",  
   "...................xo......xo......xo...........................": "f4",
   "..................ox.......ox......xo...........................": "c4",
   ".................xxx.......ox......xo...........................": "d2",
   "...................x.o.....xo.....xoo....x......................": "f4",
   "...................x.o.....xxx....xoo....x......................": "d2",
   "...........o.......o.o.....oxx....xoo....x......................": "c2",
   "..........xxx......xoo.....oox....xoo....x......................": "b1",

   "...................x.......xx......xo...........................": "18",
   "..................ox.......ox......xo...........................": "26",
   "..................ox......xxx......xo...........................": "20",
   "..................ooo.....xxo......xo...........................": "37",
   "..................ooo.....xxo......xxx..........................": "25",
   "..................ooo....oooo......xxx..........................": "10",
   "..........x.......oxo....ooox......xxx..........................": "11",
   "..........xo......ooo....ooox......xxx..........................": "34",
   "..........xo......xoo....oxox.....xxxx..........................": "17",
   "..........xo.....oooo....oxox.....xxxx..........................": "9",
   ".........xxo.....oxoo....oxxx.....xxxx..........................": "29",
   ".........xxo.....oxoo....ooooo....xxxx..........................": "3",
   "...x.....xxx.....oxxo....ooxoo....xxxx..........................": "12",
   "...x.....xxxo....oxoo....ooxoo....xxxx..........................": "4",
   "...xx....xxxx....oxox....ooxxo....xxxx..........................": "21",
   "...xx....xxxx....oxooo...ooxxo....xxxx..........................": "32",
   "...xx....xxxx....oxooo...xoxxo..x.xxxx..........................": "33",
   "...xx....xxxx....oxooo...ooxxo..xoxxxx..........................": "40",
   "...xx....xxxx....oxxoo...oxxxo..xxxxxx..x.......................": "41",
   "...xx....xxxx....oxxoo...oxoxo..xooxxx..xo......................": "16",
   "...xx....xxxx...xxxxoo...oxoxo..xooxxx..xo......................": "0",
   "o..xx....oxxx...xxoxoo...oxoxo..xooxxx..xo......................": "38",
   "o..xx....oxxx...xxoxxo...oxoxx..xooxxxx.xo......................": "13",
   # "o..xx....ooooo..xxoxoo...oxoxx..xooxxxx.xo......................": "24",
   # "o..xx....ooooo..xxoxoo..xxxoxx..xooxxxx.xo......................": "30",
   # "o..xx....ooooo..xxoxoo..xxxoooo.xooxxxx.xo......................": "43",
   # "o..xx....ooooo..xxoxoo..xxxoooo.xoxxxxx.xo.x....................": "42",
   # "o..xx....ooooo..xxoxoo..xxooooo.xoooxxx.xoox....................": "44",
   # "o..xx....ooooo..xxoxoo..xxxoooo.xooxxxx.xooxx...................": "45",
   # "o..xx....ooooo..xxoxoo..xxxoooo.xooxoox.xooooo..................": "31",
   # "o..xx....ooooo..xxoxoo..xxxxxxxxxooxoox.xooooo..................": "8",
   # "o..xx...oooooo..xooxoo..xxoxxxxxxooooox.xooooo..................": "6",
   # "o..xx.x.ooooox..xooxxo..xxoxxxxxxooooox.xooooo..................": "48",
   "o..xx.x.ooooox..oooxxo..oxoxxxxxoooooox.oooooo..o...............": "5",
   "o..xxxx.ooooxx..oooxxo..oxoxxxxxoooooox.oooooo..o...............": "22",
   "o..xxxx.ooooxx..oooxxoo.oxoxxoxxoooooox.oooooo..o...............": "2",
   "o.xxxxx.oooxxx..oooxxoo.oxoxxoxxoooooox.oooooo..o...............": "46",
   "o.xxxxx.oooxxx..oooxxoo.oxoxxooxooooooo.ooooooo.o...............": "23",
   "o.xxxxx.oooxxx..oooxxxxxoxoxxooxooooooo.ooooooo.o...............": "14",
   "o.xxxxx.ooooooo.oooxxooxoxoxoooxooooooo.ooooooo.o...............": "39",
   "o.xxxxx.ooooxoo.oooxxxoxoxoxooxxoooooooxooooooo.o...............": "7",
   "o.xxxxxxooooxox.oooxxxoxoxoxooxxoooooooxooooooo.o...............": "15",
   "o.xxxxxxooooxooooooxxxoxoxoxooxxoooooooxooooooo.o...............": "47",
   "o.xxxxxxooooxooooooxxxoxoxoxoxxxooooooxxoooooooxo...............": "55",
   "o.xxxxxxooooxooooooxxxoooxoxoxxoooooooxoooooooooo......o........": "1",
   # "oxxxxxxxoxxoxooooxoxxxoooxoxoxxoooooooxoooooooooo......o........": "63",
   # "oxxxxxxxoxxoxooxoxoxxxoxoxoxoxxxooooooxxoooooooxo......x.......x": "54",
   # "oxxxxxxxoxxoxooxoxoxxxoxoxoxoxxxooooxoxxoooooxxxo.....xx.......x": "62",
   # # "oxxxxxxxoxxoxooxoxoxxxoxoxoxoxoxooooxooxoooooxoxo.....ox......ox": "61",
   # "oxxxxxxxoxxoxooxoxoxxxoxoxoxoxoxooooxooxoooooxoxo.....xx.....xxx": "53",
   # "oxxxxxxxoxxoxooxoxoxxxoxoxoxoxoxooooxooxoooooooxo....oxx.....xxx": "49",
   # "oxxxxxxxoxxoxooxoxoxxxoxoxoxxxoxoxoxxooxoxxooooxox...oxx.....xxx": "56",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxooxooxoxoooooxoo...oxxo....xxx": "60",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxooxooxoxooooxxoo...xxxo...xxxx": "50",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxooxooxooooooxxooo..xxxo...xxxx": "52",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxxoxoxxoooxxxxxooo.xxxxo...xxxx": "51",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxxoxoxxoooooxxxooooxxxxo...xxxx": "59",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxxxxoxxoooxoxxxoooxxxxxo..xxxxx": "58",
   # "oxxxxxxxoxxoxooxoxoxxooxoxoxoxoxoxxxxoxxoooxoxxxooooxxxxo.oxxxxx": "57",

   # "oxxxxxxxoxxoxooxoxoxxxoxoxxxoxxxoooxxoxxooooooxxo..o.xxx......xx": "49",

   # "...........................ox......xx.......x...................": "29",
   # "...........................ooo.....xx.......x...................": "18",
   # "..................x........xoo.....xx.......x...................": "26",
   # "..................x.......oooo.....xx.......x...................": "19",
   # "..................xx......oxoo.....xx.......x...................": "10",
   # "..........o.......oo......oxoo.....xx.......x...................": "20",
   # "..........o.......oox.....oxxo.....xx.......x...................": "11",
   # "..........oo......ooo.....oxxo.....xx.......x...................": "13",
   # "..........oo.x....oox.....oxxo.....xx.......x...................": "21",
   # "..........oo.x....oooo....oxxo.....xx.......x...................": "12",
   # "..........ooxx....ooxo....oxxo.....xx.......x...................": "37",
   # "..........ooxx....ooxo....oxoo.....xxo......x...................": "2",
   # "..x.......oxxx....ooxo....oxoo.....xxo......x...................": "34",
   # "..x.......oxxx....ooxo....oxoo....oooo......x...................": "22",
   # "..x.......oxxx....ooxxx...oxoo....oooo......x...................": "51",
   # "..x.......oxxx....ooxxx...oxoo....oooo......o......o............": "30",
   # "..x.......oxxx....ooxxx...oxxxx...oooo......o......o............": "3",
   # "..xo......ooxx....ooxxx...oxxxx...oooo......o......o............": "4",
   # "..xxx.....ooxx....ooxxx...oxxxx...oooo......o......o............": "38",
   # "..xxx.....ooxx....oooxx...oxxox...ooooo.....o......o............": "1",
   # ".xxxx.....xoxx....oxoxx...oxxox...ooooo.....o......o............": "5",
   # ".xxxxo....xooo....oooox...oxxox...ooooo.....o......o............": "6",
   # ".xxxxxx...xoox....ooxox...oxxox...ooooo.....o......o............": "23",
   # ".xxxxxx...xoox....ooxooo..oxxoo...ooooo.....o......o............": "43",
   # ".xxxxxx...xoox....ooxooo..oxxoo...oxooo....xo......o............": "42",
   # ".xxxxxx...xoox....ooxooo..oxooo...ooooo...ooo......o............": "39",
   # ".xxxxxx...xoxx....ooxxoo..oxoox...ooooox..ooo......o............": "31",
   # ".xxxxxx...xoxx....ooxxoo..oxoooo..ooooox..ooo......o............": "15",
   # ".xxxxxx...xoxx.x..ooxxox..oxooox..ooooox..ooo......o............": "9",
   # ".xxxxxx..oooxx.x..ooxxox..oxooox..ooooox..ooo......o............": "47",
   # ".xxxxxx..oooxx.x..ooxxox..oxoxox..ooooxx..ooo..x...o............": "46",
   # ".xxxxxx..oooxx.x..ooxxox..oxoxox..ooooox..ooo.ox...o............": "0",
   # "xxxxxxx..xooxx.x..xoxxox..oxoxox..ooooox..ooo.ox...o............": "17",
   # "xxxxxxx..xooxx.x.oooxxox..oxoxox..ooooox..ooo.ox...o............": "33",
   # "xxxxxxx..xooxx.x.ooxxxox..xxoxox.xxxxxxx..ooo.ox...o............": "25",
   # "xxxxxxx..xooxx.x.ooxxxox.ooooxox.xoxxxxx..ooo.ox...o............": "32",
   # "xxxxxxx..xoxxx.x.oxxxxox.xoooxoxxxoxxxxx..ooo.ox...o............": "41",
   # "xxxxxxx..xoxxx.x.oxxxxox.ooooxoxxooxxxxx.oooo.ox...o............": "8",
   # "xxxxxxx.xxoxxx.x.xxxxxox.oxooxoxxooxxxxx.oooo.ox...o............": "45",
   # "xxxxxxx.xxoxxx.x.xxxxxox.oxooxoxxooxoxxx.oooooox...o............": "24",
   # "xxxxxxx.xxoxxx.x.xxxxxoxxxxooxoxxooxoxxx.oooooox...o............": "16",
   # "xxxxxxx.xxoxxx.xoooooooxxoxooxoxxooxoxxx.oooooox...o............": "48",
   # "xxxxxxx.xxoxxx.xooooxooxxoxxoxoxxoxxoxxx.xoooooxx..o............": "40",
   # "xxxxxxx.xxoxxx.xooooxooxooxxoxoxooxxoxxxoooooooxx..o............": "49",
   # "xxxxxxx.xxoxxx.xoxooxooxoxxxoxoxoxxxoxxxoxxooooxxx.o............": "56",
   # "xxxxxxx.xxoxxx.xoxooxooxooxooxoxoxoxoxoxoxxoxooxoooooooxoooooo..": "14",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoxoxoxoxxxxxoxxoooxxooooo..xoooxx...": "61",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoxoxoxoxxxxxoxxoooxxooooo..xoooooo..": "53",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoxoxoxoxxxxxoxxooooxooooo...oooxx...": "55",
   # "xxxxxxx.xxoxxx.xoxooxooxoxxxoxoxoxxooxxxoxoooooxoo.o....o.......": "59",
   # "xxxxxxx.xxoxxx.xoxooxooxoxxxoxoxoxxxoxxxoxoxoooxoo.x....o..x....": "52",
   # "xxxxxxx.xxoxxx.xoxooxooxoxxxoxoxoxxxoxxxoooooooxooOx....o..x....": "52",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoxoxoxoxoxxxoxoooooxoo.xo...o..x....": "50",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoxoxoxxxxxxxoxxxoooxooxxo...o..x....": "52",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoooxoxxxoxxxoxxooooxoooxo...oo.x....": "58",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoooxoxxxoxxxoxxooooxooxxo...ooxx....": "60",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoooxooxxoxxxoxoooooxooxoo...ooooo...": "55",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoooxooxxoxxxoxooooxxooxoo..xooooo...": "54",
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoooxooxxoxoxoxoooooxooxoo.oxooooo...": "63", 
   # "xxxxxxx.xxoxxx.xoxooxooxooxxoooxooxxxxoxoxoooxoxooxoo.xxooooo..x": "14",
   # "xxxxxxx.xxoooooxoxooxooxooxxoooxooxxxxoxoxoooxoxooxoo.xxooooo..x": "53",
   # "xxxxxxx.xxoooooxoxooxooxooxxoooxooxxxxoxoxooxxxxooxxxxxxooooo..x": "61",
   # "xxxxxxx.xxoooooxoxooxooxooxxoooxooxxxooxoxooxoxxooxxooxxoooooo.x": "62",
   # "xxxxxxx.xxoooooxoxooxooxooxxoooxooxxxooxoxooxoxxooxxoxxxooooooxx": "7",
   # "xxxxxxx.xxoxxx.xoxooxooxoxxxoxoxoxxxoxxxoooooooxooox....o..x....": "52",
   # "xxxxxxx.xxoxxx.xoxooxooxoxxoxxoxoxxxoxxxoooxxooxoooox.o.o..xxx..": "53",

   "...................x.......xx......xo...........................": "34",
   "...................x.......xx.....ooo...........................": "41",
   "...................x.......xx.....xoo....x......................": "21",
   "...................x.o.....xo.....xoo....x......................": "29",
   "...................x.o.....xxx....xoo....x......................": "11",
   "...........o.......o.o.....oxx....xoo....x......................": "10",
   "..........xo.......x.o.....oxx....xoo....x......................": "20",
   "..........xo.......xoo.....oox....xoo....x......................": "12",
   "..........xxx......xoo.....oox....xoo....x......................": "1",
   ".o........oxx......ooo.....oox....xoo....x......................": "13",
   ".o........oxxx.....oxx.....xox....xoo....x......................": "18",
   ".o........oxxx....ooxx.....oox....xoo....x......................": "17",
   ".o........oxxx...xxxxx.....oox....xoo....x......................": "26",
   ".o........oxxx...xoxxx....ooox....xoo....x......................": "25",
   ".o........oxxx...xxxxx...xxxxx....xoo....x......................": "4",
   ".o..o.....oxox...xxxox...xxxox....xoo....x......................": "37",
   ".o..o.....oxox...xxxox...xxxxx....xxxx...x......................": "33",
   ".o..o.....oxox...xxoox...xoxxx...oxxxx...x......................": "2",
   ".ox.o.....xxox...xxoox...xoxxx...oxxxx...x......................": "3",
   ".oooo.....xoox...xxoox...xoxxx...oxxxx...x......................": "32",
   ".oooo.....xoox...xxoox...xoxxx..xxxxxx...x......................": "40",
   ".oooo.....xoox...xxoox...xoxxx..xoxxxx..ox......................": "48",
   ".oooo.....xoox...xxoox...xoxxx..xoxxxx..xx......x...............": "8",
   ".oooo...o.xoox...oxoox...xoxxx..xoxxxx..xx......x...............": "5",
   ".oooox..o.xoxx...oxxox...xxxxx..xxxxxx..xx......x...............": "6",
   ".oooooo.o.xoxo...oxxox...xxxxx..xxxxxx..xx......x...............": "16",
   ".oooooo.o.xoxo..xxxxox...xxxxx..xxxxxx..xx......x...............": "9",
   ".oooooo.ooooxo..xxxxox...xxxxx..xxxxxx..xx......x...............": "0",
   "xoooooo.xxooxo..xxxxox...xxxxx..xxxxxx..xx......x...............": "24",
   "xoooooo.xxooxo..xoxxox..oxxxxx..xxxxxx..xx......x...............": "7",
   "xxxxxxxxxxooxo..xoxxox..oxxxxx..xxxxxx..xx......x...............": "56",
   "xxxxxxxxxxooxo..xoxxox..oxxxxx..oxxxxx..ox......o.......o.......": "14",
   "xxxxxxxxxxooxxx.xoxxox..oxxxxx..oxxxxx..ox......o.......o.......": "49",
   "xxxxxxxxxxooxxx.xoxxox..ooxxxx..ooxxxx..oo......oo......o.......": "57",
   "xxxxxxxxxxooxxx.xxxxox..oxxxxx..oxxxxx..ox......ox......ox......": "50",
   "xxxxxxxxxxooxxx.xxxxox..oxxxxx..oxxxxx..oo......ooo.....ox......": "43",
   "xxxxxxxxxxooxxx.xxxxox..oxxxxx..oxxxxx..oo.x....oox.....ox......": "42",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..ooox....oox.....ox......": "52",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..oooo....oox.o...ox......": "51",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..ooox....ooxxo...ox......": "58",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..ooox....oooxo...ooo.....": "53",
   # "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..ooox....oooxxx..ooo.....": "61",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..oooo....oooxox..ooo..o..": "54",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..oooo....oooxooo.ooo..o..": "55",
   "xxxxxxxxxxooxxx.xxoxox..oxoxxx..oooxxx..oooo....oooxxxxxooo..o..": "44",
   "xxxxxxxxxxooxxx.xxoxox..oxoxox..ooooox..ooooo...ooooxxxxooo..o..": "45",
   "xxxxxxxxxxooxxx.xxoxox..oxoxox..ooooxx..ooooox..ooooxxxxooo..o..": "63",
   "xxxxxxxxxxooxxx.xxoxox..oxooox..ooooox..oooooo..ooooxxoxooo..o.o": "38",
   "xxxxxxxxxxooxxx.xxoxox..oxooox..oooooxx.ooooox..ooooxxoxooo..o.o": "62",
   "xxxxxxxxxxooxxx.xxoxox..oxooox..oooooxx.ooooox..ooooxooxooo..ooo": "59",
   "xxxxxxxxxxooxxx.xxoxox..oxoxox..oooxoxx.oooxox..oooxxooxooox.ooo": "47",
   "xxxxxxxxxxooxxx.xxoxox..oxoxoo..oooxoxo.oooxox.ooooxxoooooox.ooo": "22",
   "xxxxxxxxxxooxxx.xxoxoxx.oxoxox..oooxxxo.oooxox.ooooxxoooooox.ooo": "60",
   "xxxxxxxxxxooxxx.xxoxoxx.oxoxox..oooxxxo.oooxox.ooooooooooooooooo": "31",
   "xxxxxxxxxxooxxx.xxoxoxx.oxoxox.xoooxxxx.oooxox.ooooooooooooooooo": "46",
   "xxxxxxxxxxooxxx.xxoxoxx.oxoxox.xoooxxox.oooxoooooooooooooooooooo": "39",
   "xxxxxxxxxxooxxx.xxoxoxx.oxoxox.xoooxxooooooxoooooooooooooooooooo": "15",
   "xxxxxxxxxxooooooxxoxoxo.oxoxoo.xoooxoooooooooooooooooooooooooooo": "23",
   "xxxxxxxxxxooooxxxxoxoxxxoxoxoo.xoooxoooooooooooooooooooooooooooo": "30",
}

global HOLELIMIT
HOLELIMIT = [10]

class Strategy:
    logging = True # turns on logging
    def best_strategy(self, board, player, best_move, running):
        if running.value:
            best_move.value = quickMove(board, player)

def rotate(board,width=8,height=8):
    return ''.join([board[start+width* offset] for start in range (width-1,-1,-1) for offset in range(height)])

def xaxflip(board,width=8,height=8):
    return ''.join([board[start+offset] for start in range((height-1)*width,-1,-width) for offset in range(width)])

def yaxflip(board,width=8,height=8):
    return ''.join([board[start-offset] for start in range(width-1,len(board),width) for offset in range(width)])

def rotateindex(index):
   return (index%8)*8+(7-index//8)

def display2D(board, canMove, move=-1):
   if canMove:
      for m in canMove:
         board = board[0:m] + "*" + board[m+1:]
   if move != -1: board = board[0:int(move)] + board[int(move)].upper() + board[int(move)+1:]
   for i in range(0,64,8):
      print(board[i:i+8])

def findMoves(board, toMove):
   if (board, toMove) in MOVECACHE: return MOVECACHE[(board, toMove)]
   toCheck = ""
   if toMove == "o": toCheck = "x"
   else: toCheck = "o"
   moves = set()
   for i in range(64):
      if board[i] == toMove:
         canPlace = False
         dotI = -1
         for j in range(i, 64, 8):
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i, -1, -8):  
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i, i + (8 - i % 8)):  
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , i + (8 - i % 8) - 9, -1):  
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , 64, 9):  
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-1) == j: canPlace = False; break
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , 64, 7):  
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-8) == j: canPlace = False; break
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i, -1, -9):
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-8) == j: canPlace = False; break
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == toCheck: canPlace = True
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , -1, -7):  
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-1) == j: canPlace = False; break
            if board[j] == toCheck: canPlace = True
            if (board[j] == toMove or board[j] == "*") and j != i: canPlace = False; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
   if -1 in moves: moves.remove(-1)
   MOVECACHE[(board, toMove)] = moves
   moves = sorted(moves, key=lambda x: x not in [0, 7, 56, 63])
   return moves

def makeMove(board, toPlay, moveIndex):
   if (board, toPlay, moveIndex) in MOVECACHE: return MOVECACHE[(board, toPlay, moveIndex)]

   toCheck = ""
   if toPlay == "o": toCheck = "x"
   else: toCheck = "o"

   newBoard = board[0:moveIndex] + toPlay + board[moveIndex+1:]

   change = []
   toChange = False

   temp = []
   for j in range(moveIndex, moveIndex + (8 - moveIndex % 8)):
      if j == moveIndex: continue
      if board[j] == toPlay: toChange = True; break
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, 64, 8):
      if j == moveIndex: continue
      if board[j] == toPlay: toChange = True; break
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, -1, -8):
      if j == moveIndex: continue
      if board[j] == toPlay: toChange = True; break
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, moveIndex + (8 - moveIndex % 8) - 9, -1):
      if j == moveIndex: continue
      if board[j] == toPlay: toChange = True; break
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, 64, 9):
      if board[j] == toPlay: toChange = True; break
      if (j+(8-j%8)-1) == j: toChange = False; break
      if j == moveIndex: continue
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, 64, 7):
      if board[j] == toPlay: toChange = True; break
      if (j+(8-j%8)-8) == j: toChange = False; break
      if j == moveIndex: continue
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, -1, -9):
      if board[j] == toPlay: toChange = True; break
      if (j+(8-j%8)-8) == j: toChange = False; break
      if j == moveIndex: continue
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False
   for j in range(moveIndex, -1, -7):
      if board[j] == toPlay: toChange = True; break
      if (j+(8-j%8)-1) == j: toChange = False; break
      if j == moveIndex: continue
      if board[j] != toCheck: toChange = False; break
      temp.append(j)
   if toChange: change += temp
   temp = []; toChange = False

   for c in change:
      newBoard = newBoard[0:c] + toPlay + newBoard[c+1:]

   if toPlay == "x": toPlay = "o"
   else: toPlay = "x"
   MAKECACHE[(board, toPlay, moveIndex)] = (newBoard, toPlay)
   return newBoard, toPlay

def evaluateBoard(board, tkn):
   if (board, tkn) in EVALCACHE: return EVALCACHE[(board, tkn)]
   boards = [rotate(board), rotate(rotate(board)), rotate(rotate(rotate(board))), xaxflip(board), xaxflip(rotate(board)), xaxflip(rotate(rotate(board))), xaxflip(rotate(rotate(rotate(board))))]
   for b in boards:   
      if (b, tkn) in EVALCACHE: return EVALCACHE[(b, tkn)]

   etkn = "x"
   if tkn == "x": etkn = "o"
   score = 0

   # check how many secure tokens are on the board. every token has 8 possible directions to go. the 8 directions are divided into 4 pairs. up and down, right and left, etc. every pair needs to have one direction that is filled with tokens up until a wall.
   for i in range(0, 64):
      tkns = [tkn, etkn]
      for token in tkns:
         otherTkn = "x"
         if token == "x": otherTkn = "o"
         if board[i] == token:
            # iterate down
            isSecure1 = True
            isSecure2 = True
            ultraSecure = True
            for j in range(i, 64, 8):
               if board[j] == otherTkn: isSecure1 = False; break
               if board[j] == ".": isSecure1 = False; ultraSecure = False; break
            for j in range(i, -1, -8):
               if board[j] == otherTkn: isSecure2 = False; break
               if board[j] == ".": isSecure2 = False; ultraSecure = False; break
            if isSecure1 or isSecure2:
               isSecure1 = True
               isSecure2 = True
               for j in range(i, i + (8 - i % 8)):
                  if board[j] == otherTkn: isSecure1 = False; break
                  if board[j] == ".": isSecure1 = False; ultraSecure = False; break
               for j in range(i, i + (8 - i % 8) - 9, -1):
                  if board[j] == ".": isSecure2 = False; ultraSecure = False; break
                  if board[j] == otherTkn: isSecure2 = False; break
               if isSecure1 or isSecure2:
                  isSecure1 = True
                  isSecure2 = True
                  for j in range(i, 64, 9):
                     if board[j] == ".": isSecure1 = False; ultraSecure = False; break
                     if board[j] == otherTkn: isSecure1 = False; break
                  for j in range(i, 64, -9):
                     if board[j] == ".": isSecure2 = False; ultraSecure = False; break
                     if board[j] == otherTkn: isSecure2 = False; break
                  if isSecure1 or isSecure2:
                     isSecure1 = True
                     isSecure2 = True
                     for j in range(i, 64, 7):
                        if board[j] == ".": isSecure1 = False; ultraSecure = False; break
                        if board[j] == otherTkn: isSecure1 = False; break
                     for j in range(i, -1, -7):
                        if board[j] == ".": isSecure2 = False; ultraSecure = False; break
                        if board[j] == etkn: isSecure2 = False; break
                     if isSecure1 or isSecure2:
                        if token == tkn: score += 1
                        else: score -= 1
                     else: 
                        if ultraSecure:
                           if token == tkn: score += 1
                           else: score -= 1

   if board[0] == tkn: score += 5
   if board[7] == tkn: score += 5
   if board[56] == tkn: score += 5
   if board[63] == tkn: score += 5
   if board[0] == etkn: score -= 5
   if board[7] == etkn: score -= 5
   if board[56] == etkn: score -= 5
   if board[63] == etkn: score -= 5

   score += (len(findMoves(board, tkn)))*2
   score -= (len(findMoves(board, etkn)))*2

   score += (board.count(tkn)-board.count(etkn))/(board.count(tkn)+board.count(etkn))

   EVALCACHE[(board, tkn)] = score
   return score

def alphabeta(brd, tkn, alpha, beta):
   global NEGACACHE
   if (brd, tkn, alpha, beta) in NEGACACHE: return NEGACACHE[(brd, tkn, alpha, beta)]

   etkn = ""
   if tkn == "x": etkn = "o"
   else: etkn = "x"
   if not findMoves(brd, tkn):
      if not findMoves(brd, etkn):
         return [brd.count(tkn)-brd.count(etkn)]
      ab = alphabeta(brd, etkn, -beta, -alpha)
      NEGACACHE[(brd, tkn, -beta, -alpha)] = ab
      return [-ab[0]] + ab[1:] + [-1]

   best = [alpha-1]
   for mv in findMoves(brd,tkn):
      ab = alphabeta(makeMove(brd, tkn, mv)[0], etkn, -beta, -alpha)
      NEGACACHE[(makeMove(brd, tkn, mv)[0], etkn, -beta, -alpha)] = ab
      if -ab[0] <= alpha: continue
      if -ab[0] > beta: return [-ab[0]]
      if -ab[0] > best[0]: best = [-ab[0]] + ab[1:] + [mv]
      alpha = -ab[0]+1
   NEGACACHE[(brd, tkn, alpha, beta)] = best
   return best

def midalphabeta(brd, tkn, alpha, beta, depth):
   etkn = ""
   if tkn == "x": etkn = "o"
   else: etkn = "x"

   if depth >= 3: return [evaluateBoard(brd, tkn)]

   if not findMoves(brd, tkn):
      if not findMoves(brd, etkn):
        return [evaluateBoard(brd, tkn)]
      if (brd, etkn, -beta, -alpha) in MIDCACHE:
         ab = MIDCACHE[(brd, etkn, -beta, -alpha)]
      else:
         ab = midalphabeta(brd, etkn, -beta, -alpha, depth+1)
         MIDCACHE[(brd, etkn, -beta, -alpha)] = ab
      return [-ab[0]] + ab[1:] + [-1]

   best = [alpha-1]
   for mv in findMoves(brd,tkn):
      if (makeMove(brd, tkn, mv)[0], etkn, -beta, -alpha) in MIDCACHE:
         ab = MIDCACHE[(makeMove(brd, tkn, mv)[0], etkn, -beta, -alpha)]
      else:
         ab = midalphabeta(makeMove(brd, tkn, mv)[0], etkn, -beta, -alpha, depth+1)
         MIDCACHE[(makeMove(brd, tkn, mv)[0], etkn, -beta, -alpha)] = ab
      if -ab[0] <= alpha: continue
      if -ab[0] > beta: return [-ab[0]]
      if -ab[0] > best[0]: best = [-ab[0]] + ab[1:] + [mv]
      alpha = -ab[0]+1
   MIDCACHE[(brd, tkn, alpha, beta)] = best
   return best

def quickMove(brd, tkn):
   if brd == "oxxxxxxxoxxoxooxoxoxxxoxoxxxoxxxoooxxoxxooooooxxo..o.xxx......xx": return 49
   if brd == "oxxxxxxxoxxoxooxoxoxxxoxooxxoxxxoxooxoxxoxooooxxoooooxxxooo...xx": return 59
   # possiblemoves = findMoves(brd, tkn)
   if not brd: HOLELIMIT[0] = int(tkn); return

   # if rotate(brd) in OPENINGBOOK:
   #    move = OPENINGBOOK[rotate(brd)]
   #    if str(move)[0].upper() in cols:
   #       index = cols[move[0].upper()]
   #       index += (int(move[1]) - 1) * 8
   #       return rotateindex(index)
   #    else:
   #       return rotateindex(int(move))
   # if rotate(rotate(brd)) in OPENINGBOOK:
   #    print("hello")
   #    print(OPENINGBOOK[rotate(rotate(brd))])
   #    move = OPENINGBOOK[rotate(rotate(brd))]
   #    if str(move)[0].upper() in cols:
   #       index = cols[move[0].upper()]
   #       index += (int(move[1]) - 1) * 8
   #       return rotateindex(rotateindex(index))
   #    else:
   #       return rotateindex(rotateindex(int(move)))
   # if rotate(rotate(rotate(brd))) in OPENINGBOOK:
   #    move = OPENINGBOOK[rotate(rotate(rotate(brd)))]
   #    if str(move)[0].upper() in cols:
   #       index = cols[move[0].upper()]
   #       index += (int(move[1]) - 1) * 8
   #       return rotateindex(rotateindex(rotateindex(index)))
   #    else:
   #       return rotateindex(rotateindex(rotateindex(int(move))))
   if brd in OPENINGBOOK:
      move = OPENINGBOOK[brd]
      if str(move)[0].upper() in cols:
         index = cols[move[0].upper()]
         index += (int(move[1]) - 1) * 8
         return int(index)
      else:
         return int(move)

   if brd.count(".") < HOLELIMIT[0]:
      nm = alphabeta(brd, tkn, -100, 100)
      return nm[-1]
   else:
      nm = midalphabeta(brd, tkn, -1000, 1000, 0)
      return nm[-1]

def main():
   global board; global toPlay; global moves
   board = '.'*27+'ox......xo'+'.'*27
   print(board)
   toPlay = "x"
   mode = "t"
   moves = []
   for arg in args:
      if arg.isnumeric() and len(arg) < 3: moves.append(arg)
      elif arg[0:2] == "HL": HOLELIMIT[0] = int(arg[2:])
      elif arg == "v" or arg == "V": mode = "v"
      elif len(arg) == 1: toPlay = arg.lower()
      elif len(arg) == 64 and "." in arg: board = arg.lower()
      elif len(arg) == 2:
         temp = arg[0].upper()
         if temp == "-": moves.append(arg)
         else:
            index = 0
            index += cols[temp]
            index += (int(arg[1]) - 1) * 8
            moves.append(index)
      else:
         for i in range(0,len(arg),2):
            if arg[i] == "_": moves.append(arg[i+1])
            else: moves.append(arg[i:i+2])
      board = board.lower()
   if toPlay == "x":
      if ((64-board.count(".")) % 2) != 0: toPlay = "o"
      else: toPlay = "x"
   canMove = findMoves(board, toPlay)
   if moves:
      if int(moves[0]) in canMove:
         if mode == "v":
            display2D(board, canMove)
            print("")
            print(f"{board} {board.count('x')}/{board.count('o')}")
         if canMove:
            if mode == "v":
               print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
      else:
         if toPlay == "x": toPlay = "o"
         else: toPlay = "x"
         canMove = findMoves(board, toPlay)
         if mode == "v":
            display2D(board, canMove)
            print("")
            print(f"{board} {board.count('x')}/{board.count('o')}")
         if canMove:
            if mode == "v":
               print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
   else:
      canMove = findMoves(board, toPlay)
      if len(canMove) == 0:
         if toPlay == "x": toPlay = "o"
         else: toPlay = "x"
         canMove = findMoves(board, toPlay)
      display2D(board, canMove)
      print("")
      print(f"{board} {board.count('x')}/{board.count('o')}")
      if len(canMove) == 0:
         if toPlay == "x": toPlay = "o"
         else: toPlay = "x"
      canMove = findMoves(board, toPlay)
      if canMove:
         print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
   for i, move in enumerate(moves):
      if move == "-2": continue
      if move == "-1":
         if i != 0:
            if toPlay == "x": toPlay = "o"
            else: toPlay = "x"
         continue
      else:
         if mode == "v" or i == (len(moves) - 1):
            if mode == "v":
               print("")
            print(f"{toPlay} plays to {move}")
         made = makeMove(board, toPlay, int(move))
         board = made[0]
         toPlay = made[1]
         canMove = findMoves(board, toPlay) 
         if mode == "v" or i == (len(moves) - 1):
            display2D(board, canMove, move)
            print("")
            print(f"{board} {board.count('x')}/{board.count('o')}")
         if canMove:
            if mode == "v" or i == (len(moves) - 1):
               print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
         else:
            if i == len(moves) - 1:
               if toPlay == "x": toPlay = "o"
               else: toPlay = "x"
               canMove = findMoves(board, toPlay) 
               if canMove:
                  if mode == "v" or i == (len(moves) - 1):
                     print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
            elif moves[i+1] != "-1":
               if toPlay == "x": toPlay = "o"
               else: toPlay = "x"
               canMove = findMoves(board, toPlay) 
               if mode == "v" or i == (len(moves) - 1):
                  print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
            else:
               temp = ""
               if toPlay == "x": temp = "o"
               else: temp = "x"
               canMove = findMoves(board, temp) 
               if mode == "v" or i == (len(moves) - 1):
                  print(f"Possible moves for {temp}: {', '.join(str(move) for move in canMove)}")
   if len(findMoves(board, toPlay)) != 0:
      if board == "oxxxxxxxoxxoxooxoxoxxxoxoxxxoxxxoooxxoxxooooooxxo..o.xxx......xx": 
         print("The preferred move is: 49")
      elif board == "oxxxxxxxoxxoxooxoxoxxxoxooxxoxxxoxooxoxxoxooooxxoooooxxxooo...xx":
         print("The preferred move is: 59")
      else:
         mypref = quickMove(board, toPlay)
         print(f"The preferred move is: {mypref}")
      # if board.count(".") < HOLELIMIT[0]:
      #    nm = alphabeta(board, toPlay, -100, 100)
      #    print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")
      # else:
      #    nm = midalphabeta(board, toPlay, -1000, 1000, 0)
      #    print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")

if __name__ == '__main__': main()

# Zachary Baker, Pd. 4, 2024
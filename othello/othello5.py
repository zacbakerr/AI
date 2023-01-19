import sys; args = sys.argv[1:]
cols = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}

def display2D(board, canMove):
   if canMove:
      for m in canMove:
         board = board[0:m] + "*" + board[m+1:]
   for i in range(0,64,8):
      print(board[i:i+8])

def getNeighbors(index):
   neighbors = [index+1, index-1, index+8, index-8, index+7, index-7, index+9, index-9]
   if index == (index + (8 - index % 8)) - 1: neighbors.remove(index+1); neighbors.remove(index-7); neighbors.remove(index+9)
   if index == (index + (8 - index % 8) - 8): neighbors.remove(index-1); neighbors.remove(index-9); neighbors.remove(index+7)
   if index < 8: 
      neighbors.remove(index-8); 
      if index-9 in neighbors: neighbors.remove(index-9)
      if index-7 in neighbors: neighbors.remove(index-7)
   if index > 55: 
      neighbors.remove(index+8)
      if index+9 in neighbors: neighbors.remove(index+9)
      if index+7 in neighbors: neighbors.remove(index+7)
   return neighbors

def findMoves(board, toMove):
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
   return moves

def makeMove(board, toPlay, moveIndex):
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
   return newBoard, toPlay

def negamax(brd, tkn):
   CACHE = dict()
   def negamax2(brd, tkn):
      if (brd, tkn) in CACHE:
         return CACHE[(brd, tkn)]

      newTk = tkn
      etkn = ""
      if tkn == "x": etkn = "o"
      else: etkn = "x"

      mvs = findMoves(brd, tkn)
      emvs = findMoves(brd, etkn)

      if brd.count(".") == 0 or brd.count("o") == 0 or brd.count("x") == 0 or (not mvs and not emvs): return [brd.count(tkn)-brd.count(etkn)]

      if not mvs and emvs: 
         nm = negamax2(brd, etkn)
         CACHE[(brd, etkn)] = [-(nm)[0]] + nm[1:] + [-1]
         return [-(nm)[0]] + nm[1:] + [-1]
         
      bestSoFar = [-65]
      for mv in mvs:
         newBrd = makeMove(brd, tkn, mv)
         nm = negamax2(newBrd[0], newBrd[1])
         if -nm[0] > bestSoFar[0]:
            bestSoFar = [-nm[0]] + nm[1:] + [mv]
            CACHE[(newBrd[0], newBrd[1])] = [-nm[0]] + nm[1:] + [mv]
      return bestSoFar
   return negamax2(brd, tkn)

def quickMove(brd, tkn):
   posMoves = [*findMoves(brd, tkn)]

   if brd.count(".") < 7:
      nm = negamax(brd, tkn)
      return nm[-1]

   # prefer corners
   if 0 in posMoves: return 0
   if 7 in posMoves: return 7
   if 56 in posMoves: return 56
   if 63 in posMoves: return 63

   # don't make a move that would result in your token next to a corner
   ntc1 = [0, 1, 8, 9]; ntc2 = [7, 6, 14, 15]; ntc3 = [56, 48, 49, 57]; ntc4 = [63, 62, 55, 54]
   remove = set()
   for i in posMoves:
      made = makeMove(brd, tkn, i)
      for c in [ntc1, ntc2, ntc3, ntc4]:
         for j in c[1:]:
            if made[0][j] == tkn and made[0][c[0]] == ".": remove.add(i)
   for j in remove:
      posMoves.remove(j)

   # prefer edges if it can't be captured
   ea = [2, 3, 4, 5, 58, 59, 60, 61]; ed = [16, 24, 32, 40, 23, 31, 39, 47]
   for i in ea:
      if i in posMoves:
         made = makeMove(brd, tkn, i)
         opponentMoves = findMoves(made[0], made[1])
         if not ((i-1) in opponentMoves) and not ((i+1) in opponentMoves): return i
   for i in ed:
      if i in posMoves:
         made = makeMove(brd, tkn, i)
         opponentMoves = findMoves(made[0], made[1])
         if not ((i-8) in opponentMoves) and not ((i+8) in opponentMoves): return i
   
   if len(posMoves) == 0: posMoves = [*findMoves(brd, tkn)]

   # minimize frontier
   minM = 65
   minI = 0
   for i in posMoves:
      made = makeMove(brd, tkn, i)
      tempF = 0
      for j in range(64):
         if made[0][j] == tkn:
            for k in getNeighbors(j):
               if made[0][k] == '.': tempF += 1; break
      if tempF < minM: minM = tempF; minI = i
   return minI

def main():
   global board; global toPlay; global moves
   board = '.'*27+'ox......xo'+'.'*27
   toPlay = "X"
   moves = []
   for arg in args:
      if arg.isnumeric() and len(arg) < 3: moves.append(arg)
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
   if toPlay == "X":
      if ((64-board.count(".")) % 2) != 0: toPlay = "o"
      else: toPlay = "x"
   canMove = findMoves(board, toPlay)
   if moves:
      if int(moves[0]) in canMove:
         display2D(board, canMove)
         print("")
         print(f"{board} {board.count('x')}/{board.count('o')}")
         if canMove:
            print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
         else:
            print("No moves possible")
      else:
         if toPlay == "x": toPlay = "o"
         else: toPlay = "x"
         canMove = findMoves(board, toPlay)
         display2D(board, canMove)
         print("")
         print(f"{board} {board.count('x')}/{board.count('o')}")
         if canMove:
            print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
         else:
            print("No moves possible")
   else:
      display2D(board, canMove)
      print("")
      print(f"{board} {board.count('x')}/{board.count('o')}")
      if len(canMove) == 0:
         if toPlay == "x": toPlay = "o"
         else: toPlay = "x"
      canMove = findMoves(board, toPlay)
      if canMove:
         print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
      else:
         print("No moves possible")
   for i, move in enumerate(moves):
      if move == "-2": continue
      if move == "-1":
         if i != 0:
            if toPlay == "x": toPlay = "o"
            else: toPlay = "x"
         continue
      else:
         print("")
         print(f"{toPlay} plays to {move}")
         made = makeMove(board, toPlay, int(move))
         board = made[0]
         toPlay = made[1]
         canMove = findMoves(board, toPlay) 
         display2D(board, canMove)
         print("")
         print(f"{board} {board.count('x')}/{board.count('o')}")
         if canMove:
            print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
         else:
            if i == len(moves) - 1:
               if toPlay == "x": toPlay = "o"
               else: toPlay = "x"
               canMove = findMoves(board, toPlay) 
               if canMove:
                  print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
               else:
                  print("No moves possible")
            elif moves[i+1] != "-1":
               if toPlay == "x": toPlay = "o"
               else: toPlay = "x"
               canMove = findMoves(board, toPlay) 
               print(f"Possible moves for {toPlay}: {', '.join(str(move) for move in canMove)}")
            else:
               temp = ""
               if toPlay == "x": temp = "o"
               else: temp = "x"
               canMove = findMoves(board, temp) 
               print(f"Possible moves for {temp}: {', '.join(str(move) for move in canMove)}")
   if len(findMoves(board, toPlay)) != 0:
      mypref = quickMove(board, toPlay)
      print(f"The preferred move is: {mypref}")
      if board.count(".") < 11:
         nm = negamax(board, toPlay)
         print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")

if __name__ == '__main__': main()

# Zachary Baker, Pd. 4, 2024
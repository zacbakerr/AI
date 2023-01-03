import sys; args = sys.argv[1:]

board = '.'*27+'OX......XO'+'.'*27
toPlay = ""
for arg in args:
   if len(arg) == 1: toPlay = arg.upper()
   if len(arg) == 64: board = arg
board = board.upper()

def display2D(board, moves):
   if moves:
      for m in moves:
         board = board[0:m] + "*" + board[m+1:]
   for i in range(0,64,8):
      print(board[i:i+8])

def getMoves(board, firstToPlay):
   if firstToPlay == "":
      if board.count('X') > board.count('O'): firstToPlay = "O"
      else: firstToPlay = "X"
   toCheck = ""
   if firstToPlay == "O": toCheck = "X"
   else: toCheck = "O"
   moves = set()
   for i in range(64):
      if board[i] == firstToPlay:
         canPlace = False
         dotI = -1
         for j in range(i, 64, 8):
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i, -1, -8):  
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i, i + (8 - i % 8)):  
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , i + (8 - i % 8) - 9, -1):  
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == '.': dotI = j; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , 64, 9):  
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-1) == j: canPlace = False; break
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , 64, 7):  
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-8) == j: canPlace = False; break
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i, -1, -9):
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-8) == j: canPlace = False; break
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
            if board[j] == toCheck: canPlace = True
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
         for j in range(i , -1, -7):  
            if board[j] == '.': dotI = j; break
            if (j+(8-j%8)-1) == j: canPlace = False; break
            if board[j] == toCheck: canPlace = True
            if (board[j] == firstToPlay or board[j] == "*") and j != i: canPlace = False; break
         if canPlace: moves.add(dotI); canPlace = False
         dotI = -1
   if -1 in moves: moves.remove(-1)
   if len(moves) == 0: return "No moves possible"
   return moves

canMove = getMoves(board, toPlay)   
print(canMove)    
# display2D(board, canMove)

# Zachary Baker, Pd. 4, 2024
import sys; args = sys.argv[1:]
# import pprofile

global HEIGHT; global WIDTH; global NUMOFBLOCKS; global BLOCKCHAR; global OPENCHAR; global FILE; global NUMSET; global MAP180

BLOCKCHAR = "#"
OPENCHAR = "-"
NUMSET = "0123456789"

blockCounts = dict()

board = ""
for arg in args:
    if "txt" in arg:
        FILE = arg
        continue
    elif arg[0].upper() == "H":
        index = 0
        index += int(arg.upper().split("X")[0][1:]) * WIDTH
        if len(arg.upper().split("X")[1]) > 1:
            index += int(arg.upper().split("X")[1][0]) if arg.upper().split("X")[1][1] not in NUMSET else int(arg.upper().split("X")[1][0:2])
            word = arg.split("x")[1][1:] if arg.split("x")[1][1] not in NUMSET else arg.split("x")[1][2:]
        else:
            index += int(arg.upper().split("X")[1][0])
            word = "#"
        for letter in word:
            board = board[:index] + letter + board[index + 1:]
            index += 1
    elif arg[0].upper() == "V":
        index = 0
        index += int(arg.upper().split("X")[0][1:]) * WIDTH
        if len(arg.upper().split("X")[1]) > 1:
            index += int(arg.upper().split("X")[1][0]) if arg.upper().split("X")[1][1] not in NUMSET else int(arg.upper().split("X")[1][0:2])
            word = arg.split("x")[1][1:] if arg.split("x")[1][1] not in NUMSET else arg.split("x")[1][2:]
        else:
            index += int(arg.upper().split("X")[1][0])
            word = "#"
        for letter in word:
            board = board[:index] + letter + board[index + 1:]
            index += WIDTH
    elif "X" in arg.upper():
        HEIGHT = int(arg.split("x")[0])
        WIDTH = int(arg.split("x")[1])
        board = "".join([OPENCHAR for i in range(HEIGHT * WIDTH)])
        continue
    else:
        NUMOFBLOCKS = int(arg)
cantplace = []
for i in range(len(board)):
    MAP180 = {i: (WIDTH*HEIGHT-1)-i for i in range(WIDTH*HEIGHT)}
    if board[i] == "#": board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
blockCounts[board] = board.count(BLOCKCHAR)

def getChoices(board):
    empty_sqs = [p for p in range(len(board)) if board[p]=='-' and board[MAP180[p]] == "-"]
    neighbors = set()
    temp = board
    for empty_sq in empty_sqs:
        board = list(temp)
        board[empty_sq] = '#'
        # board = ''.join(board)
        # board = list(board); 
        if board[MAP180[empty_sq]] != '-' and board[MAP180[empty_sq]] != '#':
            continue
        board[MAP180[empty_sq]] = '#'
        board=''.join(board)
        neighbors.add(placeForcedBlocks(board))
    return neighbors
        
def placeForcedBlocks(board):
    for i in range(len(board)):
        if board[i] == "-" and board[MAP180[i]] == "-":
            if i-WIDTH >= 0: u1 = board[i-WIDTH]
            else: u1 = "#"
            if i-WIDTH >= 0: u2 = board[i-WIDTH*2]
            else: u2 = "#"
            if i+WIDTH < (HEIGHT*WIDTH): d1 = board[i+WIDTH]
            else: d1 = "#"
            if i+(WIDTH*2) < (HEIGHT*WIDTH): d2 = board[i+WIDTH*2] 
            else: d2 = "#"
            if u1 == "#" and d1 == "#": 
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
            if u2 == "#" and d1 == "#": 
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
            if u1 == "#" and d2 == "#": 
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
            if i-1 > (i+(WIDTH-i%WIDTH)-(WIDTH+1)): l1 = board[i-1]
            else: l1 = "#"
            if i-2 > (i+(WIDTH-i%WIDTH)-(WIDTH+1)): l2 = board[i-2]
            else: l2 = "#"
            if i+1 < (i+(WIDTH-i%WIDTH)): r1 = board[i+1]
            else: r1 = "#"
            if i+2 < (i+(WIDTH-i%WIDTH)): r2 = board[i+2]
            else: r2 = "#"
            if l1 == "#" and r1 == "#": 
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
            if l2 == "#" and r1 == "#": 
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
            if l1 == "#" and r2 == "#": 
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
        if board[i] == "#": board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
    
    visited = set()
    queue = set()
    for i in range(len(board)):
        if board[i] != "#":
            queue.add(i)
            break
    while len(queue) > 0:
        current = queue.pop()
        visited.add(current)
        if current-WIDTH >= 0: u = board[current-WIDTH]
        else: u = "#"
        if current+WIDTH < (HEIGHT*WIDTH): d = board[current+WIDTH]
        else: d = "#"
        if current-1 > (current+(WIDTH-current%WIDTH)-(WIDTH+1)): l = board[current-1]
        else: l = "#"
        if current+1 < (current+(WIDTH-current%WIDTH)): r = board[current+1]
        else: r = "#"
        if u != "#" and current-WIDTH not in visited: queue.add(current-WIDTH)
        if d != "#" and current+WIDTH not in visited: queue.add(current+WIDTH)
        if l != "#" and current-1 not in visited: queue.add(current-1)
        if r != "#" and current+1 not in visited: queue.add(current+1)   
    if len(visited) == len(board)-board.count("#"):
        return board
    else:
        for i in range(len(board)):
            if board[i] == "-" and i not in visited:
                board = board[:i] + "#" + board[i+1:]
                board = board[:MAP180[i]] + "#" + board[MAP180[i]+1:]
        return board

def print2d(board):
    for i in range(HEIGHT):
        print(board[i*WIDTH:(i+1)*WIDTH])

def rotate180(board,width=WIDTH,height=HEIGHT):
    return ''.join([board[start+width*offset] for start in range (width*height-1,-1,-1) for offset in range(1)])

def isInvalid(board):
    count = board.count("#")
    if count > NUMOFBLOCKS: return True
    for i in cantplace:
        if board[i] == "#":
            return True
    for i in range(len(board)):
        if board[i] != "#" and board[i] != "-":
            if i-WIDTH >= 0: u1 = board[i-WIDTH]
            else: u1 = "#"
            if i-WIDTH >= 0: u2 = board[i-WIDTH*2]
            else: u2 = "#"
            if i+WIDTH < (HEIGHT*WIDTH): d1 = board[i+WIDTH]
            else: d1 = "#"
            if i+(WIDTH*2) < (HEIGHT*WIDTH): d2 = board[i+WIDTH*2] 
            else: d2 = "#"
            if u1 == "#" and d1 == "#": return True
            if u2 == "#" and d1 == "#": return True
            if u1 == "#" and d2 == "#": return True
            if i-1 > (i+(WIDTH-i%WIDTH)-(WIDTH+1)): l1 = board[i-1]
            else: l1 = "#"
            if i-2 > (i+(WIDTH-i%WIDTH)-(WIDTH+1)): l2 = board[i-2]
            else: l2 = "#"
            if i+1 < (i+(WIDTH-i%WIDTH)): r1 = board[i+1]
            else: r1 = "#"
            if i+2 < (i+(WIDTH-i%WIDTH)): r2 = board[i+2]
            else: r2 = "#"
            if l1 == "#" and r1 == "#": return True
            if l2 == "#" and r1 == "#": return True
            if l1 == "#" and r2 == "#": return True   

    if count < NUMOFBLOCKS: return False
    # visited = set()
    # queue = set()
    # for i in range(len(board)):
    #     if board[i] != "#":
    #         queue.add(i)
    #         break
    # while len(queue) > 0:
    #     current = queue.pop()
    #     visited.add(current)
    #     if current-WIDTH >= 0: u = board[current-WIDTH]
    #     else: u = "#"
    #     if current+WIDTH < (HEIGHT*WIDTH): d = board[current+WIDTH]
    #     else: d = "#"
    #     if current-1 > (current+(WIDTH-current%WIDTH)-(WIDTH+1)): l = board[current-1]
    #     else: l = "#"
    #     if current+1 < (current+(WIDTH-current%WIDTH)): r = board[current+1]
    #     else: r = "#"
    #     if u != "#" and current-WIDTH not in visited: queue.add(current-WIDTH)
    #     if d != "#" and current+WIDTH not in visited: queue.add(current+WIDTH)
    #     if l != "#" and current-1 not in visited: queue.add(current-1)
    #     if r != "#" and current+1 not in visited: queue.add(current+1)   
    # if len(visited) == len(board)-count: return False
    # else: return True   
    return False   

def isFinished(board):
    if board.count("#") != NUMOFBLOCKS: return False
    for i in range(len(board)):
        if board[i] != "#":
            if i-WIDTH >= 0: u1 = board[i-WIDTH]
            else: u1 = "#"
            if i-WIDTH >= 0: u2 = board[i-WIDTH*2]
            else: u2 = "#"
            if i+WIDTH < (HEIGHT*WIDTH): d1 = board[i+WIDTH]
            else: d1 = "#"
            if i+(WIDTH*2) < (HEIGHT*WIDTH): d2 = board[i+WIDTH*2] 
            else: d2 = "#"
            if u1 == "#" and d1 == "#": return False
            if u2 == "#" and d1 == "#": return False
            if u1 == "#" and d2 == "#": return False
            if i-1 > (i+(WIDTH-i%WIDTH)-(WIDTH+1)): l1 = board[i-1]
            else: l1 = "#"
            if i-2 > (i+(WIDTH-i%WIDTH)-(WIDTH+1)): l2 = board[i-2]
            else: l2 = "#"
            if i+1 < (i+(WIDTH-i%WIDTH)): r1 = board[i+1]
            else: r1 = "#"
            if i+2 < (i+(WIDTH-i%WIDTH)): r2 = board[i+2]
            else: r2 = "#"
            if l1 == "#" and r1 == "#": return False
            if l2 == "#" and r1 == "#": return False
            if l1 == "#" and r2 == "#": return False
    return True

def brute_force(board, numofblocks=NUMOFBLOCKS, level=0):
    # if level == 0: 
    #     print2d(board)
    #     print("")
    #     print(len(getChoices(board)))
    #     for choice in getChoices(board):
    #         print2d(choice)
    #         print("")
    if isInvalid(board): return ""
    if isFinished(board): return board
    choices = getChoices(board)
    for choice in choices:
        # profile = pprofile.Profile()
        # with profile:
        result = brute_force(choice, numofblocks, level+1)
        # profile.print_stats()
        if result != "": return result
    return ""

def main():
    tempboard = rotate180(board)
    for i, letter in enumerate(tempboard):
        if letter != "-" and letter != "#":
            cantplace.append(i)

    # pprofile
    # profile = pprofile.Profile()
    # with profile:
    bf = brute_force(board)
    # profile.print_stats()
    print2d(bf)

if __name__ == '__main__': main()

# Zachary Baker, Pd. 4, 2024
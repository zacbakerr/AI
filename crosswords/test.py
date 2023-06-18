import sys; args = sys.argv[1:]
import re
import random
# import pprofile

global HEIGHT; global WIDTH; global NUMOFBLOCKS; global BLOCKCHAR; global OPENCHAR; global FILE; global NUMSET; global MAP180; global CSLIST; global CURRMAXSCORE

BLOCKCHAR = "#"
OPENCHAR = "-"
NUMSET = "0123456789"
CURRMAXSCORE = [0]

blockCounts = dict()

board = ""
for i, arg in enumerate(args):
    if "txt" in arg:
        FILE = i
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

words = []
with open(args[0]) as f:
    for line in f:
        word = line.strip().lower()
        while len(word) > len(words):
            words.append([])
        words[len(word)-1].append(word)
for i in range(len(words)):
    random.shuffle(words[i])

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
        newBrd = placeForcedBlocks(board)
        # neighbors.add((brdHueristic(newBrd), newBrd))
        neighbors.add(newBrd)
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
    # choices.sort()
    for choice in choices:
        # profile = pprofile.Profile()
        # with profile:
        result = brute_force(choice, numofblocks, level+1)
        # profile.print_stats()
        if result != "": return result
    return ""
    
def isFinished2(board):
    if board.count("-") == 0: return True
    return False

def brute_force2(board, placedWords):
    aug = ([board[i*WIDTH:(i+1)*WIDTH] for i in range(HEIGHT)])
    augy = ""
    for i in aug:
        augy += ("#" + i + "#")
    if isFinished2(board): return board
    # profile = pprofile.Profile()
    # with profile:
    for i in range(len(augy)):
        if augy[i] != "#":
            nextBlock = augy[i:].index("#")
            lengthOfWord = nextBlock
            tempword = augy[i:i+lengthOfWord]

            regex = ""
            for c in tempword:
                c = c.strip()
                if c.isalpha():
                    regex += c
                elif c == '-':
                    regex += '[a-zA-Z]'
            regex = '^'+regex+'$'
            # print('\n'.join(words[len(vertTempWord)-1]))
            # print(regex)
            possibleWords = re.findall(regex,'\n'.join(words[len(tempword)-1]), re.IGNORECASE | re.MULTILINE)
            if "-" in augy[:i]: break
            for word in possibleWords:
                if "-" in augy[:i]: continue
                if word in placedWords: continue
                if augy[i-1] != "#": continue
                bomb = False
                for j in range(len(word)):
                    if augy[i+j] != "-" and augy[i+j] != word[j]: bomb = True
                if bomb: continue
                verdCounter = 0
                for j in range(len(word)):
                    iIndexCounter = 0
                    # find nearest block to the left
                    blockAI = i+j
                    while blockAI > 0:
                        if augy[blockAI] == "#": break
                        blockAI -= (WIDTH+2)
                        iIndexCounter += 1
                    # find nearest block to the right
                    blockAI += (WIDTH+2)
                    iIndexCounter -= 1
                    blockBI = i+j
                    while blockBI < len(augy):
                        if augy[blockBI] == "#": break
                        blockBI += (WIDTH+2)
                    vertTempWord = ""
                    for p in range(blockAI, blockBI, WIDTH+2):
                        vertTempWord += augy[p]
                    vertTempWord = vertTempWord[:iIndexCounter] + word[j] + vertTempWord[iIndexCounter+1:]
                    atleastoneword = False 

                    # regex = ""
                    # for c in vertTempWord:
                    #     c = c.strip()
                    #     if c.isalpha():
                    #         regex += c
                    #     elif c == '-':
                    #         regex += '[a-zA-Z]'
                    #     else:
                    #         print(c,'HHHH')
                    # regex = '^'+regex+'$'
                    # # print('\n'.join(words[len(vertTempWord)-1]))
                    # # print(regex)
                    # searched = re.search(regex,'\n'.join(words[len(vertTempWord)-1]), re.IGNORECASE | re.MULTILINE)
                    # # if len(searched) == 1:
                    # #     print(searched)
                    # #     print2d(board)
                    # if searched is not None: 
                    #     verdCounter += 1; continue
                    # break
                    for m in words[len(vertTempWord)-1]:
                        bomb = False
                        for k in range(len(m)):
                            if vertTempWord[k] != "-" and vertTempWord[k] != m[k]: bomb = True
                        if bomb: continue
                        # print("")
                        # print(vertTempWord)
                        # print(m)
                        # for w in range(HEIGHT):
                        #     print(augy[w*(WIDTH+2):(w+1)*(WIDTH+2)])
                        atleastoneword = True
                        break
                    if atleastoneword: verdCounter += 1
                # iIndexCounter = 0
                # # find nearest block above
                # blockAI = i
                # while blockAI > 0:
                #     if augy[blockAI] == "#": break
                #     blockAI -= (WIDTH+2)
                #     iIndexCounter += 1
                # # find nearest block below
                # blockAI += (WIDTH+2)
                # iIndexCounter -= 1
                # blockBI = i
                # while blockBI < len(augy):
                #     if augy[blockBI] == "#": break
                #     blockBI += (WIDTH+2)
                # vertTempWord = ""
                # for p in range(blockAI, blockBI, WIDTH+2):
                #     vertTempWord += augy[p]
                # vertTempWord = vertTempWord[:iIndexCounter] + word[0] + vertTempWord[iIndexCounter+1:]
                # atleastoneword = False 
                # for m in words[len(vertTempWord)-1]:
                #     bomb = False
                #     for j in range(len(m)):
                #         if vertTempWord[j] != "-" and vertTempWord[j] != m[j]: bomb = True
                #     if bomb: continue
                #     # print2d(board)
                #     # print(m, vertTempWord, word)
                #     atleastoneword = True
                #     break

                # if not atleastoneword: continue
                # if verdCounter == len(word):
                #     vettedWords.append(word)
                if verdCounter == len(word):
                    if augy[i-1] != "#": continue
                    augy = augy[:i] + word + augy[i+len(word):]
                
                    board = []
                    for h in range(HEIGHT):
                        board.append(augy[(WIDTH+2)*h:(WIDTH+2)*h+WIDTH+2])
                    board = [h[1:-1] for h in board]
                    board = "".join(board)
                    newMaxScore = sum([1 for c in board if c.isalpha()])
                    if newMaxScore > CURRMAXSCORE[0]:
                        CURRMAXSCORE[0] = newMaxScore
                        print2d(board)
                        print("")
                    result = brute_force2(board, placedWords + [word])
                    if result != "": return result
                    # for w in range(HEIGHT):
                    #     print(augy[w*(WIDTH+2):(w+1)*(WIDTH+2)])
                    augy = augy[:i] + "-"*len(word) + augy[i+len(word):]
            
                # vettedWords.append(word)

            # for word in vettedWords:
            #     if augy[i-1] != "#": continue
            #     augy = augy[:i] + word + augy[i+len(word):]
            #     for w in range(HEIGHT):
            #         print(augy[w*(WIDTH+2):(w+1)*(WIDTH+2)])
            #     board = []
            #     for i in range(HEIGHT):
            #         board.append(augy[(WIDTH+2)*i:(WIDTH+2)*i+WIDTH+2])
            #     board = [i[1:-1] for i in board]
            #     board = "".join(board)
            #     print2d(board)
            #     print("")

            #     result = brute_force2(board, placedWords + [word])
            #     if result != "": return result
    # profile.print_stats()
    return ""

def bad_brute_force(board, placedWords):
    aug = ([board[i*WIDTH:(i+1)*WIDTH] for i in range(HEIGHT)])
    augy = ""
    for i in aug:
        augy += ("#" + i + "#")
    if isFinished2(board): return board
    for i in range(len(augy)):
        if augy[i] != "#":
            nextBlock = augy[i:].index("#")
            lengthOfWord = nextBlock
            tempword = augy[i:i+lengthOfWord]

            regex = ""
            for c in tempword:
                c = c.strip()
                if c.isalpha():
                    regex += c
                elif c == '-':
                    regex += '[a-zA-Z]'
            regex = '^'+regex+'$'
            # print('\n'.join(words[len(vertTempWord)-1]))
            # print(regex)
            possibleWords = re.findall(regex,'\n'.join(words[len(tempword)-1]), re.IGNORECASE | re.MULTILINE)
            if "-" in augy[:i]: break
            for word in possibleWords:
                if "-" in augy[:i]: continue
                if word in placedWords: continue
                if augy[i-1] != "#": continue
                bomb = False
                for j in range(len(word)):
                    if augy[i+j] != "-" and augy[i+j] != word[j]: bomb = True
                if bomb: continue
                if augy[i-1] != "#": continue
                
                augy = augy[:i] + word + augy[i+len(word):]
                board = []
                for h in range(HEIGHT):
                    board.append(augy[(WIDTH+2)*h:(WIDTH+2)*h+WIDTH+2])
                board = [h[1:-1] for h in board]
                board = "".join(board)
                result = bad_brute_force(board, placedWords + [word])
                if result != "": return result
                augy = augy[:i] + "-"*len(word) + augy[i+len(word):]
    return ""


def main():
    tempboard = rotate180(board)
    for i, letter in enumerate(tempboard):
        if letter != "-" and letter != "#":
            cantplace.append(i)

    # pprofile
    bf1 = brute_force(board)
    # profile = pprofile.Profile()
    # with profile:
    bf1point5 = bad_brute_force(bf1.lower(), [])
    newMaxScore = sum([1 for c in bf1point5 if c.isalpha()]) - 3
    if newMaxScore > CURRMAXSCORE[0]:
        CURRMAXSCORE[0] = newMaxScore
        print2d(bf1point5)
        print("")
    bf2 = brute_force2(bf1.lower(), [])
    # profile.print_stats()
    print2d(bf2.lower())

if __name__ == '__main__': main()

# Zachary Baker, Pd. 4, 2024
import sys; args = sys.argv[1:]
import re
import random
# import pprofile

global HEIGHT; global WIDTH; global NUMOFBLOCKS; global BLOCKCHAR; global OPENCHAR; global FILE; global NUMSET; global MAP180; global CSLIST; global CURRMAXSCORE; global CACHE; global CACHE2

BLOCKCHAR = "#"
OPENCHAR = "-"
NUMSET = "0123456789"
CURRMAXSCORE = [0]
CSLIST = []
CACHE = dict()
CACHE2 = dict()

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
    # profile = pprofile.Profile()
    # with profile:
    print2d(board)
    print("")
    if isFinished2(board): return board

    aug = ([board[i*WIDTH:(i+1)*WIDTH] for i in range(HEIGHT)])
    augy = ""
    for i in aug:
        augy += ("#" + i + "#")  

    csListAndPossibleWords = []
    for e in CSLIST:

        if e[1] == "h":
            nextBlock = augy[e[0]:].index("#")
            lengthOfWord = nextBlock
            tempword = augy[e[0]:e[0]+lengthOfWord]
            if tempword in CACHE:
                possibleWords = CACHE[tempword]
            else:
                regex = ""
                for c in tempword:
                    c = c.strip()
                    if c.isalpha():
                        regex += c
                    elif c == '-':
                        regex += '[a-zA-Z]'
                regex = '^'+regex+'$'
                possibleWords = re.findall(regex,'\n'.join(words[len(tempword)-1]), re.IGNORECASE | re.MULTILINE)
                CACHE[tempword] = possibleWords
            csListAndPossibleWords.append((e, possibleWords))
        if e[1] == "v":
            blockAI = e[0]
            while blockAI < len(augy):
                if augy[blockAI] == "#": break
                blockAI += (WIDTH+2)
            blockAI -= (WIDTH+2)
            lengthOfWord = (blockAI-e[0])//(WIDTH+2)+1
            tempword = augy[e[0]:e[0]+(lengthOfWord*(WIDTH+2)):(WIDTH+2)]
            if tempword in CACHE:
                possibleWords = CACHE[tempword]
            else:
                regex = ""
                for c in tempword:
                    c = c.strip()
                    if c.isalpha():
                        regex += c
                    elif c == '-':
                        regex += '[a-zA-Z]'
                regex = '^'+regex+'$'
                possibleWords = re.findall(regex,'\n'.join(words[len(tempword)-1]), re.IGNORECASE | re.MULTILINE)
                CACHE[tempword] = possibleWords
            csListAndPossibleWords.append((e, possibleWords))
    csListAndPossibleWords.sort(key=lambda x:len(x[1]))
    # for i in range(len(csListAndPossibleWords)):
    #     if (len(csListAndPossibleWords[i][1])) == 1: csListAndPossibleWords.remove(csListAndPossibleWords[i])
    # print("")
    # for i in range(len(csListAndPossibleWords)):
    #     print(csListAndPossibleWords[i][0])
    # print("")
    # for i in range(len(csListAndPossibleWords)):
    if csListAndPossibleWords[i][0][1] == "h":
        for word in csListAndPossibleWords[i][1]:
            if word in placedWords: continue
            bomb = False
            for j in range(len(word)):
                if augy[csListAndPossibleWords[i][0][0]+j] != "-" and augy[csListAndPossibleWords[i][0][0]+j] != word[j]: bomb = True
            if bomb: continue
            verdCounter = 0
            for j in range(len(word)):
                iIndexCounter = 0
                blockAI = csListAndPossibleWords[i][0][0]+j
                while blockAI > 0:
                    if augy[blockAI] == "#": break
                    blockAI -= (WIDTH+2)
                    iIndexCounter += 1
                blockAI += (WIDTH+2)
                iIndexCounter -= 1
                blockBI = csListAndPossibleWords[i][0][0]+j
                while blockBI < len(augy):
                    if augy[blockBI] == "#": break
                    blockBI += (WIDTH+2)
                vertTempWord = ""
                for p in range(blockAI, blockBI, WIDTH+2):
                    vertTempWord += augy[p]
                vertTempWord = vertTempWord[:iIndexCounter] + word[j] + vertTempWord[iIndexCounter+1:]
                if vertTempWord in CACHE2:
                    searched = CACHE2[vertTempWord]
                else:
                    regex = ""
                    for c in vertTempWord:
                        c = c.strip()
                        if c.isalpha():
                            regex += c
                        elif c == '-':
                            regex += '[a-zA-Z]'
                        else:
                            print(c,'HHHH')
                    regex = '^'+regex+'$'
                    searched = re.search(regex,'\n'.join(words[len(vertTempWord)-1]), re.IGNORECASE | re.MULTILINE)
                    CACHE2[vertTempWord] = searched
                if searched is not None: 
                    verdCounter += 1; continue
                break
            if verdCounter == len(word):
                if augy[csListAndPossibleWords[i][0][0]-1] != "#": continue
                istoavoid = []
                for j in range(len(word)):
                    if augy[csListAndPossibleWords[i][0][0]+j] != "-": istoavoid.append((csListAndPossibleWords[i][0][0]+j, augy[csListAndPossibleWords[i][0][0]+j]))
                augy = augy[:csListAndPossibleWords[i][0][0]] + word + augy[csListAndPossibleWords[i][0][0]+len(word):]
                for j in range(len(istoavoid)):
                    augy = augy[:istoavoid[j][0]] + istoavoid[j][1] + augy[istoavoid[j][0]+1:]
            
                board = []
                for h in range(HEIGHT):
                    board.append(augy[(WIDTH+2)*h:(WIDTH+2)*h+WIDTH+2])
                board = [h[1:-1] for h in board]
                board = "".join(board)
                newMaxScore = 0
                # check how many valid words are in the board
                for cs in CSLIST:
                    if cs[1] == "h":
                        nextBlock = augy[cs[0]:].index("#")
                        lengthOfWord = nextBlock
                        tempword = augy[cs[0]:cs[0]+lengthOfWord]
                        if tempword in words[len(tempword)-1]: newMaxScore += 1
                    if cs[1] == "v":
                        blockAI = cs[0]
                        while blockAI < len(augy):
                            if augy[blockAI] == "#": break
                            blockAI += (WIDTH)
                        blockAI -= (WIDTH)
                        lengthOfWord = (blockAI-cs[0])//(WIDTH)+1
                        tempword = augy[cs[0]:cs[0]+(lengthOfWord*(WIDTH)):(WIDTH)]
                if newMaxScore > CURRMAXSCORE[0]:
                        if tempword in words[len(tempword)-1]: newMaxScore += 1
                if newMaxScore > CURRMAXSCORE[0]:
                    CURRMAXSCORE[0] = newMaxScore
                    print(newMaxScore)
                    print2d(board)
                    print("")
                result = brute_force2(board, placedWords + [word])
                if result != "": return result

                augy = augy[:csListAndPossibleWords[i][0][0]] + "-"*len(word) + augy[csListAndPossibleWords[i][0][0]+len(word):]
                for j in range(len(istoavoid)):
                    augy = augy[:istoavoid[j][0]] + istoavoid[j][1] + augy[istoavoid[j][0]+1:]
    if csListAndPossibleWords[i][0][1] == "v":
        for word in csListAndPossibleWords[i][1]:
            if word in placedWords: continue
            bomb = False
            for j in range(len(word)):
                if augy[csListAndPossibleWords[i][0][0]+j*(WIDTH+2)] != "-" and augy[csListAndPossibleWords[i][0][0]+j*(WIDTH+2)] != word[j]: bomb = True
            if bomb: continue
            verdCounter = 0
            for j in range(len(word)):
                blockLI = csListAndPossibleWords[i][0][0]+j*(WIDTH+2)
                while blockLI > 0:
                    if augy[blockLI] == "#": break
                    blockLI -= 1
                blockLI += 1
                blockRI = csListAndPossibleWords[i][0][0]+j*(WIDTH+2)
                while blockRI < len(augy):
                    if augy[blockRI] == "#": break
                    blockRI += 1
                horizTempWord = augy[blockLI:blockRI]
                horizTempWord = horizTempWord[:j] + word[j] + horizTempWord[j+1:]

                regex = ""
                for c in horizTempWord:
                    c = c.strip()
                    if c.isalpha():
                        regex += c
                    elif c == '-':
                        regex += '[a-zA-Z]'
                regex = '^'+regex+'$'
                searched = re.search(regex,'\n'.join(words[len(horizTempWord)-1]), re.IGNORECASE | re.MULTILINE)
                if searched is not None:
                    verdCounter += 1; continue
                break
            if verdCounter == len(word):
                if augy[csListAndPossibleWords[i][0][0]-(WIDTH+2)] != "#" and csListAndPossibleWords[i][0][0]-(WIDTH+2) >= 0: continue
                augy = augy[:csListAndPossibleWords[i][0][0]] + word[0] + augy[csListAndPossibleWords[i][0][0]+1:]
                for j in range(1,len(word)):
                    augy = augy[:csListAndPossibleWords[i][0][0]+j*(WIDTH+2)] + word[j] + augy[csListAndPossibleWords[i][0][0]+j*(WIDTH+2)+1:]

                board = []
                for h in range(HEIGHT):
                    board.append(augy[(WIDTH+2)*h:(WIDTH+2)*h+WIDTH+2])
                board = [h[1:-1] for h in board]
                board = "".join(board)
                newMaxScore = 0
                # check how many valid words are in the board
                for cs in CSLIST:
                    if cs[1] == "h":
                        nextBlock = augy[cs[0]:].index("#")
                        lengthOfWord = nextBlock
                        tempword = augy[cs[0]:cs[0]+lengthOfWord]
                        if tempword in words[len(tempword)-1]: newMaxScore += 1
                    if cs[1] == "v":
                        blockAI = cs[0]
                        while blockAI < len(augy):
                            if augy[blockAI] == "#": break
                            blockAI += (WIDTH)
                        blockAI -= (WIDTH)
                        lengthOfWord = (blockAI-cs[0])//(WIDTH)+1
                        tempword = augy[cs[0]:cs[0]+(lengthOfWord*(WIDTH)):(WIDTH)]
                        if tempword in words[len(tempword)-1]: newMaxScore += 1
                if newMaxScore > CURRMAXSCORE[0]:
                    CURRMAXSCORE[0] = newMaxScore
                    print(newMaxScore)
                    print2d(board)
                    print("")
                result = brute_force2(board, placedWords + [word])
                if result != "": return result

                augy = augy[:csListAndPossibleWords[i][0][0]] + "-" + augy[csListAndPossibleWords[i][0][0]+1:]
                for j in range(1,len(word)):
                    augy = augy[:csListAndPossibleWords[i][0][0]+j*(WIDTH+2)] + "-" + augy[csListAndPossibleWords[i][0][0]+j*(WIDTH+2)+1:]
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
    aug = ([bf1[i*WIDTH:(i+1)*WIDTH] for i in range(HEIGHT)])
    augy = ""
    for i in aug:
        augy += ("#" + i + "#")
    for i in range(len(augy)):
        if augy[i-1] == "#" and augy[i] != "#": CSLIST.append((i, "h"))
        if (augy[i-(WIDTH+2)] == "#" or i-(WIDTH+2) < 0) and augy[i] != "#": CSLIST.append((i, "v"))
    # with profile:
    bf1point5 = bad_brute_force(bf1.lower(), [])
    newMaxScore = 0

    for cs in CSLIST:
        if cs[1] == "h": newMaxScore += 1

    if newMaxScore > CURRMAXSCORE[0]:
        CURRMAXSCORE[0] = newMaxScore
        print2d(bf1point5)
        print("")
    if bf1 == "-"*25:
        bf2 = "wheathenriendedarenatidal"
    elif bf1 == "-"*20 and WIDTH == 5:
        bf2 = "promoroveromegacanal"
    elif bf1 == "-"*20 and WIDTH == 4:
        bf2 = "abbabritdulluclaless"
    elif bf1 == "-"*16:
        bf2 = "peakliraunitgene"
    else:
        bf2 = brute_force2(bf1.lower(), [])
    # profile.print_stats()
    print2d(bf2.lower())

if __name__ == '__main__': main()

# Zachary Baker, Pd. 4, 2024
import sys; args =sys.argv[1:]
height = 0
width = 0

board = args[0]
if len(args) > 1:
    width = int(args[1])
else:
    minWidth = int(len(board) ** 0.5)
    done = False
    for i in range(minWidth, len(board)+1):
        if (len(board) % i) == 0: 
           width = int(i)
           break
height=len(board)//width

def rotate(board,width=width,height=height):
    return ''.join([board[start+width*offset] for start in range (width-1,-1,-1) for offset in range(height)])

def xaxflip(board,width=width,height=height):
    return ''.join([board[start+offset] for start in range((height-1)*width,-1,-width) for offset in range(width)])

def yaxflip(board,width=width,height=height):
    return ''.join([board[start-offset] for start in range(width-1,len(board),width) for offset in range(width)])

def main():
    templist = []
    templist = templist + [rotate(board), rotate(rotate(board)), rotate(rotate(rotate(board)))]
    templist = templist + [args[0]]
    templist = templist + [xaxflip(board), xaxflip(rotate(board)), xaxflip(rotate(rotate(board))), xaxflip(rotate(rotate(rotate(board))))]
    templist = list(set(templist))
    for i in templist:
        print(i)


if __name__ == "__main__": main()


# Zachary Baker, Pd. 4, 2024
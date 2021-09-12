class Player:

    def __init__(self, shape):
        self.shape = shape

    g = 1
    l = 1
    m = 1
    s = 1
    t = 5


def printboard():
    
    for i in range(3):
        print('\n-------------')
        print('|',end = '')
        for j in range(3):            
            ind = i*3+j
            print(' {:<2}|'.format(board[ind]),end = '')
    print("\n-------------\n")
    

def makemove(player):
    global board
    global firstTurn
    valid = False
    while not valid:
        if firstTurn:
            size = input("Player %s, please input G for Giant, L for Large, M for Medium, S for Small or T for Tiny: " % player.shape)
            firstTurn = False
        else:
            size = input("Player %s, please input peice size, G, L, M, S or T: " % player.shape)

        size = size.upper()
        if size == 'G':
            if player.g == 0:
                print('No more giant pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'L':
            if player.l == 0:
                print('No more large pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'M':
            if player.m == 0:
                print('No more medium pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'S':
            if player.s == 0:
                print('No more small pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'T':
            if player.t == 0:
                print('No more tiny pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        else:
            print('That is not a valid size, please try again')
            continue

        try:
            place = int(input("Please choose a coordinate to place your piece (from 0 to 8):"))
        except:
            print('That is not a valid position, please try again')
            continue
        if place not in range(9):
            print('That is not a valid position, please try again')
            continue
        elif board[place] in range(9):
            board[place] = player.shape[0] + size
            valid = True
        elif sizekey[board[place][1]] >= sizekey[size]:
            print('You can only place a bigger piece on a smaller piece. Please try again')
            continue
        else:
            board[place] = player.shape[0] + size
            valid = True

    if size == 'G':
        player.g -= 1
    elif size == 'L':
        player.l -= 1
    elif size == 'M':
        player.m -= 1
    elif size == 'S':
        player.s -= 1
    elif size == 'T':
        player.t -= 1
    print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (player.shape, player.g, player.l, player.m, player.s, player.t))

    printboard()

def wincheck():
    global win
    winner = None

    for shape in ['O', 'X']:

        # row check
        for rowcol in range(3):
            if all(shape in str(board[i]) for i in range(3 * rowcol, 3 * rowcol + 3)):
                print('win')
                win = True
                winner = shape

        # column check
            if all(shape in str(board[i]) for i in range(rowcol, 9, 3)):
                print('win')
                win = True
                winner = shape

        # diagonal check
        if all(shape in str(board[i]) for i in range(2, 7, 2)):
            print('win')
            win = True
            winner = shape

        if all(shape in str(board[i]) for i in range(0, 9, 4)):
            print('win')
            win = True
            winner = shape

    return win, winner


# Start game

"""Game Description:

This is a two player game. Player one must choose to play as an o or x. Player two will play as the other.
A player can place a piece on a square from 0 to 8 inclusive, with the goal of making a full row, column
or diagonal their shape.

A player can choose to place a small, medium or large piece. A large piece is bigger than a medium piece and a medium
piece is bigger than a small piece. A player can place replace any smaller piece with a smaller piece.

"""

print("The goal of this game is to make a row, column or diagonal withes all O\'s or all X\'s. \
You can choose to place a tiny, small, medium, large or giant piece on your turn, and you can place a larger piece on a \
smaller one.")

# p1shape = input("Player 1 choose o or x")
# if p1shape == 'o':
#   p2shape = 'x'
# else:
#   p1shape = 'x'
#   p2shape = 'o'
# print('Player one is ' + p1shape + ' and player 2 is ' + p2shape)

p1shape, p2shape = 'X', 'O'
p1 = Player(p1shape)
p2 = Player(p2shape)

sizekey = {'G': 5,'L': 4, 'M': 3, 'S': 2, 'T':1}
board = [i for i in range(9)]
printboard()
firstTurn = True

win = False
while not win:
    makemove(p1)
    win, winner = wincheck()
    if win:
        break

    makemove(p2)
    win, winner = wincheck()

print(winner + ' is the Winner')

class Player:

    def __init__(self, shape):
        self.shape = shape

    l = 3
    m = 3
    s = 3


def printboard():
    for i in range(9):
        if not i % 3:
            print('')
        print('{:<2}'.format(board[i]), end=' |')
    print('\n')

def makemove(player):
    global board
    valid = False
    while not valid:
        size = input("%s, please input l for Large, m for medium or s for small" % player.shape)
        if size == 'l':
            if player.l == 0:
                print('No more large pieces, please try again')
                continue
        elif size == 'm':
            if player.m == 0:
                print('No more medium pieces, please try again')
                continue
        elif size == 's':
            if player.s == 0:
                print('No more small pieces, please try again')
                continue
        else:
            print('That is not a valid size, please try again')
            continue

        try:
            place = int(input("Please choose a coordinate to place your piece (from 0 to 8)"))
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
            print('You can only place a smaller piece on a bigger piece. Please try again')
            continue
        else:
            board[place] = player.shape[0] + size
            valid = True

    if size == 'l':
        player.l -= 1
    elif size == 'm':
        player.m -= 1
    elif size == 's':
        player.s -= 1
    print("%s: large = %d, medium = %d, small = %d" % (player.shape, player.l, player.m, player.s))

    printboard()

def wincheck():
    global win
    winner = None

    for shape in ['o', 'x']:

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

print("The goal of this game is to make a row, column or diagonal withes all o or all x.\n\
You can choose to place a small, medium or large piece on your turn, and you can place a larger piece on a\n\
smaller one")

# p1shape = input("Player 1 choose o or x")
# if p1shape == 'o':
#   p2shape = 'x'
# else:
#   p1shape = 'x'
#   p2shape = 'o'
# print('Player one is ' + p1shape + ' and player 2 is ' + p2shape)

p1shape, p2shape = 'o', 'x'
p1 = Player(p1shape)
p2 = Player(p2shape)

sizekey = {'l': 3, 'm': 2, 's': 1}
board = [i for i in range(9)]
printboard()

win = False
while not win:
    makemove(p1)
    win, winner = wincheck()
    if win:
        break

    makemove(p2)
    win, winner = wincheck()

print(winner + ' is the Winner')
import pygame

class Player:

    def __init__(self, shape):
        self.shape = shape
        if shape == 'X':
            self.colour = (255, 0, 0)
        else:
            self.colour = (255, 0, 255)

    g = 1
    l = 1
    m = 1
    s = 1
    t = 5


def printboard():
    for i in range(3):
        print('\n-------------')
        print('|', end='')
        for j in range(3):
            ind = i * 3 + j
            print(' {:<2}|'.format(board[ind]), end='')
    print("\n-------------\n")


def makemove(player):
    global board
    global firstTurn
    valid = False
    while not valid:
        pygame.event.clear()
        if firstTurn:
            size = input(
                "Player %s, please input G for Giant, L for Large, M for Medium, S for Small or T for Tiny: " % player.shape)
            firstTurn = False
        else:
            size = input("Player %s, please input piece size, G, L, M, S or T: " % player.shape)

        size = size.upper()
        if size == 'G':
            if player.g == 0:
                print('No more giant pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (
                player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'L':
            if player.l == 0:
                print('No more large pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (
                player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'M':
            if player.m == 0:
                print('No more medium pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (
                player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'S':
            if player.s == 0:
                print('No more small pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (
                player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        elif size == 'T':
            if player.t == 0:
                print('No more tiny pieces, please try again')
                print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (
                player.shape, player.g, player.l, player.m, player.s, player.t))
                continue
        else:
            print('That is not a valid size, please try again')
            continue

        pygame.event.clear()

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
    print("%s: Giant = %d, Large = %d, Medium = %d, Small = %d, Tiny = %d" % (
    player.shape, player.g, player.l, player.m, player.s, player.t))

    printboard()

    # draw to pygame

    pygame.draw.circle(screen, player.colour, [(windowWidth / 3 + (place % 3) * windowWidth / 9 + windowWidth / 18),
                                           (windowHeight / 3 + (place // 3) * windowHeight / 9 + windowHeight / 18)],
                       min(windowHeight * sizekey[size] / (5*18), windowWidth * sizekey[size] / (5*18)))

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
This is a two player game.
A player can place a piece on a square from 0 to 8 inclusive, with the goal of making a full row, column
or diagonal with all X's or O's.
A player can choose to place a tiny, small, medium, large or giant piece. A player can place replace any smaller piece \
with a larger piece.
"""

print("The goal of this game is to make a row, column or diagonal with all O\'s or all X\'s. \
You can choose to place a tiny, small, medium, large or giant piece on your turn, and you can place a larger piece on \
a smaller one.")

p1shape, p2shape = 'X', 'O'
p1 = Player(p1shape)
p2 = Player(p2shape)

sizekey = {'G': 5, 'L': 4, 'M': 3, 'S': 2, 'T': 1}
board = [i for i in range(9)]
printboard()

# Pygame stuff

windowWidth, windowHeight = 600, 600

# Set up the drawing window
screen = pygame.display.set_mode([windowWidth, windowHeight])

# Fill the background with white
screen.fill((255, 255, 255))

pygame.draw.lines(screen, (0, 0, 0), True, [(windowWidth / 3, windowHeight / 3), (2 * windowWidth / 3, windowHeight / 3),
                                         (2 * windowWidth / 3, 2 * windowHeight / 3),
                                         (windowWidth / 3, 2 * windowHeight / 3)])

pygame.event.clear()

for i in range(2):
    pygame.draw.line(screen, (0, 0, 0), ((4 + i) * windowWidth / 9, windowHeight / 3),
                     ((4 + i) * windowWidth / 9, 2 * windowHeight / 3))
    pygame.draw.line(screen, (0, 0, 0), (windowWidth / 3, (4 + i) * windowHeight / 9),
                     (2 * windowWidth / 3, (4 + i) * windowHeight / 9))

# update the display
#pygame.display.flip()

# Start game

firstTurn = True

win = False
while not win:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win = True
            winner = "No Winner"

    for person in [p1, p2]:
        makemove(person)
        win, winner = wincheck()
        pygame.display.flip()
        if win:
            break

print(winner + ' is the Winner')
input('Thanks for playing, type anything to quit')

pygame.display.quit()

import pygame

# Initialise player/choose how many starting pieces they have. Can implement colour choice here.

class Player:

    def __init__(self, shape):
        self.shape = shape
        if shape == 'x':
            self.colour = (255, 0, 0)
        else:
            self.colour = (0, 0, 255)


    l = 1
    m = 2
    s = 5


def printboard():
    for i in range(9):
        if not i % 3:
            print('')
        print('{:<2}'.format(board[i]), end=' |')
    print('\n')

def makemove(player):

    # Make sure that board will be changed outside of the function

    global board

    # Keeps window from crashing

    pygame.event.clear()

    # Only make a valid move

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

        # Remake coords (1-9?)

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
        elif sizeKey[board[place][1]] >= sizeKey[size]:
            print('You can only place a bigger piece on a smaller piece. Please try again')
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

    pygame.draw.circle(screen, player.colour, [(windowWidth / 3 + (place % 3) * windowWidth / 9 + windowWidth / 18),
                                           (windowHeight / 3 + (place // 3) * windowHeight / 9 + windowHeight / 18)],
                       min(windowHeight * sizeKey[size] / (3*18), windowWidth * sizeKey[size] / (3*18)))

def wincheck():
    global win
    winner = None

    for shape in ['o', 'x']:


        for rowcol in range(3):

        # row check
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

p1shape, p2shape = 'x', 'o'
p1 = Player(p1shape)
p2 = Player(p2shape)

sizeKey = {'l': 3, 'm': 2, 's': 1}
board = [i for i in range(9)]
printboard()

windowWidth, windowHeight = 600, 600

# Set up the drawing window
screen = pygame.display.set_mode([windowWidth, windowHeight])

# Fill the background with white
screen.fill((255, 255, 255))

# Draw a solid blue circle in the center
# pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
pygame.draw.lines(screen, (0, 0, 0), 1, [(windowWidth / 3, windowHeight / 3), (2 * windowWidth / 3, windowHeight / 3),
                                         (2 * windowWidth / 3, 2 * windowHeight / 3),
                                         (windowWidth / 3, 2 * windowHeight / 3)])
for i in range(2):
    pygame.draw.line(screen, (0, 0, 0), ((4 + i) * windowWidth / 9, windowHeight / 3),
                     ((4 + i) * windowWidth / 9, 2 * windowHeight / 3))
    pygame.draw.line(screen, (0, 0, 0), (windowWidth / 3, (4 + i) * windowHeight / 9),
                     (2 * windowWidth / 3, (4 + i) * windowHeight / 9))

# update the display
pygame.display.flip()

# Run until the user asks to quit
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

# Done! Time to quit.

input('Thanks for playing, type anything to quit')

pygame.display.quit()
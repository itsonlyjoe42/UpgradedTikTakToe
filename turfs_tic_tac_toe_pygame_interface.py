class UserBut:

        def __init__(self,x,y,w,h,text):

            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text

        def draw(self,screen):

            pygame.draw.rect(screen,black,(self.x, self.y, self.w, self.h))
            pygame.draw.rect(screen,grey,(self.x+1, self.y+1, self.w-2, self.h-2))
            textRen = font1.render(self.text,1,black)
            screen.blit(textRen, (self.x+20, self.y+4))


        def isOver(self,x,y):

            overBut = False
            if x > self.x+2 and x< self.x +self.w -2:
                if y > self.y+2 and y < self.y +self.h -2:
                    overBut = True
            return overBut


class Board:

    def __init__(self,rows,cols,x,y,size):
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        self.size = size
        self.width = self.cols*(self.size)
        self.height = self.rows*(self.size)
        self.cells = []

    def draw(self,screen):
        for cellRow in self.cells:
            for cell in cellRow:
                cell.draw(screen)
        for i in range(self.rows + 1):
            pygame.draw.line(screen,black,(self.x,self.y+self.size*i),
                             (self.x+self.width,self.y+self.size*i), cell_border)

        for j in range(self.cols + 1):
            pygame.draw.line(screen,black,(self.x+self.size*j,self.y),
                             (self.x+self.size*j,self.y+self.height), cell_border)


class GameBoard(Board):
        def __init__(self,rows,cols,x,y,size):

                super().__init__(rows,cols,x,y,size)

                for i in range(self.rows):
                    self.cells.append([])
                    for j in range(self.cols):
                        newCell = BoardCell(self.x + self.size*j, self.y + self.size*i, self.size)
                        self.cells[i].append(newCell)

        def drawTurnSq(self, screen):
                 pygame.draw.rect(screen,teamColor[turn],(self.x-5, self.y-5, self.width+10, self.height+10),3)

        def checkWin(self, win, turn, winL1, winL2):
                grid = []

                for i in range(self.cols):
                    grid.append([])
                    for j in range(self.rows):
                        grid[i].append([])
                        if self.cells[i][j].stack:
                            grid[i][j] = self.cells[i][j].stack[-1].team

                gSize = len(grid)
                for team in range(numberOfPlayers):
                    for i in range(gSize):
                        if all((grid[i][j] == team) for j in range(gSize)):

                            turn = team
                            winL1.x = self.cells[i][0].x
                            winL1.y = self.cells[i][0].y+self.cells[i][0].size//2
                            winL2.x = self.cells[i][-1].x+self.cells[i][-1].size
                            winL2.y = winL1.y
                            win = True

                        if all((grid[j][i] == team) for j in range(gSize)):

                            turn = team
                            winL1.x = self.cells[0][i].x+self.cells[i][0].size//2
                            winL1.y = self.cells[0][i].y
                            winL2.x = winL1.x
                            winL2.y = self.cells[-1][i].y+self.cells[-1][i].size
                            win = True

                    if all((grid[j][j] == team) for j in range(gSize)):

                        turn = team
                        winL1.x = self.cells[0][0].x
                        winL1.y = self.cells[0][0].y
                        winL2.x = self.cells[-1][-1].x + self.cells[-1][-1].size
                        winL2.y = self.cells[-1][-1].y + self.cells[-1][-1].size
                        win = True

                    if all((grid[gSize-j-1][j] == team) for j in range(gSize)):

                        turn = team
                        winL1.x = self.cells[-1][0].x
                        winL1.y = self.cells[-1][0].y + self.cells[-1][0].size
                        winL2.x = self.cells[0][-1].x + self.cells[0][-1].size
                        winL2.y = self.cells[0][-1].y
                        win = True

                return (win, turn, winL1, winL2)


class PlayerBoard(Board):
        
        def __init__(self,rows,cols,x,y,size,player):
                super().__init__(rows,cols,x,y,size)
                self.player = player

                for i in range(self.rows):
                    self.cells.append([])
                    for j in range(self.cols):
                        newPiece = Piece(i*self.cols+j+1,self.player)
                        newCell = BoardCell(self.x+self.size*j,self.y+self.size*i,self.size, newPiece)
                        self.cells[i].append(newCell)

        def noPieces(self):
                for cellRow in self.cells:
                    for cell in cellRow:
                        if cell.stack:
                            return False
                return True

class BoardCell:

    def __init__(self,x,y,size,startPiece = None):
        self.x = x
        self.y = y
        self.size= size
        self.selected = False
        self.stack = []
        
        if startPiece:
            self.stack.append(startPiece)
            self.playerCell = True

    def draw(self,screen):
        if self.selected:
            pygame.draw.rect(screen,green,(self.x+selRectOffset,self.y+selRectOffset,
                                           self.size-selRectOffset*2, self.size-selRectOffset*2),1)

        for piece in self.stack:
            if piece:
                pygame.draw.circle(screen,piece.color, (self.x+self.size//2,self.y+self.size//2),
                               (r_unit+piece.size*r_unit//2)-2)
                pygame.draw.circle(screen,(0,0,0) ,(self.x+self.size//2,self.y+self.size//2),
                               (r_unit+piece.size*r_unit//2),2)

    def isOver(self,x,y):
        if self.x < x and self.x+self.size > x:
            if self.y < y and self.y+self.size > y:
                return True
        return False

class Pos():

        def __init__(self, x, y):
                self.x = x
                self.y = y

class Piece:

    def __init__(self,size,team):
        self.size = size
        self.team = team
        self.color = teamColor[team]

def reset():

    global player1board, tacboard,player2board, win, turn

    player1board = PlayerBoard(1,piece_sizes,windowEdge,windowEdge,cell_size,0)
    tacboard = GameBoard(gameSize,gameSize,windowWidth//2-gameSize*cell_size//2,
                         (windowHeight-cell_size)//2-gameSize*cell_size//2, cell_size)
    player2board = PlayerBoard(1,piece_sizes, windowEdge, windowHeight-windowEdge-2*cell_size,
                            cell_size,1)

    win = False

    turn = 0

def redraw():
    screen.fill((255,255,255))
    player1board.draw(screen)
    player2board.draw(screen)
    resetBut.draw(screen)
    tacboard.draw(screen)
    tacboard.drawTurnSq(screen)
    if win:
        pygame.draw.line(screen, green, (winL1.x,winL1.y), (winL2.x, winL2.y),3)
    pygame.display.update()

# Program Start

import pygame
import copy

pygame.init()

windowWidth = 500
windowHeight = 700
windowEdge = 50

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Tic Tac Toe 2.0")

font1 = pygame.font.SysFont('arial',28,1)

red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
black = (0,0,0)
grey = (128,128,128)

teamColor = [red,blue]
gameSize = 3
piece_sizes = 5

cell_size = (windowWidth - (windowEdge*2))//piece_sizes
cell_border = 3

r_unit = cell_size//10

run = True
turn = 0

butWidth = 100
butHeight = 50

winL1 = Pos(None,None)
winL2 = Pos(None,None)

selRectOffset = 3
selectedCell = None

numberOfPlayers = 2

win = False

resetBut = UserBut(windowWidth//2-butWidth//2, windowHeight-windowEdge-butHeight, butWidth, butHeight,"Reset")
player1board = PlayerBoard(1,piece_sizes,windowEdge,windowEdge,cell_size,0)
tacboard = GameBoard(gameSize,gameSize,windowWidth//2-gameSize*cell_size//2, (windowHeight-cell_size)//2-gameSize*cell_size//2,
                        cell_size)
player2board = PlayerBoard(1,piece_sizes, windowEdge, windowHeight-windowEdge-2*cell_size,
                            cell_size,1)

reset()

while run:
    pygame.time.delay(25)
    redraw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            (posx, posy) = event.pos
            if win == False:
                if selectedCell:
                    for cellRow in tacboard.cells:
                        for cell in cellRow:
                            if cell.isOver(posx,posy):

                                if not cell.stack or cell.stack[-1].size > selectedCell.stack[-1].size:
                                    cell.stack.append(selectedCell.stack[-1])
                                    selectedCell.stack.pop()
                                    selectedCell.selected = False
                                    selectedCell = None
                                    turn = (turn + 1)%2
                                    (win, turn, winL1, winL2) = tacboard.checkWin(win, turn, winL1, winL2)
                else:

                    if turn == 0:
                        if player1board.noPieces():
                            for cellRow in tacboard.cells:
                                for cell in cellRow:
                                    if cell.isOver(posx,posy):
                                        if (cell.stack and cell.stack[-1].team == turn):
                                            cell.selected = True
                                            selectedCell = cell
                        else:
                            for cellRow in player1board.cells:
                                for cell in cellRow:
                                    if (cell.isOver(posx,posy)):
                                        cell.selected = True
                                        selectedCell = cell
                    else:
                        if player2board.noPieces():
                            for cellRow in tacboard.cells:
                                for cell in cellRow:
                                    if cell.isOver(posx,posy):
                                        if (cell.stack and cell.stack[-1].team == turn):
                                            cell.selected = True
                                            selectedCell = cell
                        else:
                            for cellRow in player2board.cells:
                                for cell in cellRow:
                                    if cell.isOver(posx,posy):
                                        cell.selected = True
                                        selectedCell = cell

            if resetBut.isOver(posx,posy):
                reset()


pygame.quit()

    

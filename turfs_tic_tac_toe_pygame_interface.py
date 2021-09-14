import pygame
import copy

pygame.init()


windowWidth = 500
windowHeight = 700
windowEdge = 50

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Tic Tac Toe 2.0")

font1 = pygame.font.SysFont('arial',40,1)
font2 = pygame.font.SysFont('arial',28,1)

red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

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


winx1 = None
winy1 = None
winx2 = None
winy2 = None

selRectOffset = 3
selectedCell = None

numberOfPlayers = 2

win = False

class UserBut():
        def __init__(self,x,y,w,h,text):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.text = text
            
        def draw(self,win):
            
            pygame.draw.rect(win,(0,0,0),(self.x, self.y, self.w, self.h))
            pygame.draw.rect(win,(128,128,128),(self.x+1, self.y+1, self.w-2, self.h-2))
            textRen = font2.render(self.text,1,(0,0,0))
            win.blit(textRen, (self.x+20, self.y+4))
            


        def isOver(self,x,y):
            overBut = False
            if x > self.x+2 and x< self.x +self.w -2:
                if y > self.y+2 and y < self.y +self.h -2:
                    overBut = True
            return overBut

class TicBoard:
    
    def __init__(self,rows,cols,x,y,size,player=-1):
        self.rows = rows
        self.cols = cols
        self.player = player
        self.x = x
        self.y = y
        self.size = size
        self.width = self.cols*(self.size) 
        self.height = self.rows*(self.size)
        self.cells = []

        for i in range(self.rows):
            self.cells.append([])
            for j in range(self.cols):
                if self.player>-1:
                    self.cells[i].append(BoardCell(self.x+self.size*j,self.y+self.size*i,self.size,
                                                   Piece(i*self.cols+j+1,self.player)))
                    
                else:
                    self.cells[i].append(BoardCell(self.x+self.size*j,self.y+self.size*i,self.size))
        

    def draw(self,screen):
        for cellRow in self.cells:
            for cell in cellRow:
                cell.draw(screen)
        for i in range(self.rows + 1):
            pygame.draw.line(screen,(0,0,0),(self.x,self.y+self.size*i),
                             (self.x+self.width,self.y+self.size*i), cell_border)

        for j in range(self.cols + 1):
            pygame.draw.line(screen,(0,0,0),(self.x+self.size*j,self.y),
                             (self.x+self.size*j,self.y+self.height), cell_border)
        if self.player==-1:
            pygame.draw.rect(screen,teamColor[turn],(self.x-5, self.y-5, self.width+10, self.height+10),3)
       
    def noPieces(self):
        for cellRow in self.cells:
            for cell in cellRow:
                if cell.stack:
                    return False
        return True

    def checkWin(self):
        grid = []
        global win, winx1, winx2, winy1, winy2, turn
        
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
                    winx1 = self.cells[i][0].x
                    winy1 = self.cells[i][0].y+self.cells[i][0].size//2
                    winx2 = self.cells[i][-1].x+self.cells[i][-1].size
                    winy2 = winy1
                    win = True

                if all((grid[j][i] == team) for j in range(gSize)):
                    
                    turn = team
                    winx1 = self.cells[0][i].x+self.cells[i][0].size//2
                    winy1 = self.cells[0][i].y
                    winx2 = winx1
                    winy2 = self.cells[-1][i].y+self.cells[-1][i].size
                    win = True

            if all((grid[j][j] == team) for j in range(gSize)):
                
                turn = team
                win = True

            if all((grid[gSize-j-1][j] == team) for j in range(gSize)):
                
                turn = team
                win = True
            
                    

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
        

class Piece:

    def __init__(self,size,team):
        self.size = size
        self.team = team
        self.color = teamColor[team]
        

resetBut = UserBut(windowWidth//2-butWidth//2, windowHeight-windowEdge-butHeight, butWidth, butHeight,"Reset")
player1board = TicBoard(1,piece_sizes,windowEdge,windowEdge,cell_size,0)
tacboard = TicBoard(gameSize,gameSize,windowWidth//2-gameSize*cell_size//2, (windowHeight-cell_size)//2-gameSize*cell_size//2,
                        cell_size)
player2board = TicBoard(1,piece_sizes, windowEdge, windowHeight-windowEdge-2*cell_size,
                            cell_size,1)


def reset():
    global player1board, tacboard,player2board, win, turn
    player1board = TicBoard(1,piece_sizes,windowEdge,windowEdge,cell_size,0)
    tacboard = TicBoard(gameSize,gameSize,windowWidth//2-gameSize*cell_size//2, (windowHeight-cell_size)//2-gameSize*cell_size//2,
                        cell_size)
    player2board = TicBoard(1,piece_sizes, windowEdge, windowHeight-windowEdge-2*cell_size,
                            cell_size,1)

    win = False

    turn = 0
    
reset()

def redraw():
    screen.fill((255,255,255))
    player1board.draw(screen)
    global win
    
    player2board.draw(screen)
    resetBut.draw(screen)
    tacboard.draw(screen)
    if win:
        pygame.draw.line(screen, green, (winx1,winy1), (winx2,winy2),3)
    pygame.display.update()
    

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
                                    tacboard.checkWin()
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
    

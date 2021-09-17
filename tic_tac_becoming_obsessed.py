class UserBut: # Custom Button Class 

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


class Board:    # Board Class. Parent of Player Board Class, where pieces begin and Game Board Class where pieces are played. Contains a 2d list of Cell Class Objects

    def __init__(self,rows,cols,x,y):
        
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y        
        self.width = self.cols*(cell_size)
        self.height = self.rows*(cell_size)
        self.cells = []

    def draw(self,screen):
        
        for cellRow in self.cells:  # Draws all cells in it's 2d list
            
            for cell in cellRow:
                
                cell.draw(screen)           
                
        for i in range(self.rows + 1):  # Draws Horizontal Lines of Board
            
            pygame.draw.line(screen,black,(self.x,self.y+cell_size*i),
                             (self.x+self.width,self.y+cell_size*i), cell_border_thickness)

        for j in range(self.cols + 1):  #Draws Vertical Lines of Board
            
            pygame.draw.line(screen,black,(self.x+cell_size*j,self.y),
                             (self.x+cell_size*j,self.y+self.height), cell_border_thickness)


class GameBoard(Board): # Game Board child Class of Board. Contains 2d list of Cells which start without pieces. Has a checkWin method
    
        def __init__(self,rows,cols,x,y):

                super().__init__(rows,cols,x,y)
                
                for i in range(self.rows):
                    
                    self.cells.append([])
                    
                    for j in range(self.cols):
                        
                        newCell = BoardCell(self.x + cell_size*j, self.y + cell_size*i)
                        self.cells[i].append(newCell)

        def draw(self, screen):
            
            super().draw(screen)
            pygame.draw.rect(screen,teamColor[turn],(self.x-5, self.y-5, self.width+10, self.height+10),3) #Gameboard class draws a box around the Board indicating whose go it is.

        def checkWin(self):

                global win, turn, winL1, winL2
                grid = []
                
                for i in range(self.cols):  #Generate a 2d list with the top most team piece represented as an interger, used for Checking Win Conditions
                    
                    grid.append([])
                    
                    for j in range(self.rows):
                        
                        grid[i].append([])
                        
                        if self.cells[i][j].stack:
                            
                            grid[i][j] = self.cells[i][j].stack[-1].team

                gSize = len(grid)
                
                for team in range(numberOfPlayers): 
                    
                    for i in range(gSize):
                        
                        if all((grid[i][j] == team) for j in range(gSize)): #Check rows for win

                            turn = team
                            winL1.x = self.cells[i][0].x
                            winL1.y = self.cells[i][0].y+cell_size//2
                            winL2.x = self.cells[i][-1].x+cell_size
                            winL2.y = winL1.y
                            win = True

                        if all((grid[j][i] == team) for j in range(gSize)): #Check columns for win

                            turn = team
                            winL1.x = self.cells[0][i].x+cell_size//2
                            winL1.y = self.cells[0][i].y
                            winL2.x = winL1.x
                            winL2.y = self.cells[-1][i].y+cell_size
                            win = True

                    if all((grid[j][j] == team) for j in range(gSize)): #Check positive (\) diagonal for win

                        turn = team
                        winL1.x = self.cells[0][0].x
                        winL1.y = self.cells[0][0].y
                        winL2.x = self.cells[-1][-1].x + cell_size
                        winL2.y = self.cells[-1][-1].y + cell_size
                        win = True

                    if all((grid[gSize-j-1][j] == team) for j in range(gSize)): #Check negative (/) diagonal for win

                        turn = team
                        winL1.x = self.cells[-1][0].x
                        winL1.y = self.cells[-1][0].y + cell_size
                        winL2.x = self.cells[0][-1].x + cell_size
                        winL2.y = self.cells[0][-1].y
                        win = True
                    

class PlayerBoard(Board):   # Player board child class of Board. Each cell initiates with a Game Piece of ascending sizes
        
        def __init__(self,rows,cols,x,y,player):
            
                super().__init__(rows,cols,x,y)
                self.player = player
                
                for i in range(self.rows):
                    
                    self.cells.append([])
                    
                    for j in range(self.cols):
                        
                        newCell = BoardCell(self.x+cell_size*j,self.y+cell_size*i)
                        newPiece = Piece(i*self.cols+j+1,self.player, newCell.center.x, newCell.center.y)
                        newCell.stack.append(newPiece)
                        self.cells[i].append(newCell)        


class BoardCell:    # Cell Class has a list functioning as a stack containing Game Pieces. 

    def __init__(self,x,y):
        
        self.x = x
        self.y = y        
        self.stack = []
        self.center= Pos(self.x + cell_size//2,self.y + cell_size//2)
        
        

    def drawActive(self,screen):    # If a game piece was selected from a Cell it is the "Selected Cell", and drawn with a green rectangle
        
        pygame.draw.rect(screen,green,(self.x+selRectOffset,self.y+selRectOffset,
                                           cell_size-selRectOffset*2, cell_size-selRectOffset*2),2)
    def draw(self, screen): # Draw all game pieces in the stack
        
        for piece in self.stack:
            
            if piece:
                
                piece.draw(screen)

    def isOver(self,x,y):   
        
        if self.x < x and self.x+cell_size > x:
            
            if self.y < y and self.y+cell_size > y:
                
                return True
            
        return False


class Pos:

        def __init__(self, x, y):
            
                self.x = x
                self.y = y
                

class Piece:

        def __init__(self, size, team, x, y):
            
                self.size = size
                self.team = team
                self.x = x
                self.y = y
                self.color = teamColor[team]
                self.r = (piece_r_base+self.size*piece_r_inc)

        def draw(self, screen):
            
                pygame.draw.circle(screen,self.color, (self.x, self.y), self.r-2)
                pygame.draw.circle(screen, black,(self.x, self.y), self.r, 3)

        def update(self, pos):
            
                self.x = pos.x
                self.y = pos.y

                
def reset():    # Reset Boards, Pieces, Win status, Turn  status, Moving Piece and Selected Cell variables for new game

    global player1board, tacboard,player2board, win, turn, boards, selectedCell, movingPiece
    
    player1board = PlayerBoard(1,piece_sizes,windowEdge,windowEdge,0)
    tacboard = GameBoard(gameSize,gameSize,windowWidth//2-gameSize*cell_size//2,
                         (windowHeight-cell_size)//2-gameSize*cell_size//2)
    player2board = PlayerBoard(1,piece_sizes, windowEdge, windowHeight-windowEdge-2*cell_size,1)
    boards = [player1board, tacboard, player2board]
    selectedCell = None
    movingPiece = None
    win = False
    turn = 0
    

def redraw():   
    
    screen.fill((255,255,255))
    
    for board in boards:
        
        board.draw(screen)
        
    resetBut.draw(screen)
    
    if win: # If the game has been won, draw a green line through the winning line of peices
        
        pygame.draw.line(screen, green, (winL1.x,winL1.y), (winL2.x, winL2.y),3)
        
    if movingPiece: # If the there is a piece being moved, draw that piece independantly of cells and indicate which cell if came from
        
        movingPiece.draw(screen)
        selectedCell.drawActive(screen)
        
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
gameSize = 3    # The game will be played on a grid gameSize x gameSize
piece_sizes = 5 # The number of pieces and sizes of pieces each player will have

cell_size = (windowWidth - (windowEdge*2))//piece_sizes # The size of each cell of the boards
cell_border_thickness = 3

piece_r_base = cell_size//11 # The base radius of the game pieces
piece_r_inc = cell_size//12 # The incremental difference in radius between game pieces        

run = True
turn = 0

butWidth = 100 # Reset Button Size
butHeight = 50

winL1 = Pos(None,None)  # The Win Line Start and End coordinates, initialised to None
winL2 = Pos(None,None)

selRectOffset = 3   # The interal offset of Rectangle indicatiing the Selected Cell

numberOfPlayers = 2 # May include functionality in the future to support more than 2 players

selectedCell = None
movingPiece = None
win = False

resetBut = UserBut(windowWidth//2-butWidth//2, windowHeight-windowEdge-butHeight, butWidth, butHeight,"Reset")
reset()

while run:  # Game Loop
    
    pygame.time.delay(25)
    
    if win:
        
        movingPiece = None
        
    if movingPiece: # If a piece is being moved, get the mouse postion and update the piece's (x,y) postion to match
        
        (mposx,mposy) = pygame.mouse.get_pos()
        mpos = Pos(mposx, mposy)
        movingPiece.update(mpos)
                
    redraw()    # Redraw the game screen

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            run = False

        if event.type == pygame.MOUSEBUTTONUP:  # If the left mouse button is released
            
            (posx, posy) = event.pos
            
            if win == False:    # If the game hasn't already been Won
                
                if movingPiece:    # If there is a piece being moved
                    
                    if selectedCell.isOver(posx,posy):  # If the mouse is over the selected cell, return piece there & unselect the cell
                        
                        selectedCell.stack.append(movingPiece)
                        selectedCell.stack[-1].update(selectedCell.center)
                        movingPiece = None
                        selectedCell = None
                        
                    else:
                        
                        for cellRow in tacboard.cells:  # If the mouse is not over the selected cell, check the gameboard
                            
                            for cell in cellRow:
                                
                                if cell.isOver(posx,posy):  #If the mouse is over a gameboard cell

                                    if not cell.stack or cell.stack[-1].size > movingPiece.size:    #If the cell has no pieces or it's top piece is bigger than the moving piece
                                        
                                        cell.stack.append(movingPiece)  
                                        cell.stack[-1].update(cell.center)
                                        movingPiece = None
                                        selectedCell = None                                        
                                        turn = (turn + 1)%2
                                        tacboard.checkWin() #Add the moving piece to the top of the cell stack, updates the pieces position to the center of the cell, advance the turn count and check for a win condition
                                        
                else:
                    
                        for board in boards:    # If there is no piece being moved, check all cells on all boards
                            
                            for cellRow in board.cells:
                                
                                for cell in cellRow:    
                                    
                                    if cell.isOver(posx,posy):  #If the mouse is over a cell
                                        
                                        if (cell.stack and cell.stack[-1].team == turn):    #If the cell contain a peice and the top piece can be moved on this turn
                                            
                                            movingPiece = cell.stack[-1]
                                            cell.stack.pop()
                                            selectedCell = cell
                                            tacboard.checkWin() # The top piece becomes the moving piece, the cell becomes the selected cell and check for win conditions                        

            if resetBut.isOver(posx,posy):  # If the mouse is over the reset button, reset the game
                
                reset()

pygame.quit()

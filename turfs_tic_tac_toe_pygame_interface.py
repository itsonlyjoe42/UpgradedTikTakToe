import pygame
import copy

pygame.init()


windowWidth = 500
windowHeight = 600
windowEdge = 50

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Tic Tac Toe 2.0")

font1 = pygame.font.SysFont('arial',40,1)
font2 = pygame.font.SysFont('arial',28,1)

red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

teamColor = [red,blue]

piece_sizes = 5

cell_size = (windowWidth - (windowEdge*2))//piece_sizes #460/5 = 92
cell_border = 3

r_unit = cell_size//12

run = True
turn = 0

selRectOffset = 3
selectedCell = None

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
                               r_unit+piece.size*r_unit//2)

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
        
 
player1board = TicBoard(1,piece_sizes,windowEdge,windowEdge,cell_size,0)
tacboard = TicBoard(3,3,windowWidth//2-3*cell_size//2, windowHeight//2-3*cell_size//2,
                    cell_size)
player2board = TicBoard(1,piece_sizes, windowEdge, windowHeight-windowEdge-cell_size,
                        cell_size,1)



def redraw():
    screen.fill((255,255,255))
    player1board.draw(screen)
    
    player2board.draw(screen)
    tacboard.draw(screen)
    pygame.display.update()
    

while run:
    pygame.time.delay(25)   
    redraw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            (posx, posy) = event.pos
           
            for cellRow in player1board.cells:
                for cell in cellRow:
                    if (cell.isOver(posx,posy)):
                        cell.selected = True
                        if selectedCell:
                            selectedCell.selected = False
                        selectedCell = cell
            for cellRow in player2board.cells:
                for cell in cellRow:
                    if cell.isOver(posx,posy):
                        cell.selected = True
                        if selectedCell:
                            selectedCell.selected = False
                        selectedCell = cell
        
            
            if selectedCell:
                for cellRow in tacboard.cells:
                    for cell in cellRow:
                        if cell.isOver(posx,posy):
                            selectedCell.selected = False
                            cell.stack.append(selectedCell.stack[-1])
                            selectedCell.stack.pop()
                            selectedCell = None
       
pygame.quit()
    

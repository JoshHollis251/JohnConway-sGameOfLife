import sys
from turtle import width
import pygame
import math
from queue import PriorityQueue
import copy

WINWIDTH = 800
WINHEIGHT = 800

BLACK = (50, 50, 50)
TURQUOISE = (72,209,204)
WHITE = (150, 150, 150)
PURPLE = (144, 110, 255)

WINDOW = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption("John Conway's Game of Life")
pygame.init()
clock = pygame.time.Clock()

class Node:
   def __init__(self, row, col, width, height, totalRows, totalCols):
      self.row = row
      self.col = col
      self.x = row * width
      self.y = col * height
      self.color = BLACK
      self.neighbors = []
      self.width = width
      self.height = height
      self.totalRows = totalRows
      self.totalCols = totalCols
   
   def get_pos(self):
      return self.row, self.col
   
   def is_filled(self):
      if self.color == TURQUOISE:
         return 1
      else:
         return 0 
   
   def reset(self):
      self.color = BLACK
      
   def fillSquare(self):
      self.color = TURQUOISE
      
   def draw(self, WIN):
      pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height))
              
   def __lt__(self, other):
      return False

   
def makeGrid(rows, cols):
   grid = []
   xsize = WINWIDTH // cols
   ysize = WINHEIGHT // rows  
   for i in range(cols):
      grid.append([])
      for j in range(rows):
         node = Node(i, j, xsize, ysize, rows, cols)
         grid[i].append(node) 
   
   return grid
   
def drawGrid(WIN, rows, cols):
   xsize = WINWIDTH // cols
   ysize = WINHEIGHT // rows
   for i in range(rows):
      pygame.draw.line(WIN, WHITE, (0, i * ysize), (WINWIDTH, i * ysize))
      for j in range(cols):
         pygame.draw.line(WIN, WHITE, (j * xsize, 0), (j * xsize, WINHEIGHT))
         
def draw(WIN, grid, rows, cols):
   WIN.fill(WHITE)
   
   for row in grid:
      for node in row:
         node.draw(WIN)
   
   drawGrid(WIN, rows, cols)
   pygame.display.update()
   
def getClickedPos(xpos, ypos, rows, cols):
   xsize = WINWIDTH // cols
   ysize = WINHEIGHT // rows
   
   row = ypos // ysize
   col = xpos // xsize
   
   return row, col

def updateNeighbors(grid, rows, cols):
   GCopy = copy.deepcopy(grid)
   neighborCount = 0
   for x in range(cols):
      for y in range(rows):
         
         neighborCount = int(grid[x][ (y-1)%rows].is_filled() + grid[x][ (y+1)%rows].is_filled() +
                             grid[(x-1)%cols][ y].is_filled() + grid[(x+1)%cols][ y].is_filled() +
                             grid[(x-1)%cols][ (y-1)%rows].is_filled() + grid[(x-1)%cols][ (y+1)%rows].is_filled() +
                             grid[(x+1)%cols][ (y-1)%rows].is_filled() + grid[(x+1)%cols][ (y+1)%rows].is_filled() )
         node = grid[x][y]
         if node.is_filled() == 1:
            if neighborCount == 2 or neighborCount == 3:
               GCopy[x][y].fillSquare()
            else: 
               GCopy[x][y].reset()
         else:
            if neighborCount == 3:
               GCopy[x][y].fillSquare()
            else:
               GCopy[x][y].reset()
               grid[0]  
   return GCopy

def main(WIN):
   ROWS = 25
   COLS = 25
   pause = False
   grid = makeGrid(ROWS, COLS)
   while True:
      while pause == True: #paused logic
         grid = updateNeighbors(grid, ROWS, COLS)
         draw(WIN, grid, ROWS, COLS)
         for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                  pause = False

      while pause == False: #paused logic
         draw(WIN, grid, ROWS, COLS)
         for event in pygame.event.get():

            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
               
            if event.type == pygame.KEYDOWN: #space bar pause
                  if event.key == pygame.K_SPACE:
                     pause = True

            if pygame.mouse.get_pressed()[0]: #left click
               ypos, xpos = pygame.mouse.get_pos()
               row, col = getClickedPos(xpos, ypos, ROWS, COLS)
               node = grid[row][col]
               node.fillSquare()

            if pygame.mouse.get_pressed()[2]: #right click
               ypos, xpos = pygame.mouse.get_pos()
               row, col = getClickedPos(xpos, ypos, ROWS, COLS)
               node = grid[row][col]
               node.reset()
                
main(WINDOW)
   
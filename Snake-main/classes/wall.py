import pygame,os
from pygame.math import Vector2

cwd = os.getcwd()
cell_size = 40
cell_number = 20

class WALL:
    def __init__(self,screen):
        self.body = []
        self.screen = screen
        self.middle_wall =pygame.image.load(cwd+'/Snake-main/Graphics/middle_wall.png').convert_alpha()


    def dynamicWall(self,grid):
        for yCount,i in enumerate(grid):
            for xCount,x in enumerate(i):
                if x == 1:
                    self.body.append(Vector2(xCount,yCount))

    def create_Wall(self):
         for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            wall_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            self.screen.blit(self.middle_wall, wall_rect)

    def deleteWall(self):
        self.body = []

    #Check if apple is same position as wall
    def checkCollision(self,pos):
        for block in self.body:
            if block == pos:
                return True
            
     #Check if snake collision with wall       
    def checkSnakeCollision(self,snake_head):
        for w in self.body:
            wallRect =(pygame.Rect(int(w[0] * cell_size) ,int(w[1] * cell_size),cell_size, cell_size))
            if snake_head.colliderect(wallRect):
                return True
            
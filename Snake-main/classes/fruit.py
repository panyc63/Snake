from pygame.math import Vector2
import pygame, random,os

cwd = os.getcwd()
cell_size = 40
cell_number = 20


class FRUIT:
    def __init__(self,screen):
        self.screen = screen
        self.pos = Vector2(0,0)
        self.randomize()
        self.apple2 =pygame.image.load(cwd+'/Snake-main/Graphics/apple2.png').convert_alpha()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        self.screen.blit(self.apple2, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

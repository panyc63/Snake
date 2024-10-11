import pygame

cell_size = 40
cell_number = 20

class BULLET:
    def __init__(self, position, direction,screen):
        self.screen = screen
        self.position = position
        self.direction = direction
        self.speed = 0.2  # Adjust the speed as needed
        self.radius = cell_size // 4  # Smaller circle
        self.color = (0, 0, 255)  # BLUE color

    def move(self):
        
        self.position += self.direction * self.speed

    def draw_bullet(self):
        # Draw the bullet as a small circle
        pixel_position = (int(self.position.x * cell_size), int(self.position.y * cell_size))
        pygame.draw.circle(self.screen, self.color, pixel_position, self.radius)
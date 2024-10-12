import pygame,os
import tkinter as tk
from tkinter import filedialog
import json


cwd = os.getcwd()
cell_size = 40
cell_number = 20

class mapEditting:
    def __init__(self,screen):
        root = tk.Tk()
        root.withdraw()
        self.screen = screen
        self.WIDTH = cell_size*cell_number
        self.HEIGHT = cell_size*cell_number
        self.TILE_SIZE = 40
        self.GRID_WIDTH = self.WIDTH // self.TILE_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.TILE_SIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.background_image = pygame.image.load(cwd+'/Snake-main/Graphics/background.jpg').convert()


    def createMap(self):
        global customGrid
        running = True
        dragging = False
        draggingDelete = False
        while running:
            self.screen.fill(self.BLACK)
            self.screen.blit(self.background_image, (0, 0))  # Draw the background image

            self.drawGrid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click to place a tile
                        dragging = True
                        x, y = event.pos
                        self.grid[y // self.TILE_SIZE][x // self.TILE_SIZE] = 1  # Place a tile
                    elif event.button == 3:  # Right click to remove a tile
                        draggingDelete = True
                        x, y = event.pos
                        self.grid[y // self.TILE_SIZE][x // self.TILE_SIZE] = 0  # Remove a tile
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    draggingDelete = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Save map
                        customGrid = self.save_map()
                        running = False
                    elif event.key == pygame.K_b:
                        running = False

                if dragging:
                    circle_pos = pygame.mouse.get_pos()
                    x =circle_pos[1]             
                    y = circle_pos[0]
                    self.grid[x // self.TILE_SIZE][y// self.TILE_SIZE] = 1
                if draggingDelete:
                    circle_pos = pygame.mouse.get_pos()
                    x =circle_pos[1]             
                    y = circle_pos[0]
                    self.grid[x // self.TILE_SIZE][y// self.TILE_SIZE] = 0

            pygame.display.flip()
    def loadSpecificMap(self,mapName):
        with open(cwd+"/Snake-main/"+mapName, 'r') as f:
            grid = json.load(f)
        return grid

    #Load Custom Map
    def loadMap(self):
        global selected_map_name
        file_path = filedialog.askopenfilename(title="Select a Map File", filetypes=[("JSON files", "*.json")])
        self.selected_map_name = os.path.basename(file_path)
        if file_path:  # Check if a file was selected
            with open(file_path, 'r') as file:
                customGrid = json.load(file)

            return customGrid
        else:
            return None
    
    
    def save_map(self):
        global selected_map_name
        file_path = filedialog.asksaveasfilename(
        title="Save File",
        defaultextension=".json",  # Default file extension
        filetypes=[("json", "*.json"), ("All files", "*.*")]  # File type options
    )   
        try:
            self.selected_map_name = os.path.basename(file_path)
            with open(file_path, 'w') as f:
                json.dump(self.grid, f)
            return self.grid
        except FileNotFoundError:
            pass

    def drawGrid(self):
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                # Only draw the outline, no fill
                if self.grid[y][x] == 1:  # Filled
                    pygame.draw.rect(self.screen, self.RED, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)  # Draw the outline of the square
              
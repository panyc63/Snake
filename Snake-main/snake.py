import pygame, sys, random ,os
from pygame.math import Vector2
import sqlitecloud
from classes.snakeClass import SNAKE 
from classes.bullet import BULLET
from classes.fruit import FRUIT
from classes.wall import WALL 
from classes.mapEditting import mapEditting


# Constants
cell_size = 40
cell_number = 20
cwd = os.getcwd()
class scores:
    ApiKey  = 'EGjpcL3ZfSkxt9dL8y2sQkJCreUD69vmX9a6bpaa3M4'
    highscore = 0

main_menu = 0
playing = 1
game_end = 2
paused = 3
overlay=4
grid = []
customGrid =[]
game_state = main_menu

button_colour = (100, 100, 255)
hover_colour = (150, 150, 255)
font_colour = (0, 0, 0)
#font = pygame.font.SysFont(None, 25, True)

screen = pygame.display.set_mode()
pygame.display.set_caption("Snake Attack")

# Button dimensions and positions
button_width = 300
button_height = 50
start_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 360), (button_width, button_height))
mapSetting_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 420), (button_width, button_height))
leaderscore_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 480), (button_width, button_height))
quit_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 540), (button_width, button_height))


def gameDifficulty():
    
    #Game Difficulty screen
    global game_state,grid,customGrid,selected_map_name
    gameDifficulty = True
    mapE = mapEditting(screen)
    selected_map_name = ""

    while gameDifficulty:
        screen.blit(game_menu_image, (0, 0))  # Set the background
        mouse_pos = pygame.mouse.get_pos()
        map1_button_rect = pygame.Rect((100, 400), (button_width/2, button_height))
        map2_button_rect = pygame.Rect((300, 400), (button_width/2, button_height))

        map3_button_rect = pygame.Rect((500, 400), (button_width/2, button_height))

        map4_button_rect = pygame.Rect((50, 480), (button_width/2, button_height))
        map5_button_rect = pygame.Rect((250, 480), (button_width/2, button_height))

        customMap_button_rect = pygame.Rect((450, 480), (button_width, button_height))
        backMap_button_rect = pygame.Rect((cell_size * cell_number // 2 - button_width // 2, 600), (button_width, button_height))



        map1_hovered = map1_button_rect.collidepoint(mouse_pos)
        map2_hovered = map2_button_rect.collidepoint(mouse_pos)
        map3_hovered = map3_button_rect.collidepoint(mouse_pos)
        map4_hovered = map4_button_rect.collidepoint(mouse_pos)
        map5_hovered = map5_button_rect.collidepoint(mouse_pos)
        customMap_hovered = customMap_button_rect.collidepoint(mouse_pos)
        backButtonMap_hovered = backMap_button_rect.collidepoint(mouse_pos)


        draw_button(map1_button_rect, "Map 1", map1_hovered)
        draw_button(map2_button_rect, "Map 2", map2_hovered) 
        draw_button(map3_button_rect, "Map 3", map3_hovered) 
        draw_button(map4_button_rect, "Map 4", map4_hovered) 
        draw_button(map5_button_rect, "Map 5", map5_hovered) 
        draw_button(customMap_button_rect, "Custom Map", customMap_hovered) 
        draw_button(backMap_button_rect, "Back", backButtonMap_hovered) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backMap_button_rect.collidepoint(mouse_pos):
                    gameDifficulty = False  # Exit map settings
                    game_state = main_menu  # Go back to the main menu
                elif map1_button_rect.collidepoint(mouse_pos):
                    grid = mapE.loadSpecificMap("map1.json")
                    selected_map_name = "Map 1"
                    game_state = overlay
                    gameDifficulty = False
                elif map2_button_rect.collidepoint(mouse_pos):
                    grid = mapE.loadSpecificMap("map2.json")
                    selected_map_name = "Map 2"
                    game_state = overlay
                    gameDifficulty = False

                elif map3_button_rect.collidepoint(mouse_pos):
                    grid = mapE.loadSpecificMap("map3.json")
                    selected_map_name = "Map 3"
                    game_state = overlay
                    gameDifficulty = False
                elif map4_button_rect.collidepoint(mouse_pos):
                    grid = mapE.loadSpecificMap("map4.json")
                    selected_map_name = "Map 4"
                    game_state = overlay
                    gameDifficulty = False
                elif map5_button_rect.collidepoint(mouse_pos):
                    grid = mapE.loadSpecificMap("map5.json")
                    selected_map_name = "Map 5"
                    game_state = overlay
                    gameDifficulty = False

                elif customMap_button_rect.collidepoint(mouse_pos):
                    if not customGrid:
                        grid = mapE.loadMap()
                        customGrid = grid
                        game_state = overlay
                        gameDifficulty = False
                    elif not customGrid == []:
                        grid = customGrid                            
                        game_state = overlay
                        gameDifficulty = False

        pygame.display.flip()      

def mapSetting():

    #Map Setting screen
    global game_state,customGrid
    mapEdit = True
    mapE = mapEditting(screen)

    while mapEdit:
        screen.blit(background_image, (0, 0))  # Set the background
        mouse_pos = pygame.mouse.get_pos()
        loadMap_button_rect = pygame.Rect((cell_size * cell_number // 2 - button_width // 2, 420), (button_width, button_height))
        createMap_button_rect = pygame.Rect((cell_size * cell_number // 2 - button_width // 2, 480), (button_width, button_height))
        backMap_button_rect = pygame.Rect((cell_size * cell_number // 2 - button_width // 2, 540), (button_width, button_height))

        loadMap_hovered = loadMap_button_rect.collidepoint(mouse_pos)
        createMap_hovered = createMap_button_rect.collidepoint(mouse_pos)
        backButtonMap_hovered = backMap_button_rect.collidepoint(mouse_pos)
        screen.blit(map_Instruction,(50,60))
        draw_button(loadMap_button_rect, "Load Map", loadMap_hovered) 
        draw_button(createMap_button_rect, "Create Map", createMap_hovered) 
        draw_button(backMap_button_rect, "Back", backButtonMap_hovered) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if backMap_button_rect.collidepoint(mouse_pos):
                    mapEdit = False  # Exit map settings
                    game_state = main_menu  # Go back to the main menu
                elif loadMap_button_rect.collidepoint(mouse_pos):
                    # Implement load map functionality here
                    customGrid = mapE.loadMap()
                    mapEdit = False  # Exit map settings
                    game_state = main_menu  # Go back to the main menu
                elif createMap_button_rect.collidepoint(mouse_pos):
                    # Implement create map functionality here
                    mapE.createMap()

        pygame.display.flip()      

# Function to draw the leaderboard table
def draw_leaderboard():
    high_scores = fetch_high_scores()  # Get high scores from SQLite Cloud

    # Draw the header
    header_font = pygame.font.Font(cwd + '/Snake-main/Font/PoetsenOne-Regular.ttf', 30)
    header_surface = header_font.render("Leaderboard", True, (0, 0, 0))
    screen.blit(header_surface, (cell_size * cell_number // 2 - header_surface.get_width() // 2, 50))

    # Define table dimensions
    table_width = cell_size * cell_number / 1.5
    row_height = 40
    table_x = (cell_size * cell_number - table_width) // 2  # Center the table
    table_y = 100  # Moved down by 20 pixels
    cell_width = table_width / 2  # Two columns: Username and Score
    rank_width = 80  # Increased width for the rank column

    # Draw the border for the table
    pygame.draw.rect(screen, (0, 0, 0), (table_x, table_y, table_width, row_height + len(high_scores) * 30), 2)

    # Draw the table header
    rank_header_surface = game_font.render("Rank", True, (0, 0, 0))
    username_header_surface = game_font.render("Username", True, (0, 0, 0))
    score_header_surface = game_font.render("Score", True, (0, 0, 0))
    screen.blit(rank_header_surface, (table_x + 10, table_y + 10))
    screen.blit(username_header_surface, (table_x + rank_width + 10, table_y + 10))  # Adjusted position
    screen.blit(score_header_surface, (table_x + rank_width + cell_width + 10, table_y + 10))

    # Draw the vertical lines separating columns
    pygame.draw.line(screen, (0, 0, 0), (table_x + rank_width, table_y), 
                     (table_x + rank_width, table_y + row_height + len(high_scores) * 30), 2)
    pygame.draw.line(screen, (0, 0, 0), (table_x + rank_width + cell_width, table_y), 
                     (table_x + rank_width + cell_width, table_y + row_height + len(high_scores) * 30), 2)

    # Draw rows and their borders
    for index, (username, score) in enumerate(high_scores):
        row_y = table_y + row_height + index * 30
        # Draw row border
        pygame.draw.rect(screen, (0, 0, 0), (table_x, row_y, table_width, 30), 1)

        # Fit text in cells
        rank_surface = game_font.render(str(index + 1), True, (0, 0, 0))  # Rank number
        username_surface = game_font.render(username, True, (0, 0, 0))
        score_surface = game_font.render(str(score), True, (0, 0, 0))
        
        # Center rank numbers
        rank_x = table_x + (rank_width - rank_surface.get_width()) // 2
        screen.blit(rank_surface, (rank_x, row_y + 5))  # Centered rank number
        screen.blit(username_surface, (table_x + rank_width + 10, row_y + 5))  # Adjust vertical alignment
        screen.blit(score_surface, (table_x + rank_width + cell_width + 10, row_y + 5))  # Adjust vertical alignment

    # Draw bottom border
    pygame.draw.rect(screen, (0, 0, 0), (table_x, table_y + row_height + len(high_scores) * 30 - 2, table_width, 2))  # Bottom border


# Function to display the leaderboard and scores
def display_leaderboard():
    global game_state
    leaderboard_active = True

    while leaderboard_active:
        screen.blit(background_image, (0, 0))  # Set the background
        draw_leaderboard()  # Call function to draw the leaderboard

        # Button for going back to the main menu
        back_button_rect = pygame.Rect((cell_size * cell_number // 2 - button_width // 2, 540), (button_width, button_height))
        draw_button(back_button_rect, "Back", False)  # No hover effect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    leaderboard_active = False  # Exit leaderboard display
                    game_state = main_menu  # Go back to the main menu

        pygame.display.flip()

# Add a function to fetch high scores from the SQLite database
def fetch_high_scores():
    conn = sqlitecloud.connect(f"sqlitecloud://cjmouemghk.sqlite.cloud:8860?apikey={scores.ApiKey}")
    conn.execute(f"USE DATABASE my-database")
    cursor = conn.execute("SELECT username, score FROM scores ORDER BY score DESC LIMIT 10")
    high_scores = cursor.fetchall()
    conn.close()
    return high_scores

# Uploads Username and Score to sqlitecloud
def upload_score(username):
    # Assuming you have a variable that holds the current score
    current_score = scores.highscore

    # Create a connection to SQLite Cloud
    conn = sqlitecloud.connect(f"sqlitecloud://cjmouemghk.sqlite.cloud:8860?apikey={scores.ApiKey}")
    conn.execute(f"USE DATABASE my-database")

    # Create the scores table if it does not exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    # Insert the score into the database
    conn.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, current_score))
    conn.commit()
    conn.close()

    print("Score uploaded successfully.")

#Main menu screen
def main_menu_screen():

    global game_state,grid

    game_menu = True

    while game_menu:
        screen.blit(game_menu_image, (0, 0))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over any button
        start_hovered = start_button_rect.collidepoint(mouse_pos)
        mapSettings_hovered = mapSetting_button_rect.collidepoint(mouse_pos)
        leaderscore_hovered = leaderscore_button_rect.collidepoint(mouse_pos)
        quit_hovered = quit_button_rect.collidepoint(mouse_pos)

        # Hover effects
        draw_button(start_button_rect, "Start", start_hovered)
        
        draw_button(mapSetting_button_rect, "Map Settings", mapSettings_hovered)
        draw_button(leaderscore_button_rect, "Highscore", leaderscore_hovered)
        draw_button(quit_button_rect, "Quit", quit_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #Check if button was pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                #If Start Button was pressed
                if start_button_rect.collidepoint(mouse_pos):
                    print("Start button clicked")
                    gameDifficulty()
                    game_menu = False

                    #If Settings Button was pressed
                elif mapSetting_button_rect.collidepoint(mouse_pos):
                    print("Map Settings button clicked")
                    mapSetting()
                    game_menu = False
                #If Leaderscore Button was pressed
                elif leaderscore_button_rect.collidepoint(mouse_pos):
                    display_leaderboard()
                    print("Leaderscore button clicked")
                #If Quit Button was pressed
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def draw_button(rect, text, is_hovered):

    # Choose color based on hover state
    color = hover_colour if is_hovered else button_colour
    pygame.draw.rect(screen, color, rect)
    # Draw text on top of the button
    text_surf = game_font.render(text, True, font_colour)
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

#Pause Menu
def pause_menu_screen():
    global game_state
    pause_menu_active = True

    if main_game.paused_time is None:  # Only set this the first time the game is paused
        main_game.paused_time = pygame.time.get_ticks()

    # Tinted screen when paused
    tint_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size), pygame.SRCALPHA)
    tint_surface.fill((0, 0, 0, 150))  

    # Button dimensions and positions
    button_width = 200
    button_height = 50
    resume_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 300), (button_width, button_height))
    restart_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 360), (button_width, button_height))
    menu_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 420), (button_width, button_height))

    while pause_menu_active:
        # Keep the game elements drawn in the background
        main_game.draw_elements()

        # Apply the tinted overlay to give a "paused" effect
        screen.blit(tint_surface, (0, 0))

        # Render the "PAUSED" text
        paused_text_surface = game_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(paused_text_surface, (cell_number * cell_size // 2 - paused_text_surface.get_width() // 2, 160))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        resume_hovered = resume_button_rect.collidepoint(mouse_pos)
        restart_hovered = restart_button_rect.collidepoint(mouse_pos)
        menu_hovered = menu_button_rect.collidepoint(mouse_pos)

        draw_button(resume_button_rect, "Resume", resume_hovered)
        draw_button(restart_button_rect, "Retry", restart_hovered)
        draw_button(menu_button_rect, "Main Menu", menu_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(mouse_pos):
                    current_time = pygame.time.get_ticks()
                    # Add the pause duration to the total paused time
                    main_game.total_paused_duration += current_time - main_game.paused_time
                    main_game.paused_time = None  # Reset paused time
                    game_state = playing  # Resume game
                    pause_menu_active = False
                elif restart_button_rect.collidepoint(mouse_pos):
                    main_game.snake.reset()
                    main_game.bullets = []  # Reset bullets
                    game_state = playing
                    pause_menu_active = False
                elif menu_button_rect.collidepoint(mouse_pos):
                    main_game.reset()
                    game_state = main_menu  # Return to main menu
                    pause_menu_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # If "P" is pressed again, resume the game
                    current_time = pygame.time.get_ticks()
                    main_game.total_paused_duration += current_time - main_game.paused_time
                    main_game.paused_time = None  # Reset paused time
                    game_state = playing
                    pause_menu_active = False

        pygame.display.flip()
        
#End Game Screen

def end_game_screen():
    global game_state
    username_input = ""
    submit_enabled = True

    # Tinted death screen
    tint_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size), pygame.SRCALPHA)
    tint_surface.fill((190, 0, 0, 100))

    # Retry & Quit buttons
    button_width = 200
    button_height = 50
    restart_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 340), (button_width, button_height))
    menu_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 400), (button_width, button_height))
    quit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 460), (button_width, button_height))

    # Move the input box and submit button lower
    input_box_y_position = 540  # Moved down by 20 pixels
    input_box = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position), (button_width, button_height))
    submit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position + button_height + 10), (button_width, button_height))

    end_screen = True

    while end_screen:
        
        screen.blit(background_image, (0, 0))
        screen.blit(tint_surface, (0, 0))
        screen.blit(game_over_image, (cell_number * cell_size // 2 - game_over_image.get_width() // 2, 160))

        # Draw the "Submit High Score?" text
        submit_text_surface = game_font.render("Submit High Score?", True, (255, 255, 255))
        screen.blit(submit_text_surface, (cell_number * cell_size // 2 - submit_text_surface.get_width() // 2, input_box.y - 30))

        # Draw the input box
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        input_text_surface = game_font.render(username_input, True, (0, 0, 0))
        screen.blit(input_text_surface, (input_box.x + 5, input_box.y + 5))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over buttons
        restart_hovered = restart_button_rect.collidepoint(mouse_pos)
        menu_hovered = menu_button_rect.collidepoint(mouse_pos)
        quit_hovered = quit_button_rect.collidepoint(mouse_pos)
        submit_hovered = submit_button_rect.collidepoint(mouse_pos)

        # Hover effects
        draw_button(restart_button_rect, "Retry", restart_hovered)
        draw_button(menu_button_rect,"Back to Menu", menu_hovered)
        draw_button(quit_button_rect, "Quit", quit_hovered)

        if submit_enabled:
            draw_button(submit_button_rect, "Submit", submit_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(mouse_pos):
                    main_game.snake.reset()
                    main_game.bullets = []
                    main_game.health = 5
                    game_state = playing
                    end_screen = False
                elif menu_button_rect.collidepoint(mouse_pos):
                    game_state = main_menu
                    main_game.snake.reset()
                    end_screen = False
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif submit_enabled and submit_button_rect.collidepoint(mouse_pos):
                    if username_input:  
                        upload_score(username_input)  
                        submit_enabled = False  

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if submit_enabled and username_input:  
                        upload_score(username_input)
                        submit_enabled = False
                else:
                    username_input += event.unicode

        pygame.display.flip()




class MAIN:
    def __init__(self):
        self.snake = SNAKE(screen)
        self.fruit = FRUIT(screen)
        self.wall = WALL(screen)
        self.bullets = []
        self.health = 5  # Player starts with 5 health points
        #get time of inititation which is 0 when starting
        self.last_bullet=pygame.time.get_ticks()
        self.start_time = None  
        self.game_started = False # used to check if game has started(player moved)
        self.last_fruit_time = None 
        self.paused_time = None  # Track when the game was paused
        self.total_paused_duration = 0  # Track the total time spent paused


    def update(self):
        self.snake.move_snake()
        self.update_bullets()
        self.check_eat()
        self.checkWallCollisions()        
        self.check_fail()
        self.spawn_startbullet()

        if self.game_started:


            if game_state == paused:
                return

            current_time = pygame.time.get_ticks() - self.total_paused_duration
            
            if self.paused_time is not None:
                self.last_fruit_time = current_time

            if self.last_fruit_time is None:
                self.last_fruit_time = current_time  # start the fruit timer on first movement

            # Check if 5 seconds have passed since last fruit eaten
            if current_time - self.last_fruit_time >= 5000:  # 5 seconds in milliseconds
                self.health -= 1  # Decrease health by 1
                self.last_fruit_time = current_time  # Reset the timer
                if self.health <= 0:
                    self.game_over()

#make sure the bullet only spawn when snake move
    def spawn_startbullet(self):
        if self.snake.direction != Vector2(0, 0):
            C_time = pygame.time.get_ticks()
            #after passing 2 second and spawn bullet
            if C_time - self.last_bullet >= 2000:
                self.spawn_bullet()
                #reset time to current, make it 0 again
                self.last_bullet = C_time
        
    def update_bullets(self):
        wallRect = []
        for w in self.wall.body:
            wallRect.append(pygame.Rect(int(w[0] * cell_size) ,int(w[1] * cell_size),cell_size, cell_size))
        for bullet in self.bullets[:]:
            bullet.move()
            # Remove bullet once out of map
            if bullet.position.x < 0 or bullet.position.x >= cell_number or bullet.position.y < 0 or bullet.position.y >= cell_number:
                self.bullets.remove(bullet)
            else:
                # Check collision with snake head
                bullet_rect = pygame.Rect(int(bullet.position.x * cell_size - bullet.radius),
                                          int(bullet.position.y * cell_size - bullet.radius),
                                          bullet.radius * 2, bullet.radius * 2)
                snake_head_rect = pygame.Rect(int(self.snake.body[0].x * cell_size),
                                              int(self.snake.body[0].y * cell_size),
                                              cell_size, cell_size)                           
                

                if bullet_rect.colliderect(snake_head_rect):
                    self.health -= 1  # Reduce health by 1
                    self.bullets.remove(bullet)  # Remove the bullet
                    if self.health <= 0:
                        self.game_over()  # Trigger game over if health reaches 0
                
                for w in wallRect:
                    if bullet_rect.colliderect(w):
                        self.bullets.remove(bullet)
                        break



                        
    def checkWallCollisions(self):
        snake_head_rect = pygame.Rect(int(self.snake.body[0].x * cell_size),
                                              int(self.snake.body[0].y * cell_size),
                                              cell_size, cell_size)
        
        if self.wall.checkSnakeCollision(snake_head_rect):
            self.game_over()

        if self.wall.checkCollision(self.fruit.pos):
            self.fruit.randomize()
                

    def spawn_bullet(self):
        # Randomly decide which side to spawn from (0: top, 1: bottom, 2: left, 3: right)
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.uniform(0, cell_number)
            y = 0
            direction = Vector2(0, 1)
        elif side == 1:  # Bottom
            x = random.uniform(0, cell_number)
            y = cell_number
            direction = Vector2(0, -1)
        elif side == 2:  # Left
            x = 0
            y = random.uniform(0, cell_number)
            direction = Vector2(1, 0)
        else:  # Right
            x = cell_number
            y = random.uniform(0, cell_number)
            direction = Vector2(-1, 0)

        position = Vector2(x, y)
        bullet = BULLET(position, direction,screen)
        self.bullets.append(bullet)

    # Draw Health Bar
    def draw_health_bar(self):
        
        bar_width = 100  
        bar_height = 20   
        health_x = cell_number * cell_size - bar_width - 670  
        health_y = 10  

        # Calculate health ratio (how much of the bar should be filled)
        health_ratio = self.health / 5  

        
        pygame.draw.rect(screen, (255, 0, 0), (health_x, health_y, bar_width, bar_height))  # Full red bar
        
        pygame.draw.rect(screen, (0, 255, 0), (health_x, health_y, bar_width * health_ratio, bar_height))  # Green health bar

        # Draw a border around the health bar
        pygame.draw.rect(screen, (0, 0, 0), (health_x, health_y, bar_width, bar_height), 2)

    #Initialize spawns of game
    def draw_elements(self):
        # Draw the background image
        screen.blit(background_image, (0, 0))
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.wall.deleteWall()
        self.wall.dynamicWall(grid)
        self.wall.create_Wall()
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.draw_score()
        self.draw_health_bar()

        #draws selected map at top of the screen
        if selected_map_name:
            map_text_surface = game_font.render(f"{selected_map_name}", True, (255, 255, 255))
            map_text_x = (cell_number * cell_size - map_text_surface.get_width()) // 2
            screen.blit(map_text_surface, (map_text_x, 10))

        if self.start_time is None:  # If the game hasn't started, display 00:00
            timer_text = "00:00"
        else:
            if game_state == paused and self.paused_time is not None:
             
                elapsed_time = (self.paused_time - self.start_time - self.total_paused_duration) // 1000
            else:
                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - self.start_time - self.total_paused_duration) // 1000

            
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_text = f"{minutes:02}:{seconds:02}"  # Format the time as Minute:Seconds

        # Render the timer text
        timer_surface = game_font.render(timer_text, True, (255, 255, 255))
        timer_x = cell_number * cell_size - timer_surface.get_width() - 10 
        screen.blit(timer_surface, (timer_x, 10))

    #Check snake eat apple
    def check_eat(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            scores.highscore+=1
            current_time = pygame.time.get_ticks() - self.total_paused_duration
            self.last_fruit_time = current_time
            if self.health < 5: # Makes sure player dun go over 5 health when he eats fruit
                self.health += 1

            
#game over if hit its own body
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

#game over MK 
    def game_over(self):
        global game_state
        game_state = game_end
        self.start_time = pygame.time.get_ticks()
        self.reset()
    
    def reset(self):
        self.snake.reset()
        self.bullets = []
        self.health = 5
        self.start_time = None  # Reset the timer
        self.game_started = False  # Reset game start flag
        self.last_fruit_time = None  # Reset the fruit timer
        self.paused_time = None  # Reset paused time
        self.total_paused_duration = 0  # Reset paused duration


    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56,74,12))
        pos_x = int(cell_size * cell_number - 60)
        pos_y = int(cell_size * cell_number - 40)
        #box for the score
        score_rect = score_surface.get_rect(center = (pos_x, pos_y))
        #Create a box for the apple png
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        #take position of both score and the apple to make the box for the scoreboard
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)
 
#adjusting the sound mixer
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
# Load the overlay image
start_overlay = pygame.image.load(cwd + '/Snake-main/Graphics/GameInstruction.png').convert_alpha()
start_overlay = pygame.transform.scale(start_overlay, (cell_number * cell_size, cell_number * cell_size))
apple = pygame.image.load(cwd+ '/Snake-main/Graphics/apple.png').convert_alpha()
left_wall = pygame.image.load(cwd+'/Snake-main/Graphics/left_wall.png').convert_alpha()
right_wall = pygame.image.load(cwd+'/Snake-main/Graphics/right_wall.png').convert_alpha()
game_font = pygame.font.Font(cwd+'/Snake-main/Font/PoetsenOne-Regular.ttf', 25)
map_Instruction = pygame.image.load(cwd+'/Snake-main/Graphics/mapInstruction.png').convert_alpha()
# Background image
background_image = pygame.image.load(cwd+'/Snake-main/Graphics/background.jpg').convert()
game_menu_image = pygame.image.load(cwd+'/Snake-main/Graphics/screen_menu_image.jpg').convert()
game_over_image = pygame.image.load(cwd+'/Snake-main/Graphics/game_over_image.png').convert_alpha()

# Setup timers
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)



main_game = MAIN()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == playing:
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if not main_game.game_started and event.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s, pygame.K_RIGHT, pygame.K_d]:
                    main_game.start_time = pygame.time.get_ticks()  # Start the timer
                    main_game.game_started = True # Flag the game as started
                    
                if main_game.game_started:   
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_DOWN  or event.key == pygame.K_s:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_p:  # Check for pause key
                        game_state = paused

    if game_state == playing:
        main_game.draw_elements()
    elif game_state == main_menu:
        main_menu_screen()
    elif game_state == overlay:
        # Display the overlay image
        screen.blit(start_overlay, (0, 0))
        pygame.display.flip()

        # Listen for any movement key press to transition to playing state
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s,
                                    pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]):
            game_state = playing  # Transition to playing state
    elif game_state == game_end:
        main_game.reset()
        end_game_screen()
    elif game_state == paused:
        pause_menu_screen()
        
    #screen.fill((175, 215, 70))  # Optional: Clear the screen with a color before drawing
    pygame.display.update()
    clock.tick(60)

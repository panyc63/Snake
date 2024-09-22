import pygame, sys, random ,os
from pygame.math import Vector2
import sqlitecloud


# Constants
cell_size = 40
cell_number = 20
cwd = os.getcwd()
class scores:
    ApiKey  = 'EGjpcL3ZfSkxt9dL8y2sQkJCreUD69vmX9a6bpaa3M4' #Please remove before pushing to git
    highscore = 0

##### Mik's Code #####

main_menu = 0
playing = 1
game_end = 2

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
settings_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 420), (button_width, button_height))
leaderscore_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 480), (button_width, button_height))
quit_button_rect = pygame.Rect((cell_size*cell_number // 2 - button_width // 2, 540), (button_width, button_height))

# Function to draw the leaderboard Border
def draw_leaderboard():
    high_scores = fetch_high_scores()  # Get high scores from SQLite Cloud

    # Draw the header
    header_font = pygame.font.Font(cwd + '/Snake-main/Font/PoetsenOne-Regular.ttf', 30)
    header_surface = header_font.render("Leaderboard", True, (0, 0, 0))
    screen.blit(header_surface, (cell_size * cell_number // 2 - header_surface.get_width() // 2, 50))

    # Define table dimensions
    table_width = cell_size * cell_number / 1.5
    row_height = 40
    table_x = cell_size * cell_number // 4
    table_y = 80
    cell_width = table_width / 2  # Two columns: Username and Score

    # Draw the border for the table
    pygame.draw.rect(screen, (0, 0, 0), (table_x, table_y, table_width, row_height + len(high_scores) * 30), 2)

    # Draw the table header
    username_header_surface = game_font.render("Username", True, (0, 0, 0))
    score_header_surface = game_font.render("Score", True, (0, 0, 0))
    screen.blit(username_header_surface, (table_x + 10, table_y + 10))
    screen.blit(score_header_surface, (table_x + cell_width + 10, table_y + 10))

    # Draw rows and their borders
    for index, (username, score) in enumerate(high_scores):
        row_y = table_y + row_height + index * 30
        # Draw row border
        pygame.draw.rect(screen, (0, 0, 0), (table_x, row_y, table_width, 30), 1)

        # Fit text in cells
        username_surface = game_font.render(username, True, (0, 0, 0))
        score_surface = game_font.render(str(score), True, (0, 0, 0))
        screen.blit(username_surface, (table_x + 10, row_y + 5))  # Adjust vertical alignment
        screen.blit(score_surface, (table_x + cell_width + 10, row_y + 5))  # Adjust vertical alignment

    # Draw bottom border
    pygame.draw.rect(screen, (0, 0, 0), (table_x, table_y + row_height + len(high_scores) * 30 - 2, table_width, 2))  # Bottom border

# Function to display the leaderboard
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

def upload_score(username):
    # Assuming you have a variable that holds the current score
    current_score = len(main_game.snake.body) - 3

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

    global game_state

    game_menu = True

    while game_menu:
        
        screen.blit(game_menu_image, (0, 0))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over any button
        start_hovered = start_button_rect.collidepoint(mouse_pos)
        settings_hovered = settings_button_rect.collidepoint(mouse_pos)
        leaderscore_hovered = leaderscore_button_rect.collidepoint(mouse_pos)
        quit_hovered = quit_button_rect.collidepoint(mouse_pos)

        # Hover effects
        draw_button(start_button_rect, "Start", start_hovered)
        draw_button(settings_button_rect, "Gameplay Settings", settings_hovered)
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
                    game_state = playing
                    game_menu = False
                #If Settings Button was pressed
                elif settings_button_rect.collidepoint(mouse_pos):
                    print("Gameplay Settings button clicked")
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
    restart_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 400), (button_width, button_height))
    quit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 460), (button_width, button_height))

    # Move the input box and submit button lower
    input_box_y_position = 520  # Position for the input box
    input_box = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position), (button_width, button_height))
    submit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position + button_height + 10), (button_width, button_height))

    end_screen = True

def end_game_screen():
    global game_state
    username_input = ""
    submit_enabled = True

    # Tinted death screen
    tint_surface = pygame.Surface((cell_number * cell_size, cell_number * cell_size), pygame.SRCALPHA)
    tint_surface.fill((190, 0, 0, 100))

    # Button dimensions
    button_width = 200
    button_height = 50

    # Position for buttons and game over text
    game_over_y_position = 150
    restart_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, game_over_y_position + 100), (button_width, button_height))
    quit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, game_over_y_position + 160), (button_width, button_height))

    # Move the input box and submit button lower
    input_box_y_position = game_over_y_position + 230  # Position for the input box
    input_box = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position), (button_width, button_height))
    submit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position + button_height + 10), (button_width, button_height))

    end_screen = True

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
    restart_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 400), (button_width, button_height))
    quit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, 460), (button_width, button_height))

    # Move the input box and submit button lower
    input_box_y_position = 540  # Moved down by 20 pixels
    input_box = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position), (button_width, button_height))
    submit_button_rect = pygame.Rect((cell_number * cell_size // 2 - button_width // 2, input_box_y_position + button_height + 10), (button_width, button_height))

    end_screen = True

    while end_screen:
        screen.blit(background_image, (0, 0))
        screen.blit(tint_surface, (0, 0))
        screen.blit(game_over_image, (cell_number * cell_size // 2 - game_over_image.get_width() // 2, 200))

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
        quit_hovered = quit_button_rect.collidepoint(mouse_pos)
        submit_hovered = submit_button_rect.collidepoint(mouse_pos)

        # Hover effects
        draw_button(restart_button_rect, "Retry", restart_hovered)
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
                    game_state = playing
                    end_screen = False
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif submit_enabled and submit_button_rect.collidepoint(mouse_pos):
                    if username_input:  # Check if the username is not empty
                        upload_score(username_input)  # Call the upload_score function
                        submit_enabled = False  # Disable the submit button after uploading

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if submit_enabled and username_input:  # Check if the username is not empty
                        upload_score(username_input)
                        submit_enabled = False
                else:
                    username_input += event.unicode

        pygame.display.flip()







##### Mik's Code #####

class SNAKE:
    def __init__(self):
        # Initialize the snake
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        test=0
        # Load images for snake parts
        self.head_up = pygame.image.load(cwd+'/Snake-main/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(cwd+'/Snake-main/Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(cwd+'/Snake-main/Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(cwd+'/Snake-main/Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load(cwd+'/Snake-main/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(cwd+'/Snake-main/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(cwd+'/Snake-main/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(cwd+'/Snake-main/Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(cwd+'/Snake-main/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(cwd+'/Snake-main/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(cwd+'/Snake-main/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(cwd+'/Snake-main/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(cwd+'/Snake-main/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(cwd+'/Snake-main/Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound(cwd+'/Snake-main/Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple2, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class WALL:
    def __init__(self):
        self.body = [Vector2(5,6), Vector2(4,6), Vector2(3,6)]
        self.middle_wall = pygame.image.load(cwd+'/Snake-main/Graphics/middle_wall.png').convert_alpha()

    def create_Wall(self):
         for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            wall_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(right_wall, wall_rect)
            elif index == len(self.body) -1 :
                screen.blit(left_wall, wall_rect)
            else:
                screen.blit(middle_wall, wall_rect)


class BULLET:
    def __init__(self, position, direction):
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
        pygame.draw.circle(screen, self.color, pixel_position, self.radius)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.wall = WALL()
        self.bullets = []
        #get time of inititation which is 0 when starting
        self.last_bullet=pygame.time.get_ticks()

    def update(self):
        self.snake.move_snake()
        self.update_bullets()
        self.check_eat()
        self.check_fail()
        self.spawn_startbullet()

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
        hitWall = False  
        for i in self.wall.body:
            wallRect.append([(pygame.Rect(int(i.x * cell_size) ,int(i.y * cell_size),cell_size, cell_size))])
        

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
                    self.game_over()

                
                for w in wallRect:
                    if bullet_rect.colliderect(w[0]):
                        hitWall = True
                    elif snake_head_rect.colliderect(w[0]):
                        self.game_over()

                if hitWall:   
                    self.bullets.remove(bullet)
                    hitWall = False
               

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
        bullet = BULLET(position, direction)
        self.bullets.append(bullet)


    def draw_elements(self):
        # Draw the background image
        screen.blit(background_image, (0, 0))
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.wall.create_Wall()

        for bullet in self.bullets:
            bullet.draw_bullet()
        self.draw_score()

    def check_eat(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
#game over if hit its own body
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.reset()

#game over MK 
    def game_over(self):
        global game_state
        game_state = game_end
    
    def reset(self):
        self.snake.reset()
        self.bullets = []


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
apple = pygame.image.load(cwd+ '/Snake-main/Graphics/apple.png').convert_alpha()
apple2 =pygame.image.load(cwd+'/Snake-main/Graphics/apple2.png').convert_alpha()
middle_wall =pygame.image.load(cwd+'/Snake-main/Graphics/middle_wall.png').convert_alpha()
left_wall = pygame.image.load(cwd+'/Snake-main/Graphics/left_wall.png').convert_alpha()
right_wall = pygame.image.load(cwd+'/Snake-main/Graphics/right_wall.png').convert_alpha()
game_font = pygame.font.Font(cwd+'/Snake-main/Font/PoetsenOne-Regular.ttf', 25)

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
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_DOWN  or event.key == pygame.K_s:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

    if game_state == playing:
        main_game.draw_elements()
    elif game_state == main_menu:
        main_menu_screen()
    elif game_state == game_end:
        end_game_screen()
        
    #screen.fill((175, 215, 70))  # Optional: Clear the screen with a color before drawing
    pygame.display.update()
    clock.tick(60)

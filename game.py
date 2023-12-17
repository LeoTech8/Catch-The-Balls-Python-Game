# Made by Leo in Thonny with Python and with some help from ChatGPT

# Imports Everything
import pygame
import random
import sys

# Turns On Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

class Ball:
    def __init__(self, radius, color, speed):
        self.radius = radius
        self.color = color
        self.speed_x = speed
        self.speed_y = speed
        self.spawn()

    def spawn(self):
        # Randomly generate a new position for the ball when it spawns or respawns
        self.x = random.randint(self.radius, screen_width - self.radius)
        self.y = random.randint(self.radius, screen_height - self.radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Sets Ball Variabls
balls = []
num_balls = 7
for _ in range(num_balls):
    radius = random.randint(10, 30)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    speed = random.uniform(1, 5)  # Adjust the speed range as needed
    balls.append(Ball(radius, color, speed))

clock = pygame.time.Clock()

# Load Images & Set Title
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 600))
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (100, 100))
appicon = pygame.image.load("appicon.png")
appicon = pygame.transform.scale(appicon, (100, 100))
pygame.display.set_caption("Catch The Balls")
pygame.display.set_icon(appicon)

# Set Player Variables
player_x = 300
player_y = 200
player_speed = 50
score = 0

# Game state variables
game_over = False
start_time = pygame.time.get_ticks()  # Get the initial time
elapsed_time = 0

font = pygame.font.Font(None, 36)
white = (255, 255, 255)
score_text = font.render("Score: " + str(score), True, white)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle mouse click events when the game is over
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (
                screen_width // 2 - 60 < x < screen_width // 2 + 60
                and screen_height // 2 + 50 < y < screen_height // 2 + 90
            ):
                # Clicked "Play Again"
                score = 0
                balls = []
                for _ in range(num_balls):
                    radius = random.randint(10, 30)
                    color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                    speed = random.uniform(1, 5)
                    balls.append(Ball(radius, color, speed))
                game_over = False
                start_time = pygame.time.get_ticks()
            elif (
                screen_width // 2 + 10 < x < screen_width // 2 + 90
                and screen_height // 2 + 50 < y < screen_height // 2 + 90
            ):
                # Clicked "Close"
                pygame.quit()
                sys.exit()

    if not game_over:
        screen.blit(background, (0, 0))
        screen.blit(player, (player_x, player_y))

        for ball in balls:
            ball.move()

            if ball.x < ball.radius or ball.x > screen_width - ball.radius:
                ball.speed_x *= -1
            if ball.y < ball.radius or ball.y > screen_height - ball.radius:
                ball.speed_y *= -1

            ball.draw()
            
        # Sets up arrow keys to move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
            
        # Player can't go off screen
        if player_x < 0:
            player_x = +2
        if player_x > 700:
            player_x = 699
        if player_y < 0:
            player_y = +2
        if player_y > 590:
            player_y = 589
        

        # Check for collisions between player and balls
        for ball in balls:
            if (
                (player_x - ball.radius < ball.x < player_x + 100)
                and (player_y - ball.radius < ball.y < player_y + 100)
            ):
                score += 1
                balls.remove(ball)

        # Respawn a new ball if the number of balls is less than the desired number
        if len(balls) < num_balls:
            radius = random.randint(10, 30)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            speed = random.uniform(1, 5)  # Adjust the speed range as needed
            balls.append(Ball(radius, color, speed))

        # Update the score text
        score_text = font.render("Score: " + str(score), True, white)

        # Calculate elapsed time
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # Convert to seconds

        # If one minute has passed, end the game
        if elapsed_time >= 60:
            game_over = True

        # Draw the score text on the screen
        screen.blit(score_text, (10, 10))

    # If the game is over, display the game over screen
    if game_over:
        game_over_text = font.render("Game Over", True, white)
        score_text = font.render("Score: " + str(score), True, white)
        play_again_text = font.render("Play Again", True, white)
        close_text = font.render("Close", True, white)

        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        screen.blit(score_text, (screen_width // 2 - 40, screen_height // 2))
        screen.blit(play_again_text, (screen_width // 2 - 60, screen_height // 2 + 50))
        screen.blit(close_text, (screen_width // 2 + 10, screen_height // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Snake settings
SNAKE_SIZE = 20
SNAKE_SPEED = 15
snake_pos = [[100, 50], [80, 50], [60, 50]]  # Initial snake with length 3
snake_direction = "RIGHT"

# Food settings
FOOD_SIZE = 25  # Larger food size for easier collision detection
green_food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                  random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
red_food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
green_food_spawn = True
red_food_spawn = True

# Set up the game clock
clock = pygame.time.Clock()

def game_over():
    font = pygame.font.SysFont('arial', 35)
    text = font.render("Game Over", True, RED)
    screen.blit(text, [WIDTH // 3, HEIGHT // 3])
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

def draw_snake(snake_pos):
    for pos in snake_pos:
        pygame.draw.rect(screen, WHITE, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

def move_snake(direction, snake_pos):
    if direction == 'UP':
        new_head = [snake_pos[0][0], snake_pos[0][1] - SNAKE_SIZE]
    elif direction == 'DOWN':
        new_head = [snake_pos[0][0], snake_pos[0][1] + SNAKE_SIZE]
    elif direction == 'LEFT':
        new_head = [snake_pos[0][0] - SNAKE_SIZE, snake_pos[0][1]]
    elif direction == 'RIGHT':
        new_head = [snake_pos[0][0] + SNAKE_SIZE, snake_pos[0][1]]
    
    # Insert the new head and remove the tail unless green food is eaten
    snake_pos.insert(0, new_head)
    if len(snake_pos) > snake_length:
        snake_pos.pop()

def check_collisions(snake_pos):
    # Check if snake hits the wall
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT:
        game_over()

    # Check if snake hits itself
    if snake_pos[0] in snake_pos[1:]:
        game_over()

# Main game loop
snake_length = len(snake_pos)  # Initial snake length
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # Move the snake
    move_snake(snake_direction, snake_pos)

    # Check for green food collision
    if pygame.Rect(snake_pos[0][0], snake_pos[0][1], SNAKE_SIZE, SNAKE_SIZE).colliderect(
       pygame.Rect(green_food_pos[0], green_food_pos[1], FOOD_SIZE, FOOD_SIZE)):
        snake_length += 1  # Increase length only when green food is eaten
        green_food_spawn = False

    # Check for red food collision
    elif pygame.Rect(snake_pos[0][0], snake_pos[0][1], SNAKE_SIZE, SNAKE_SIZE).colliderect(
         pygame.Rect(red_food_pos[0], red_food_pos[1], FOOD_SIZE, FOOD_SIZE)):
        if snake_length > 1:
            snake_length -= 1  # Decrease length only when red food is eaten
            snake_pos.pop()  # Remove the last segment to shrink the snake
        red_food_spawn = False

    # End game if snake length is 1 or less
    if snake_length <= 1:
        game_over()

    # Spawn new green food if eaten
    if not green_food_spawn:
        green_food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                          random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
        green_food_spawn = True

    # Spawn new red food if eaten
    if not red_food_spawn:
        red_food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                        random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
        red_food_spawn = True

    # Check for collisions
    check_collisions(snake_pos)

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake_pos)
    pygame.draw.rect(screen, GREEN, pygame.Rect(green_food_pos[0], green_food_pos[1], FOOD_SIZE, FOOD_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(red_food_pos[0], red_food_pos[1], FOOD_SIZE, FOOD_SIZE))

    # Update the screen
    pygame.display.flip()

    # Set the speed of the snake
    clock.tick(SNAKE_SPEED)

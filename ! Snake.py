# By John Lake 

import pygame as pg
from random import randrange

# Game constants
window_size = 800
tile_size = 50
range_values = (tile_size // 2, window_size - tile_size // 2, tile_size)
get_random_position = lambda: [randrange(*range_values), randrange(*range_values)]
snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
score = 0

# Initialize Pygame
pg.init()
screen = pg.display.set_mode([window_size] * 2)
clock = pg.time.Clock()
font = pg.font.Font(None, 36)

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and snake_dir != (0, tile_size):
                snake_dir = (0, -tile_size)
            if event.key == pg.K_s and snake_dir != (0, -tile_size):
                snake_dir = (0, tile_size)
            if event.key == pg.K_a and snake_dir != (tile_size, 0):
                snake_dir = (-tile_size, 0)
            if event.key == pg.K_d and snake_dir != (-tile_size, 0):
                snake_dir = (tile_size, 0)
    
    # Update snake position
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

        # Check collision with borders
        if (
            snake.left < 0
            or snake.right > window_size
            or snake.top < 0
            or snake.bottom > window_size
        ):
            pg.time.delay(1000)  # Delay for 1 second
            snake.center = get_random_position()
            food.center = get_random_position()
            length = 1
            segments = [snake.copy()]
            snake_dir = (0, 0)
            score = 0
        
        # Check self-collision
        self_collision = snake.collidelist(segments[:-1]) != -1
        if self_collision:
            pg.time.delay(1000)  # Delay for 1 second
            snake.center = get_random_position()
            food.center = get_random_position()
            length = 1
            segments = [snake.copy()]
            snake_dir = (0, 0)
            score = 0

        # Check collision with food
        if snake.colliderect(food):
            food.center = get_random_position()
            length += 1
            score += 1

    # Draw game elements
    screen.fill('green')
    pg.draw.rect(screen, 'red', food)
    [pg.draw.rect(screen, 'black ', segment) for segment in segments]
    score_text = font.render(f"Score: {score}", True, 'white')
    screen.blit(score_text, (10, 10))

    # Update display
    pg.display.flip()
    clock.tick(60)

#  Finish
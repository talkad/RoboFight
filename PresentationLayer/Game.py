import pygame
from pygame.locals import *
import os
from BusinessLayer.Robot import Robot


# define display surface
WIDTH, HEIGHT = 1000, 600


# setup pygame
pygame.init()
pygame.display.set_caption("RoboFight")
clock = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# set background
background = pygame.image.load("../img/background.png").convert()
x = 0

# game loop
running = True
all_sprites = pygame.sprite.Group()
robot = Robot(WIDTH/2, HEIGHT-60)
all_sprites.add(robot)

while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            running = False

    # Update
    all_sprites.update()

    # Draw
    rel_x = x % background.get_rect().width
    screen.blit(background, (rel_x - background.get_rect().width, 0))
    if rel_x < WIDTH:
        screen.blit(background, (rel_x, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and x > -1000:
        x -= 5
    if keys[pygame.K_LEFT] and x < 1000:
        x += 5
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()

import pygame
from pygame.locals import *
import os

from BusinessLayer.Board import Board
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


# game loop
running = True
all_sprites = pygame.sprite.Group()
robot = Robot(WIDTH/2, HEIGHT-70)
all_sprites.add(robot)

background = pygame.image.load("../img/background.png").convert()
board = Board(background, robot)

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

    # draw background
    board.game_cycle()
    rel_x = board.background_x % board.image.get_rect().width
    screen.blit(board.image, (rel_x - board.image.get_rect().width, 0))
    if rel_x < WIDTH:
        screen.blit(board.image, (rel_x, 0))

    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()

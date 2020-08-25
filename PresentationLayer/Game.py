import pygame
from pygame.locals import *
import sys
import os


def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


# define display surface
W, H = 1000, 600
AREA = W * H


# setup pygame
pygame.init()
CLOCK = pygame.time.Clock()
os.environ['SDL_VIDEO_CENTERED'] = '1'
DS = pygame.display.set_mode((W, H))
FPS = 60

background = pygame.image.load("../img/background.png").convert()
x = 0

# main loop
while True:
    events()
    rel_x = x % background.get_rect().width
    DS.blit(background, (rel_x - background.get_rect().width, 0))
    if rel_x < W:
        DS.blit(background, (rel_x, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and x > -1000:
        x -= 5
    if keys[pygame.K_LEFT] and x < 1000:
        x += 5

    print(x)
    pygame.display.update()
    CLOCK.tick(FPS)

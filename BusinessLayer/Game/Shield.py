import os
import pygame

from BusinessLayer.Game.Settings import DIRECTIONS, HEIGHT, PLAYER_ACC

filepath = os.path.dirname(__file__)
filename = '../../img/heart.png'
img = pygame.image.load(os.path.join(filepath, filename)).convert()

SPEED = 5


class Shield(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (30, 30)).convert()
        self.image.set_colorkey(pygame.Color('white'))
        self.rect = self.image.get_rect()
        self.rect.bottom = -50
        self.rect.centerx = x
        self.movement_mode = False

    def update(self):

        self.rect.y += SPEED

        keys = pygame.key.get_pressed()
        if self.movement_mode:
            if keys[pygame.K_LEFT]:
                self.rect.x += PLAYER_ACC * 2
            if keys[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_ACC * 2

        # kill if it passed the board limits
        if self.rect.bottom > HEIGHT - 70:
            self.kill()

    def change_mode(self, mode):
        self.movement_mode = mode

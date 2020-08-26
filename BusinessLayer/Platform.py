import pygame

from BusinessLayer.Settings import PLAYER_ACC


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((102, 51, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.limit = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.limit < 1850:
            self.rect.x += PLAYER_ACC
            self.limit += PLAYER_ACC
        if keys[pygame.K_RIGHT] and self.limit > -1000:
            self.rect.x -= PLAYER_ACC
            self.limit -= PLAYER_ACC

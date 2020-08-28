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
        self.movement_mode = False

    # move the platforms with the background
    # as long as the limit hasn't reached
    def update(self):
        keys = pygame.key.get_pressed()
        if self.movement_mode:
            if keys[pygame.K_LEFT]:
                self.rect.x += PLAYER_ACC * 2
            if keys[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_ACC * 2

    def change_mode(self, mode):
        self.movement_mode = mode

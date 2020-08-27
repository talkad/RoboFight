import pygame

from BusinessLayer.Settings import PLAYER_ACC, WIDTH


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, board):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((102, 51, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.board = board

    # move the platforms with the background
    # as long as the limit hasn't reached
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.board.background_x > -1000 and self.board.player.rect.centerx == WIDTH / 2:
            self.rect.x += PLAYER_ACC * 2
        if keys[pygame.K_RIGHT] and self.board.background_x > -1000 and self.board.player.rect.centerx == WIDTH / 2:
            self.rect.x -= PLAYER_ACC * 2

import pygame

WIDTH, HEIGHT = 1000, 600


class Board:
    def __init__(self, background, robot):
        self.background_x = 0
        self.image = background
        self.player = robot

    # every cycle of the game, one of two things could happen:
    # 1. the board boundary didnt reach- so the background scrolls
    # 2. otherwise the robot moves
    def game_cycle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.player.rect.centerx < 500:
                self.player.rect.x += 6
            elif self.background_x > -1000:
                self.background_x -= 6
            elif self.player.rect.centerx < 945:
                self.player.rect.x += 6

        if keys[pygame.K_LEFT]:
            if self.player.rect.centerx > 500:
                self.player.rect.x -= 6
            elif self.background_x < 1000:
                self.background_x += 6
            elif self.player.rect.centerx > 55:
                self.player.rect.x -= 6

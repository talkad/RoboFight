import pygame
from pygame.locals import *
import os
from BusinessLayer.Platform import Platform
from BusinessLayer.Robot import Robot
from BusinessLayer.Settings import WIDTH, PLAYER_ACC, HEIGHT, PLATFORM_LIST


# setup pygame
pygame.init()
pygame.display.set_caption("RoboFight")
clock = pygame.time.Clock()
FPS = 60

clock.tick(FPS)
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("../img/background.png").convert()


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.background_x = 0
        self.player = Robot(WIDTH/2, HEIGHT-70, self)
        self.running = True

    # every cycle of the game, one of two things could happen:
    # 1. the board boundary didnt reach- so the background scrolls
    # 2. otherwise the robot moves
    def game_cycle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.background_x > -1000:
                self.background_x -= PLAYER_ACC

        if keys[pygame.K_LEFT]:
            if self.background_x < 1000:
                self.background_x += PLAYER_ACC

    def new(self):
        # start a new game
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()
            # print(self.player.rect.centerx+(self.background_x * -1))

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        # draw background
        board.game_cycle()
        rel_x = board.background_x % background.get_rect().width
        screen.blit(background, (rel_x - background.get_rect().width, 0))
        if rel_x < WIDTH:
            screen.blit(background, (rel_x, 0))

        self.all_sprites.draw(screen)
        # after drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


# game loop
board = Game()

while board.running:
    board.new()
    board.show_go_screen()


pygame.quit()

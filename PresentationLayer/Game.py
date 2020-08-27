import os

import pygame
from pygame.locals import *
from BusinessLayer.Platform import Platform
from BusinessLayer.Robot import Robot
from BusinessLayer.Bullet import Explosion
from BusinessLayer.Settings import WIDTH, PLAYER_ACC, HEIGHT, PLATFORM_LIST
from PresentationLayer.Service import draw_text, concat_char, get_max

# setup pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("RoboFight")
clock = pygame.time.Clock()
FPS = 60

clock.tick(FPS)
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("../img/background.png").convert()

explosion_sound = pygame.mixer.Sound("../sound/Explosion.wav")

# generate the chat textbox
text_box = pygame.Rect(100, HEIGHT - 50, 300, 30)


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.text_mode = False
        self.text = ""
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.background_x = 0
        self.player = Robot(WIDTH / 2, HEIGHT - 70, self)
        self.running = True

    # every cycle of the game, one of two things could happen:
    # 1. the board boundary didnt reach- so the background scrolls
    # 2. otherwise the robot moves
    def game_cycle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.background_x > -1000 and self.player.rect.centerx == WIDTH / 2:
                self.background_x -= PLAYER_ACC * 2

        if keys[pygame.K_LEFT]:
            if self.background_x < 1000 and self.player.rect.centerx == WIDTH / 2:
                self.background_x += PLAYER_ACC * 2

    # start a new game
    def new(self):
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat, self)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    # Game  Main Loop
    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            pygame.sprite.collide_rect_ratio(8)
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            legal_hits = []
            for hit in hits:
                if self.player.pos.y - 20 < hit.rect.top < self.player.pos.y:
                    legal_hits.append(hit.rect.top)

            platform_height = get_max(legal_hits)
            if platform_height != -1:
                # self.player.pos.y = hits[0].rect.top
                self.player.pos.y = get_max(legal_hits)
                self.player.vel.y = 0

        # check if a bullet hits a platform
        bullet_hits = pygame.sprite.groupcollide(self.bullets, self.platforms, True, False)
        for bullet in bullet_hits:
            explosion = Explosion(bullet.rect.center)
            self.all_sprites.add(explosion)

    # handle key events
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check mouse clicked event for add platforms
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                p = Platform(x - 75, y, 150, 20, self)
                self.all_sprites.add(p)
                self.platforms.add(p)

            # add the key to the text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.text_mode:
                    self.player.shoot()
                    explosion_sound.play()
                elif self.text_mode:
                    self.text = concat_char(self.text, pygame.key.name(event.key))
                    if pygame.key.name(event.key) == 'return':
                        # sent message to opponent
                        self.text = ""

            # check for closing window
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.text_mode = not self.text_mode

    # draw all objects on the screen
    def draw(self):
        # draw background
        board.game_cycle()
        rel_x = board.background_x % background.get_rect().width
        screen.blit(background, (rel_x - background.get_rect().width, 0))
        if rel_x < WIDTH:
            screen.blit(background, (rel_x, 0))

        self.all_sprites.draw(screen)

        # draw all text on screen
        draw_text(screen, "position: ({:f}, {:f})".format(self.player.pos.x + (self.background_x * -1),
                                                          self.player.pos.y),
                  20, WIDTH / 2, 10, 'black')

        # draw textbox on screen
        if self.text_mode:
            draw_text(screen, "Chat: ", 30, 50, HEIGHT - 55, "black")

        pygame.draw.rect(screen, pygame.Color('white'), text_box, 0)
        text_color = "black"
        if len(self.text) >= 30:
            text_color = "red"
        draw_text(screen, self.text, 20, 245, HEIGHT - 50, text_color)

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

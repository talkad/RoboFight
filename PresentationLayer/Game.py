import pygame
from pygame.locals import *
import os
from BusinessLayer.Platform import Platform
from BusinessLayer.Robot import Robot
from BusinessLayer.Settings import WIDTH, PLAYER_ACC, HEIGHT, PLATFORM_LIST, BLACK

# setup pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("RoboFight")
clock = pygame.time.Clock()
FPS = 60
font_name = pygame.font.match_font('arial')

clock.tick(FPS)
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("../img/background.png").convert()

explosion_sound = pygame.mixer.Sound("../sound/Explosion.wav")


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
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
            if self.background_x > -1000:
                self.background_x -= PLAYER_ACC

        if keys[pygame.K_LEFT]:
            if self.background_x < 1000:
                self.background_x += PLAYER_ACC

    # start a new game
    def new(self):
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
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
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    # handle key events
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                    explosion_sound.play()

    # draw all objects on the screen
    def draw(self):
        # draw background
        board.game_cycle()
        rel_x = board.background_x % background.get_rect().width
        screen.blit(background, (rel_x - background.get_rect().width, 0))
        if rel_x < WIDTH:
            screen.blit(background, (rel_x, 0))

        self.all_sprites.draw(screen)
        self.draw_text(screen, "position: ({:f}, {:f})".format(self.player.pos.x + (self.background_x * -1),
                                                               self.player.pos.y),
                       20, WIDTH / 2, 10)

        # after drawing everything, flip the display
        pygame.display.flip()

    # draw text
    def draw_text(self, surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

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

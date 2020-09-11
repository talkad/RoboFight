import os
import sys
import re
import pygame
from pygame.locals import *
from random import randint
from BusinessLayer.Client.MessagingProtocol import get_content
from BusinessLayer.Game.Platform import Platform
from BusinessLayer.Game.Robot import player_robot, opponent_robot
from BusinessLayer.Game.Bullet import Explosion
from BusinessLayer.Game.Settings import WIDTH, PLAYER_ACC, HEIGHT, PLATFORM_LIST
from BusinessLayer.Game.Shield import Shield
from PresentationLayer.Observer import Observer
from PresentationLayer.Service import draw_text, concat_char, get_max, draw_shield_bar, draw_msg_stack, background, \
    screen, connection_starter

pygame.init()

pygame.display.set_caption("RoboFight")
clock = pygame.time.Clock()
FPS = 60

clock.tick(FPS)
os.environ['SDL_VIDEO_CENTERED'] = '1'

# generate the chat textbox
text_box = pygame.Rect(50, HEIGHT - 45, 300, 25)
shield_freq = 2500


class Game(Observer):
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.text_mode = False
        self.text = ""
        self.chat = []
        self.platforms = pygame.sprite.Group()
        self.platforms_list = []
        self.bullets = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.shield_list = []
        self.background_x = 0
        self.player = player_robot(WIDTH / 2, HEIGHT - 70, self)
        self.opponent = opponent_robot(WIDTH / 2, HEIGHT - 70, self)
        self.running = True
        self.game_over = False
        self.last_shield = pygame.time.get_ticks()

    # every cycle of the game, one of two things could happen:
    # 1. the board boundary didnt reach- so the background scrolls
    # 2. otherwise the robot moves
    def game_cycle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.move_bg_right()

        if keys[pygame.K_LEFT]:
            self.move_bg_left()

    def move_bg_right(self):
        if self.background_x > -1000 and self.player.rect.centerx == WIDTH / 2:
            self.background_x -= PLAYER_ACC * 2
            self.platforms_movement_mode(True)
            self.shields_movement_mode(True)
        else:
            self.platforms_movement_mode(False)
            self.shields_movement_mode(False)

    def move_bg_left(self):
        if self.background_x < 1000 and self.player.rect.centerx == WIDTH / 2:
            self.background_x += PLAYER_ACC * 2
            self.platforms_movement_mode(True)
            self.shields_movement_mode(True)
        else:
            self.platforms_movement_mode(False)
            self.shields_movement_mode(False)

    # start a new game
    def new(self):
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.opponent)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.platforms_list.append(p)

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
                self.player.pos.y = get_max(legal_hits)
                self.player.vel.y = 0

        # # check if a bullet hits a platform - removed this functionality because of high use of the CPU
        # bullet_hits = pygame.sprite.groupcollide(self.bullets, self.platforms, True, False)
        # for bullet in bullet_hits:
        #     explosion = Explosion(bullet.rect.center)
        #     self.all_sprites.add(explosion)

        # check if a bullet hits a robot
        opponent_hits = pygame.sprite.spritecollide(self.opponent, self.bullets, True)
        for bullet in opponent_hits:
            self.opponent.shield -= 20
            explosion = Explosion(bullet.rect.center)
            self.all_sprites.add(explosion)

        player_hits = pygame.sprite.spritecollide(self.player, self.bullets, True)
        for bullet in player_hits:
            self.player.shield -= 20
            explosion = Explosion(bullet.rect.center)
            self.all_sprites.add(explosion)

        # check if a shield hits a robot
        opponent_hits = pygame.sprite.spritecollide(self.opponent, self.shields, True)
        self.opponent.shield = min(self.opponent.shield + 20 * len(opponent_hits), 100)

        player_hits = pygame.sprite.spritecollide(self.player, self.shields, True)
        self.player.shield = min(self.player.shield + 20 * len(player_hits), 100)

        now = pygame.time.get_ticks()
        if now - self.last_shield > shield_freq:
            x = randint(-900, 1900)
            self.generate_shield(x)

            # send the robot location to opponent
            connection_starter.conn.write('SHIELD', f'{connection_starter.conn.msg_protocol.data.opponent_id}:{x}')
            self.last_shield = now

    def game_events(self, event):
        # too many tasks for a single thread- i would ignore this functionality for now

        # check mouse clicked event for add platforms
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     x, y = pygame.mouse.get_pos()
        #     p = Platform(x - 75, y, 150, 20)
        #     self.all_sprites.add(p)
        #     self.platforms.add(p)
        #     self.platforms_list.append(p)

        # add the key to the text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.text_mode:
                self.player.shoot()
            elif self.text_mode:
                self.text = concat_char(self.text, pygame.key.name(event.key))
                if pygame.key.name(event.key) == 'return':
                    # sent message to opponent
                    connection_starter.conn.write('SEND', self.text)
                    # add to chat
                    self.add_msg(self.player.name, self.text)
                    self.text = ""

        # check for closing window
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False
            connection_starter.conn.terminate_connection()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.text_mode = not self.text_mode

    # draw all objects on the screen
    def draw(self):
        if not self.game_over:
            # draw background
            self.game_cycle()
            rel_x = self.background_x % background.get_rect().width
            screen.blit(background, (rel_x - background.get_rect().width, 0))
            if rel_x < WIDTH:
                screen.blit(background, (rel_x, 0))

            self.all_sprites.draw(screen)

            # draw all text on screen
            draw_text(screen, "position: ({:f}, {:f})".format(self.player.pos.x - self.background_x,
                                                              self.player.pos.y),
                      20, WIDTH / 2, 10, 'black')

            # draw textbox on screen
            if self.text_mode:
                draw_text(screen, "Chat: ", 20, 30, HEIGHT - 40, "white")

            pygame.draw.rect(screen, pygame.Color('white'), text_box, 0)
            text_color = "black"
            if len(self.text) >= 40:
                text_color = "red"
            draw_text(screen, self.text, 15, 200, HEIGHT - 40, text_color)

            # draw chat
            draw_msg_stack(screen, self.chat, 15, "black")

            # draw shields
            draw_shield_bar(screen, 5, 5, self.player.shield, 'green')
            draw_shield_bar(screen, WIDTH - 155, 5, self.opponent.shield, 'red')

        else:  # draw game over screen
            screen.blit(background, (0, 0))
            display_winner = 'The winner is: '
            draw_text(screen, "Game Over", 80, 180, 260, "white")

            if self.player.shield == 0:
                display_winner += connection_starter.conn.msg_protocol.data.opponent_name
            else:
                display_winner += self.player.name

            draw_text(screen, display_winner, 60, 400, 400, "white")

        # after drawing everything, flip the display
        pygame.display.flip()

    def add_msg(self, name, msg):
        self.chat.append(name + ":   " + msg)

    def platforms_movement_mode(self, mode):
        for p in self.platforms_list:
            p.change_mode(mode)

    def shields_movement_mode(self, mode):
        for p in self.shield_list:
            p.change_mode(mode)

    def generate_shield(self, x):
        shield = Shield(x)
        self.all_sprites.add(shield)
        self.shields.add(shield)
        self.shield_list.append(shield)

    def observer_update(self, subject):
        msg = subject.received_msg
        content = get_content(msg)
        if 'SEND:' in msg:
            self.add_msg(subject.opponent_name, content)
        elif 'LOCATION:' in msg:
            match = re.match(r'\(([-/+]?\d+\.\d+),([-/+]?\d+\.\d+)\):(\S+):(\S+)', content)  # regex
            x_pos = float(match.group(1)) + self.background_x
            self.opponent.change_state(x_pos, float(match.group(2)), match.group(3), match.group(4))
        elif 'SHOOT:' in msg:
            self.opponent.shoot()
        elif 'SHIELD:' in msg:
            match = re.match(r'([-/+]?\d+)', content)  # regex
            self.generate_shield(int(match.group(1)))
        elif 'DEAD:' in msg:
            self.opponent.die()


# python -m PresentationLayer.Login

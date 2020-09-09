import os

import pygame

from BusinessLayer.Game.Bullet import Bullet
from BusinessLayer.Game.Settings import DIRECTIONS, PLAYER_ACC, PLAYER_GRAVITY, PLAYER_FRICTION, HEIGHT

vec = pygame.math.Vector2

filepath = os.path.dirname(__file__)

robot_sprite = {'Idle': [[], 10], 'Jump': [[], 10], 'Run': [[], 8],
                'Shoot': [[], 4], 'Slide': [[], 10], 'Dead': [[], 10]}


# generate a map structure that contains all the states the robot can be during the game
def create_sprite():
    for key in robot_sprite:
        for i in range(robot_sprite[key][1]):
            filename = '../../img/robot/' + key + '__{}_-removebg-preview.png'.format(i + 1)
            img = pygame.image.load(os.path.join(filepath, filename)).convert()
            img.set_colorkey((0, 0, 0))
            robot_sprite[key][0].append(img)


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, board):
        create_sprite()
        pygame.sprite.Sprite.__init__(self)
        self.game = board
        self.current_pos = "Idle"
        self.image = robot_sprite["Idle"][0][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_direction = DIRECTIONS[1]
        self.shield = 100
        # for sprite functionality
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 55

    # take care of key pressed event
    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_RIGHT]:
                self.move_right()
            elif key_state[pygame.K_LEFT]:
                self.move_left()
            # the bend-sprite isn't aligned like the other sprites,
            # and thus makes some difficulties in the collision.
            # elif key_state[pygame.K_DOWN]:
                # self.bend()
            elif key_state[pygame.K_UP]:
                self.jump()
            elif key_state[pygame.K_SPACE]:
                self.shoot_pos()
            else:
                self.idle()

            # apply friction
            self.acc.x += self.vel.x * PLAYER_FRICTION
            # equations of motion
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            # check that the robot doesnt pass the screen boundaries
            if self.rect.bottom > HEIGHT - 55:
                if self.current_pos != "Slide":
                    self.rect.bottom = HEIGHT - 60
                else:
                    self.rect.bottom = HEIGHT - 10
            else:
                self.rect.midbottom = self.pos

    def move_right(self):
        self.current_pos = "Run"
        self.image = robot_sprite["Run"][0][self.frame % robot_sprite["Run"][1]]
        self.last_direction = DIRECTIONS[1]
        if self.rect.centerx < 500:
            self.pos.x += PLAYER_ACC * 15
        elif self.rect.centerx < 945 and self.game.background_x <= -1000:
            self.pos.x += PLAYER_ACC * 15

    def move_left(self):
        self.current_pos = "Run"
        img = robot_sprite["Run"][0][self.frame % robot_sprite["Run"][1]]
        flipped_img = pygame.transform.flip(img, True, False)
        self.image = flipped_img
        self.last_direction = DIRECTIONS[0]
        if self.rect.centerx > 500:
            self.pos.x -= PLAYER_ACC * 15
        elif self.rect.centerx > 55 and self.game.background_x >= 1000:
            self.pos.x -= PLAYER_ACC * 15

    # update the current frame of the sprite according the last direction the robot moved
    def sprite_by_direction(self, sprite):
        img = robot_sprite[sprite][0][self.frame % robot_sprite[sprite][1]]
        if self.last_direction == DIRECTIONS[1]:
            self.image = img
        else:
            self.image = pygame.transform.flip(img, True, False)

    def idle(self):
        self.current_pos = "Idle"
        self.sprite_by_direction("Idle")

    def bend(self):
        self.current_pos = "Slide"
        self.sprite_by_direction("Slide")
        self.rect.bottom += 50

    def jump(self):
        self.current_pos = "Jump"
        self.sprite_by_direction("Jump")
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        counter = 0
        for hit in hits:
            if hit.rect.top == self.pos.y:
                counter += 1

        if counter > 0:
            self.vel.y = -20

    def shoot_pos(self):
        self.current_pos = "Shoot"
        self.sprite_by_direction("Shoot")

    def shoot(self):
        x_offset = 30
        if self.last_direction == DIRECTIONS[0]:
            x_offset = -30
        bullet = Bullet(self.rect.centerx + x_offset, self.rect.centery, self.last_direction)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

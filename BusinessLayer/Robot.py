import pygame

from BusinessLayer.Settings import BLACK, DIRECTION, PLAYER_ACC, PLAYER_GRAVITY, PLAYER_FRICTION

vec = pygame.math.Vector2


robot_sprite = {'Idle': [[], 10], 'Jump': [[], 10], 'JumpMelee': [[], 8], 'Melee': [[], 8], 'Run': [[], 8],
                'RunShoot': [[], 9], 'Shoot': [[], 4], 'Slide': [[], 10], 'Dead': [[], 10]}


def create_sprite():
    for key in robot_sprite:
        for i in range(robot_sprite[key][1]):
            filename = '../img/robot/'+key+' ({}).png'.format(i + 1)
            img = pygame.image.load(filename).convert()
            img.set_colorkey(BLACK)
            img_robot = pygame.transform.scale(img, (250, 250)).convert()
            robot_sprite[key][0].append(img_robot)


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y, board):
        create_sprite()
        pygame.sprite.Sprite.__init__(self)
        self.game = board
        self.image = robot_sprite["Idle"][0][0]
        self.rect = self.image.get_rect()
        # self.radius = 20
        self.rect.centerx = x
        self.rect.bottom = y
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_direction = DIRECTION[1]
        # for sprite functionality
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 55

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
            elif key_state[pygame.K_DOWN]:
                self.bend()
            elif key_state[pygame.K_UP]:
                self.jump()
            else:
                self.idle()

            # apply friction
            self.acc.x += self.vel.x * PLAYER_FRICTION
            # equations of motion
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            self.rect.midbottom = self.pos

    def move_right(self):
        self.image = robot_sprite["Run"][0][self.frame % robot_sprite["Run"][1]]
        self.last_direction = DIRECTION[1]
        if self.rect.centerx < 500:
            self.pos.x += PLAYER_ACC * 15
        elif self.rect.centerx < 945 and self.game.background_x <= -1000:
            self.pos.x += PLAYER_ACC * 15

    def move_left(self):
        img = robot_sprite["Run"][0][self.frame % robot_sprite["Run"][1]]
        flipped_img = pygame.transform.flip(img, True, False)
        self.image = flipped_img
        self.last_direction = DIRECTION[0]
        if self.rect.centerx > 500:
            self.pos.x -= PLAYER_ACC * 15
        elif self.rect.centerx > 55 and self.game.background_x >= 1000:
            self.pos.x -= PLAYER_ACC * 15

    def sprite_by_direction(self, sprite):
        img = robot_sprite[sprite][0][self.frame % robot_sprite[sprite][1]]
        if self.last_direction == DIRECTION[1]:
            self.image = img
        else:
            self.image = pygame.transform.flip(img, True, False)

    def idle(self):
        self.sprite_by_direction("Idle")

    def bend(self):
        self.sprite_by_direction("Slide")

    def jump(self):
        self.sprite_by_direction("Jump")

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -20

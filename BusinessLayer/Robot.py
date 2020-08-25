import pygame

BLACK = (0, 0, 0)
DIRECTION = ("left", "right")
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
    def __init__(self, x, y):
        create_sprite()
        pygame.sprite.Sprite.__init__(self)
        self.image = robot_sprite["Idle"][0][0]
        self.rect = self.image.get_rect()
        # self.radius = 20
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedx = 6
        self.last_direction = DIRECTION[1]
        # for sprite functionality
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_RIGHT]:
                self.move_right()
            elif key_state[pygame.K_LEFT]:
                self.move_left()
            else:
                self.idle()

    def move_right(self):
        self.image = robot_sprite["Run"][0][self.frame % robot_sprite["Run"][1]]
        self.last_direction = DIRECTION[1]

    def move_left(self):
        img = robot_sprite["Run"][0][self.frame % robot_sprite["Run"][1]]
        flipped_img = pygame.transform.flip(img, True, False)
        self.image = flipped_img
        self.last_direction = DIRECTION[0]

    def idle(self):
        img = robot_sprite["Idle"][0][self.frame % robot_sprite["Idle"][1]]
        if self.last_direction == DIRECTION[1]:
            self.image = img
        else:
            self.image = pygame.transform.flip(img, True, False)


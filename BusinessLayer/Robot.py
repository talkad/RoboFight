import pygame

BLACK = (0, 0, 0)
robot_sprite = {'idle': [], 'jump': [], 'jump_melee': [], 'run': [],
                'run_shoot': [], 'shoot': [], 'slide': [], 'dead': []}


def create_sprite():
    for i in range(10):
        filename = '../img/robot/idle ({}).png'.format(i + 1)
        img = pygame.image.load(filename).convert()
        img.set_colorkey(BLACK)
        img_robot = pygame.transform.scale(img, (250, 250)).convert()
        robot_sprite['idle'].append(img_robot)


class Robot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        create_sprite()
        pygame.sprite.Sprite.__init__(self)
        self.image = robot_sprite["idle"][0]
        self.rect = self.image.get_rect()
        # self.radius = 20
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 0
        # for sprite functionality
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            center = self.rect.center
            self.image = robot_sprite["idle"][self.frame % 8]
            self.rect = self.image.get_rect()
            self.rect.center = center

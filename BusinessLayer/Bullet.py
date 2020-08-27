import pygame

from BusinessLayer.Settings import DIRECTIONS

SPEED = 5
bullet_sprite = {'Bullet': [[], 5], 'Muzzle': [[], 5]}


# generate a map structure that contains all the states the robot can be during the game
def create_sprite():
    for key in bullet_sprite:
        for i in range(bullet_sprite[key][1]):
            filename = '../img/robot/Objects/' + key + '_00{}.png'.format(i)
            img = pygame.image.load(filename).convert()
            img.set_colorkey(pygame.Color('black'))
            img_bullet = pygame.transform.scale(img, (30, 30)).convert()
            bullet_sprite[key][0].append(img_bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        create_sprite()
        self.image = bullet_sprite['Bullet'][0][0]
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 55
        self.direction = direction

    # update the current frame of the sprite according the last direction the robot moved
    def sprite_by_direction(self, sprite):
        img = bullet_sprite[sprite][0][self.frame % bullet_sprite[sprite][1]]
        if self.direction == DIRECTIONS[1]:
            self.image = img
        else:
            self.image = pygame.transform.flip(img, True, False)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            self.sprite_by_direction('Bullet')

        if self.direction == DIRECTIONS[1]:
            self.rect.x += SPEED
        else:
            self.rect.x -= SPEED

        # kill if it moves off the top of the screen
        if self.rect.left > 1850 or self.rect.left < -1000:
            self.kill()

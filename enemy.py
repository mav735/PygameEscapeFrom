import pygame
import configparser


class Enemy(pygame.sprite.Sprite):
    """Main class of enemy"""

    def __init__(self, start_point):
        """:parameter start_point: (x,y) spawn point of player"""
        pygame.sprite.Sprite.__init__(self)

        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        self.screen_resolution = list(
            map(int, config['Resolution']['resolution'].rstrip().split(', ')))
        self.cell_size = int(config['Cell_size']['cell_size'])

        self.x = (self.screen_resolution[0] / 2) - (
                    self.cell_size * start_point[0] + 0.5 * self.cell_size)
        self.y = (self.screen_resolution[1] / 2) - (
                    self.cell_size * start_point[1] + 0.5 * self.cell_size)

        self.health = 100

        self.image = pygame.transform.scale(pygame.image.load('').convert_alpha(),
                                            (self.cell_size * 0.5, self.cell_size * 0.7))
        self.rect = self.image.get_rect()
        self.Reversed = False  # swap animation reverse

    def get_coords(self):
        """:returns coords of players(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        self.x += 0.041 * self.cell_size * coefficient

    def y_move(self, coefficient):
        self.y += 0.041 * self.cell_size * coefficient

    def movement(self, map_profile):
        """Checking clicked buttons, if they used to move player"""
        keys = pygame.key.get_pressed()
        if keys:
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.collision(map_profile, 'up'):
                self.y_move(1)
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.collision(map_profile, 'down'):
                self.y_move(-1)
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.collision(map_profile, 'left'):
                self.x_move(1)
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.collision(map_profile, 'right'):
                self.x_move(-1)

    def collision(self, map_profile, direction):
        point = [(self.x - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size),
                 (self.y - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size)]
        if direction == 'up':
            point[1] = ((self.y + 0.041 * self.cell_size) -
                        (self.screen_resolution[1] / 2)) / (-1 * self.cell_size)
        elif direction == 'down':
            point[1] = ((self.y - self.rect.h / 2 - 0.041 * self.cell_size) -
                        (self.screen_resolution[1] / 2)) / (-1 * self.cell_size)
        elif direction == 'left':
            point[0] = ((self.x + self.rect.w / 2 + 0.041 * self.cell_size) -
                        (self.screen_resolution[0] / 2)) / (-1 * self.cell_size)
        elif direction == 'right':
            point[0] = ((self.x - self.rect.w / 2 - 0.041 * self.cell_size) -
                        (self.screen_resolution[0] / 2)) / (-1 * self.cell_size)

        return map_profile[int(point[0])][int(point[1])] == '1'

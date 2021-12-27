import pygame
import configparser


class Enemy(pygame.sprite.Sprite):
    """Main class of enemy"""

    def __init__(self, start_point):
        """:parameter start_point: (x,y) spawn point of enemy"""
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

        self.file_path = r'EnemyImg\Dolphin\Dolphin.png'
        self.image = pygame.transform.scale(pygame.image.load(self.file_path).convert_alpha(),
                                            (self.cell_size * 0.7, self.cell_size * 0.5))
        self.rect = self.image.get_rect()
        self.rect.move(start_point)
        self.Reversed = False  # swap animation reverse

    def get_coords(self):
        """:returns coords of enemy(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        self.rect.x += 0.041 * self.cell_size * coefficient

    def y_move(self, coefficient):
        self.rect.y += 0.041 * self.cell_size * coefficient

    def movement(self, map_profile):
        """Checking clicked buttons"""
        keys = pygame.key.get_pressed()
        if keys:
            if keys[pygame.K_UP]:
                self.y_move(1)
            if keys[pygame.K_DOWN]:
                self.y_move(-1)
            if keys[pygame.K_LEFT]:
                self.x_move(1)
            if keys[pygame.K_RIGHT]:
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

    def resize_scale(self, new_cell_size):
        """:parameter new_cell_size: Need rescaled size of cell"""

        self.image = pygame.transform.scale(pygame.image.load(self.file_path),
                                             (new_cell_size * 0.7, new_cell_size * 0.5))

        point = ((self.x - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size),
                 (self.y - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size))

        self.x = (self.screen_resolution[0] / 2) - (new_cell_size * point[0])
        self.y = (self.screen_resolution[1] / 2) - (new_cell_size * point[1])

        self.cell_size = new_cell_size

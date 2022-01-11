import pygame
import configparser


class Entity(pygame.sprite.Sprite):
    """Main class of enemy"""

    def __init__(self, start_point, player_pos):
        """:parameter start_point: (x,y) spawn point of enemy
           :parameter player_pos: actual position of player(camera)"""
        pygame.sprite.Sprite.__init__(self)

        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        self.screen_resolution = list(
            map(int, config['Resolution']['resolution'].rstrip().split(', ')))
        self.cell_size = int(config['Cell_size']['cell_size'])

        self.x = player_pos[0] + start_point[0] * self.cell_size
        self.y = player_pos[1] + start_point[1] * self.cell_size
        self.damage = 1
        self.health = 100

        self.file_path = r'EnemyImg\Dolphin\Dolphin.png'
        self.image = pygame.transform.scale(pygame.image.load(self.file_path).convert_alpha(),
                                            (self.cell_size * 0.7, self.cell_size * 0.5))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_player_pos = list(player_pos)
        self.Reversed = False  # swap animation reverse

    def get_coords(self):
        """:returns coords of enemy(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord x"""
        self.last_player_pos[0] += 0.041 * self.cell_size * coefficient

    def y_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord y"""
        self.last_player_pos[1] += 0.041 * self.cell_size * coefficient

    def movement(self, map_profile):
        """Checking clicked buttons
           :parameter map_profile: need board info [[len(50)]]"""
        directions = ['', '']
        if self.x - self.screen_resolution[0] / 2 < -80:
            x_derivative = 1
            directions[0] = 'right'
        elif self.x > self.screen_resolution[0] / 2:
            x_derivative = -1
            directions[0] = 'left'
        else:
            x_derivative = 0

        if self.y - self.screen_resolution[1] / 2 < -10:
            y_derivative = 1
            directions[1] = 'down'
        elif self.y > self.screen_resolution[1] / 2:
            y_derivative = -1
            directions[1] = 'up'
        else:
            y_derivative = 0

        if 0 <= self.x < self.screen_resolution[0] and 0 <= self.y < self.screen_resolution[1]:
            if self.collision(map_profile, directions[0]) and self.collision(map_profile, directions[1]):
                self.last_player_pos[0] += 0.021 * self.cell_size * x_derivative * -1
                self.last_player_pos[1] += 0.021 * self.cell_size * y_derivative * -1
            elif self.collision(map_profile, directions[0]):
                self.last_player_pos[0] += 0.021 * self.cell_size * x_derivative * -1
            elif self.collision(map_profile, directions[1]):
                self.last_player_pos[1] += 0.021 * self.cell_size * y_derivative * -1

    def collision(self, map_profile, direction):
        """:parameter map_profile: need board info [[len(50)]]
           :parameter direction: gets str direction of movement object"""
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        if direction == 'up':
            point[1] = (self.y - (self.last_player_pos[1] + 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'down':
            point[1] = (self.y - (self.last_player_pos[1] - 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'left':
            point[0] = (self.x - (self.last_player_pos[0] + 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'right':
            point[0] = (self.x - (self.last_player_pos[0] - 0.081 * self.cell_size)) / self.cell_size
        else:
            return True
        return map_profile[int(round(point[0]))][int(round(point[1]))] == '1'

    def attack(self):
        if abs(self.x - self.screen_resolution[0] / 2) < 90 and abs(self.y - self.screen_resolution[1] / 2) < 50:
            return True

    def resize_scale(self, new_cell_size, player_pos):
        """:parameter player_pos: new position of player
           :parameter new_cell_size: Need rescaled size of cell"""
        self.image = pygame.transform.scale(pygame.image.load(self.file_path),
                                            (new_cell_size * 0.7, new_cell_size * 0.5))

        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        self.x = player_pos[0] + point[0] * new_cell_size
        self.y = player_pos[1] + point[1] * new_cell_size

        self.cell_size = new_cell_size

    def update(self, player_pos):
        if self.health <= 0:
            self.kill()
        else:
            print(self.health)
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        self.x = player_pos[0] + point[0] * self.cell_size
        self.y = player_pos[1] + point[1] * self.cell_size
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_player_pos = list(player_pos)

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
        keys = pygame.key.get_pressed()
        if keys:
            if keys[pygame.K_UP] and self.collision(map_profile, 'up'):
                self.y_move(1)
            if keys[pygame.K_DOWN] and self.collision(map_profile, 'down'):
                self.y_move(-1)
            if keys[pygame.K_LEFT] and self.collision(map_profile, 'left'):
                self.x_move(1)
            if keys[pygame.K_RIGHT] and self.collision(map_profile, 'right'):
                self.x_move(-1)

    def MoveToPlayer(self, player_coords):
        """:parameter player_coords: coords of players"""
        if 0 <= self.x < self.screen_resolution[0] and 0 <= self.y < self.screen_resolution[1]:
            pass

    def collision(self, map_profile, direction):
        """:parameter map_profile: need board info [[len(50)]]
           :parameter direction: gets str direction of movement object"""
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        if direction == 'up':
            point[1] = (self.y - (self.last_player_pos[1] + 0.041 * self.cell_size)) / self.cell_size
        elif direction == 'down':
            point[1] = (self.y - (self.last_player_pos[1] - 0.041 * self.cell_size)) / self.cell_size
        elif direction == 'left':
            point[0] = (self.x - (self.last_player_pos[0] + 0.041 * self.cell_size)) / self.cell_size
        elif direction == 'right':
            point[0] = (self.x - (self.last_player_pos[0] - 0.041 * self.cell_size)) / self.cell_size
        return map_profile[int(round(point[0]))][int(round(point[1]))] == '1'

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
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        self.x = player_pos[0] + point[0] * self.cell_size
        self.y = player_pos[1] + point[1] * self.cell_size
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_player_pos = list(player_pos)

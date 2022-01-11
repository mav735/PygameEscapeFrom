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
        self.path = []
        self.Player_moved = True

    def get_coords(self):
        """:returns coords of enemy(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord x"""
        self.last_player_pos[0] += 0.041 * self.cell_size * coefficient

    def y_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord y"""
        self.last_player_pos[1] += 0.041 * self.cell_size * coefficient

    @staticmethod
    def neighbours(point):
        """Returns coordinates of neighbours of current point"""
        result = []
        for k in range(9):
            result.append([point[0] - 1 + k % 3, point[1] - 1 + k // 3])
        result = [p for p in result if -1 < p[0] < 50 and -1 < p[1] < 50]
        return result

    def movement(self, map_profile):
        """Checking clicked buttons
           :parameter map_profile: need board info [[len(50)]]"""

        if 0 <= self.x < self.screen_resolution[0] and 0 <= self.y < self.screen_resolution[1]:
            if self.Player_moved:
                self.find_path(map_profile)
                self.Player_moved = False
            entity_pos = [((self.x - self.last_player_pos[0]) / self.cell_size),
                          ((self.y - self.last_player_pos[1]) / self.cell_size)]

            if self.path:
                if entity_pos[0] > self.path[0][0]:
                    self.x_move(1)
                elif entity_pos[0] < self.path[0][0]:
                    self.x_move(-1)
                if entity_pos[1] > self.path[0][1]:
                    self.y_move(1)
                elif entity_pos[1] < self.path[0][1]:
                    self.y_move(-1)

                entity_pos = [((self.x - self.last_player_pos[0]) / self.cell_size),
                              ((self.y - self.last_player_pos[1]) / self.cell_size)]

                print(entity_pos, self.path[0])
                if abs(entity_pos[0] - self.path[0][0]) <= 0.05 and \
                        abs(entity_pos[1] - self.path[0][1]) <= 0.05:
                    del self.path[0]

    def find_path(self, map_profile):
        entity_pos = [round((self.x - self.last_player_pos[0]) / self.cell_size),
                      round((self.y - self.last_player_pos[1]) / self.cell_size)]
        player_pos = [round((self.x - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size)),
                      round((self.y - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size))]
        card = [[float('inf')] * 50 for _ in range(50)]
        card[entity_pos[0]][entity_pos[1]] = 0
        current = [entity_pos]
        to_check = []
        opened = [entity_pos]
        dist = 1
        while current:
            for cell in current:
                for point in self.neighbours(cell):
                    if point not in opened:
                        if map_profile[point[0]][point[1]] == '1':
                            card[point[0]][point[1]] = dist
                            opened.append(point)
                            to_check.append(point)

            if player_pos in opened:
                break

            current.clear()
            current = to_check.copy()
            to_check.clear()
            dist += 1

        self.path = [player_pos]
        value = card[player_pos[0]][player_pos[1]]
        while value > 0:
            for point in self.neighbours(self.path[-1]):
                if value > card[point[0]][point[1]]:
                    self.path.append(point)
                    value = card[point[0]][point[1]]
        self.path.pop()
        self.path.reverse()

    def collision(self, map_profile, direction):
        """:parameter map_profile: need board info [[len(50)]]
           :parameter direction: gets str direction of movement object"""
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        if direction == 'up':
            point[1] = (self.y - (
                        self.last_player_pos[1] + 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'down':
            point[1] = (self.y - (
                        self.last_player_pos[1] - 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'left':
            point[0] = (self.x - (
                        self.last_player_pos[0] + 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'right':
            point[0] = (self.x - (
                        self.last_player_pos[0] - 0.081 * self.cell_size)) / self.cell_size
        else:
            return True
        return map_profile[int(round(point[0]))][int(round(point[1]))] == '1'

    def attack(self):
        if abs(self.x - self.screen_resolution[0] / 2) < 90 and abs(
                self.y - self.screen_resolution[1] / 2) < 50:
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
            pass
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        self.x = player_pos[0] + point[0] * self.cell_size
        self.y = player_pos[1] + point[1] * self.cell_size
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_player_pos = list(player_pos)

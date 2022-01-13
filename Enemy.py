import pygame
import configparser
from collections import deque


# from numba import njit


class Entity(pygame.sprite.Sprite):
    """Main class of enemy"""

    def __init__(self, start_point, player_pos):
        """:parameter start_point: (x,y) spawn point of enemy
           :parameter player_pos: actual position of player(camera)"""
        pygame.sprite.Sprite.__init__(self)
        self.player_pos = (None, None)
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
        self.movement_list = [None]
        self.coords = [None, False, None]
        self.Player_moved = True

    def get_coords(self):
        """:returns coords of enemy(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord x"""
        self.last_player_pos[0] += 0.081 * self.cell_size * coefficient

    def y_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord y"""
        self.last_player_pos[1] += 0.081 * self.cell_size * coefficient

    @staticmethod
    def neighbours(point):
        """Returns coordinates of neighbours of current point"""
        result = []
        for k in range(9):
            dot = [point[0] - 1 + k % 3, point[1] - 1 + k // 3]
            if abs(dot[0] - point[0] + dot[1] - point[1]) > 1:
                continue
            result.append(dot)
        result = [p for p in result if -1 < p[0] < 50 and -1 < p[1] < 50]
        return result

    def movement(self, map_profile):
        """Checking clicked buttons
           :parameter map_profile: need board info [[len(50)]]"""

        if 0 <= self.x < self.screen_resolution[0] and 0 <= self.y < self.screen_resolution[1]:
            if len(self.path) <= 2:
                self.find_path(map_profile)
                self.coords = [None, False, None]
            entity_pos = [((self.x - self.last_player_pos[0]) / self.cell_size),
                          ((self.y - self.last_player_pos[1]) / self.cell_size)]
            print(entity_pos)

            if self.path:
                self.coords.append(entity_pos)
                if len(self.path) > 2:
                    if entity_pos[0] - self.path[0][0] > 0.1 and self.movement_list[-1] != 'right':
                        if self.collision(map_profile, 'left'):
                            self.x_move(1)
                            self.movement_list.append('left')
                            print('left', end=' ')
                    if self.path[0][0] - entity_pos[0] > 0.1 and self.movement_list[-1] != 'left':
                        if self.collision(map_profile, 'right'):
                            self.x_move(-1)
                            self.movement_list.append('right')
                            print('right', end=' ')

                    if entity_pos[1] - self.path[0][1] > 0.1 and self.movement_list[-1] != 'down':
                        if self.collision(map_profile, 'up'):
                            self.y_move(1)
                            self.movement_list.append('up')
                            print('up', end=' ')
                    if self.path[0][1] - entity_pos[1] > 0.1 and self.movement_list[-1] != 'up':
                        if self.collision(map_profile, 'down'):
                            self.y_move(-1)
                            self.movement_list.append('down')
                            print('down', end=' ')

                    entity_pos = [((self.x - self.last_player_pos[0]) / self.cell_size),
                                  ((self.y - self.last_player_pos[1]) / self.cell_size)]

                    if abs(entity_pos[0] - self.path[0][0]) + \
                            abs(entity_pos[1] - self.path[0][1]) <= 2:
                        del self.path[0]
                else:
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

                    if 0 <= self.x < self.screen_resolution[0] and 0 <= self.y < \
                            self.screen_resolution[1]:
                        if self.collision(map_profile, directions[0]) and self.collision(
                                map_profile, directions[1]):
                            self.last_player_pos[0] += 0.041 * self.cell_size * x_derivative * -1
                            self.last_player_pos[1] += 0.041 * self.cell_size * y_derivative * -1
                        elif self.collision(map_profile, directions[0]):
                            self.last_player_pos[0] += 0.041 * self.cell_size * x_derivative * -1
                        elif self.collision(map_profile, directions[1]):
                            self.last_player_pos[1] += 0.041 * self.cell_size * y_derivative * -1

    def find_path(self, map_profile):
        entity_pos = [int((self.x - self.last_player_pos[0]) / self.cell_size),
                      int((self.y - self.last_player_pos[1]) / self.cell_size)]
        player_pos = [
            int((self.player_pos[0] - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size)),
            int((self.player_pos[1] - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size))]

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
            point[1] = (self.y + self.rect.h - (
                    self.last_player_pos[1] + 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'down':
            point[1] = (self.y - self.rect.h - (
                    self.last_player_pos[1] - 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'left':
            point[0] = (self.x + self.rect.w - (
                    self.last_player_pos[0] + 0.081 * self.cell_size)) / self.cell_size
        elif direction == 'right':
            point[0] = (self.x - self.rect.w - (
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

        for element in self.anime:
            for index in range(len(self.anime[element][1])):
                pygame.transform.scale(
                    pygame.image.load(self.anime[element][3][index]),
                    (new_cell_size, new_cell_size))

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


class EnemyBeast(Entity):
    def __init__(self, start_point, player_pos):
        super().__init__(start_point, player_pos)
        self.last_anime = None
        self.attack_counter = 0
        self.stay_list = [rf'EnemyImg\Fantasy Beast\Stand\stand{i}.png' for i in range(7)]
        self.walk_list = [rf'EnemyImg\Fantasy Beast\Walk\walk{i}.png' for i in range(5)]
        self.death_list = [rf'EnemyImg\Fantasy Beast\Death\death{i}.png' for i in range(3)]
        self.attack_list_1 = [rf'EnemyImg\Fantasy Beast\Attack1\attack{i}.png' for i in range(5)]
        self.death_counter = 0
        self.anime = {'stay': [True, deque([pygame.transform.scale
                                            (pygame.image.load
                                             (element).convert_alpha(),
                                             (self.cell_size * 1.3, self.cell_size * 1))
                                            for element in self.stay_list]), 0, self.stay_list],
                      'move': [False, deque([pygame.transform.scale
                                             (pygame.image.load
                                              (element).convert_alpha(),
                                              (self.cell_size * 1.3, self.cell_size * 1))
                                             for element in self.walk_list]), 0, self.walk_list],
                      'death': [False, deque([pygame.transform.scale
                                              (pygame.image.load
                                               (element).convert_alpha(),
                                               (self.cell_size * 1.3, self.cell_size * 1))
                                              for element in self.death_list]), 0, self.death_list],
                      'attack': [False, deque([pygame.transform.scale
                                               (pygame.image.load
                                                (element).convert_alpha(),
                                                (self.cell_size * 1.3, self.cell_size * 1))
                                               for element in self.attack_list_1]), 0,
                                 self.attack_list_1]
                      }

    def attack(self):
        if abs(self.x - self.screen_resolution[0] / 2) < 90 and abs(
                self.y - self.screen_resolution[1] / 2) < 50:
            self.anime['attack'][0] = True
            return True

    def x_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord x"""
        self.anime['move'][0] = True
        self.last_player_pos[0] += 0.081 * self.cell_size * coefficient

    def y_move(self, coefficient):
        """:parameter coefficient: (1 or -1) means derivative coord y"""
        self.anime['move'][0] = True
        self.last_player_pos[1] += 0.081 * self.cell_size * coefficient

    def update(self, player_pos):
        point = [(self.x - self.last_player_pos[0]) / self.cell_size,
                 (self.y - self.last_player_pos[1]) / self.cell_size]
        self.player_pos = player_pos
        self.x = player_pos[0] + point[0] * self.cell_size
        self.y = player_pos[1] + point[1] * self.cell_size
        self.last_player_pos = list(player_pos)

        if self.health <= 0:
            self.anime['death'][0] = True
            if self.anime['death'][2] != 20:
                self.anime['death'][2] += 1
            else:
                self.death_counter += 1
                self.anime['death'][2] = 0
                self.anime['death'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['death'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()

            if self.death_counter == 3:
                self.death_counter = 0
                self.kill()

            self.last_anime = 'death'
        elif self.anime['attack'][0]:
            if self.anime['attack'][2] != 4:
                self.anime['attack'][2] += 1
            else:
                self.attack_counter += 1
                self.anime['attack'][2] = 0
                self.anime['attack'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['attack'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()

            if self.attack_counter == 13:
                self.attack_counter = 0
                self.anime['attack'][0] = False

            self.last_anime = 'attack'

        elif self.anime['move'][0]:
            if self.anime['move'][2] != 12:
                self.anime['move'][2] += 1
            else:
                self.anime['move'][2] = 0
                self.anime['move'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['move'][1][0], self.Reversed, False)

            self.anime['move'][0] = False
            self.last_anime = 'move'

        elif self.anime['stay'][0]:
            if self.anime['stay'][2] != 7:
                self.anime['stay'][2] += 1
            else:
                self.anime['stay'][2] = 0
                self.anime['stay'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['stay'][1][0], self.Reversed, False)

            self.last_anime = 'stay'

        self.rect.x = self.x
        self.rect.y = self.y

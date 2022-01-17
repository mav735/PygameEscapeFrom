import pygame
from collections import deque
import configparser


class Player(pygame.sprite.Sprite):
    """Main class of player, that contents coords of cam"""

    def __init__(self, start_point, end_point):
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
        self.max_hp = 100 + int(config['Game']['health_lvl']) * 50
        self.damage = 10 + int(config['Game']['strength_lvl']) * 5
        self.death_counter = 0
        self.attack_counter = 0
        self.health = 100 + int(config['Game']['health_lvl']) * 50
        self.all_money = int(config['Game']['money'])
        self.mana = 2000
        self.armor = 0
        self.inventory = []
        self.current_object = None
        self.last_anime = None
        self.stay_list = [rf'PlayerImg\StayAnimation\stay{i}.png' for i in range(10)]
        self.walk_list = [rf'PlayerImg\MovingAnimation\walk{i}.png' for i in range(8)]
        self.death_list = [rf'PlayerImg\DeathAnimation\death{i}.png' for i in range(16)][::-1]
        self.attack_list_1 = [rf'PlayerImg\AttackAnimation\attack{i}.png' for i in range(13)]
        self.anime = {'stay': [True, deque([pygame.transform.scale
                                            (pygame.image.load
                                             (element).convert_alpha(),
                                             (self.cell_size * 0.5, self.cell_size * 0.7))
                                            for element in self.stay_list]), 0, self.stay_list],
                      'move': [False, deque([pygame.transform.scale
                                             (pygame.image.load
                                              (element).convert_alpha(),
                                              (self.cell_size * 0.5, self.cell_size * 0.7))
                                             for element in self.walk_list]), 0, self.walk_list],
                      'death': [False, deque([pygame.transform.scale
                                              (pygame.image.load
                                               (element).convert_alpha(),
                                               (self.cell_size * 1.2, self.cell_size))
                                              for element in self.death_list]), 0, self.death_list],
                      'attack': [False, deque([pygame.transform.scale
                                               (pygame.image.load
                                                (element).convert_alpha(),
                                                (self.cell_size * 1.5, self.cell_size * 2.3))
                                               for element in self.attack_list_1]), 0, self.attack_list_1]
                      }

        self.image = self.anime['stay'][1][0]
        self.rect = self.image.get_rect()
        self.Reversed = False  # swap animation reverse
        self.mask = pygame.mask.from_surface(self.image)
        self.monolith = end_point
        self.max_mana = 2000

    def get_coords(self):
        """:returns coords of players(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        speed = 0.041 + 0.041 / 8 * int(config['Game']['speed_lvl'])
        self.x += speed * self.cell_size * coefficient

    def y_move(self, coefficient):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        speed = 0.041 + 0.041 / 8 * int(config['Game']['speed_lvl'])
        self.y += speed * self.cell_size * coefficient

    def self_kill(self):
        self.health -= 100

    def movement(self, map_profile):
        """Checking clicked buttons, if they used to move player"""
        keys = pygame.key.get_pressed()
        Flag = False  # swap animation of stay/move
        if keys:
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.collision(map_profile, 'up'):
                self.y_move(1)
                self.anime['move'][0] = True
                Flag = True
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.collision(map_profile, 'down'):
                self.y_move(-1)
                self.anime['move'][0] = True
                Flag = True
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.collision(map_profile, 'left'):
                self.x_move(1)
                self.anime['move'][0] = True
                Flag = True
                self.Reversed = True
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.collision(map_profile, 'right'):
                self.x_move(-1)
                self.anime['move'][0] = True
                Flag = True
                self.Reversed = False
        if not Flag:
            self.anime['move'][0] = False
            self.anime['stay'][0] = True

    def end(self):
        point = [int((self.x - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size)),
                 int((self.y - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size))]
        result = []
        for k in range(9):
            dot = [int(point[0] - 1 + k % 3), int(point[1] - 1 + k // 3)]
            result.append(dot)
        return self.monolith in result

    def attack(self):
        if self.mana > 150:
            self.anime['move'][0] = False
            self.anime['stay'][0] = False
            self.anime['attack'][0] = True

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
        for element in self.anime:
            for index in range(len(self.anime[element][1])):
                if element != 'attack' and element != 'death':
                    self.anime[element][1][index] = pygame.transform.scale(
                        pygame.image.load(self.anime[element][3][index]),
                        (new_cell_size * 0.5, new_cell_size * 0.7))
                elif element == 'death':
                    self.anime[element][1][index] = pygame.transform.scale(
                        pygame.image.load(self.anime[element][3][index]),
                        (new_cell_size * 1.2, new_cell_size))
                else:
                    self.anime[element][1][index] = pygame.transform.scale(
                        pygame.image.load(self.anime[element][3][index]),
                        (new_cell_size * 1.5, new_cell_size * 2.3))

        point = ((self.x - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size),
                 (self.y - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size))

        self.x = (self.screen_resolution[0] / 2) - (new_cell_size * point[0])
        self.y = (self.screen_resolution[1] / 2) - (new_cell_size * point[1])

        self.cell_size = new_cell_size

    def death(self):
        if self.health <= 0:
            config = configparser.ConfigParser()
            config.read('Settings.cfg')
            config['Game']['end'] = 'True'
            with open('Settings.cfg', 'w') as configfile:
                config.write(configfile)

        return self.health <= 0

    def update(self):
        """Draw animation of deque for player"""
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        self.health = min(int(config['Game']['regeneration_lvl']) / 120 + self.health, self.max_hp)
        if self.health <= 0:
            self.anime['death'][0] = True
            if self.anime['death'][2] != 4:
                self.anime['death'][2] += 1
            else:
                self.death_counter += 1
                self.anime['death'][2] = 0
                self.anime['death'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['death'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(self.rect.size[0] * 0.2, self.rect.size[1] * -0.15)
                self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                    int(self.rect.y + 0.5 * self.screen_resolution[1]))

            if self.death_counter == 16:
                self.death_counter = 0
                self.death()

            self.last_anime = 'death'
        elif self.anime['attack'][0]:
            self.mana -= 4
            if self.anime['attack'][2] != 4:
                self.anime['attack'][2] += 1
            else:
                self.attack_counter += 1
                self.anime['attack'][2] = 0
                self.anime['attack'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['attack'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()
                self.rect = self.rect.move(self.rect.size[0] * 0.05, self.rect.size[1] * -0.35)
                self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                    int(self.rect.y + 0.5 * self.screen_resolution[1]))

            if self.attack_counter == 13:
                self.attack_counter = 0
                self.anime['attack'][0] = False

            self.last_anime = 'attack'

        elif self.anime['move'][0]:
            if self.anime['move'][2] != 7:
                self.anime['move'][2] += 1
            else:
                self.anime['move'][2] = 0
                self.anime['move'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['move'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()
                self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                    int(self.rect.y + 0.5 * self.screen_resolution[1]))
            self.last_anime = 'move'

        elif self.anime['stay'][0]:
            if self.anime['stay'][2] != 7:
                self.anime['stay'][2] += 1
            else:
                self.anime['stay'][2] = 0
                self.anime['stay'][1].rotate(1)
                self.image = pygame.transform.flip(self.anime['stay'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()
                self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                    int(self.rect.y + 0.5 * self.screen_resolution[1]))

            self.last_anime = 'stay'

        self.mask = pygame.mask.from_surface(self.image)
        self.mana = min(self.max_mana, self.mana + 0.1)

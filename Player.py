import pygame
from collections import deque


class Player(pygame.sprite.Sprite):
    """Main class of player, that contents coords of cam"""
    def __init__(self, start_point):
        """:parameter start_point: (x,y) spawn point of player"""
        pygame.sprite.Sprite.__init__(self)

        with open("Settings.cfg", "r") as SettingsFile:
            """Get global settings from Settings.cfg"""
            settings = SettingsFile.readlines()
            self.screen_resolution = list(map(int, settings[0].rstrip().split(', ')))
            self.cell_size = int(settings[-1].rstrip())

        self.x = (self.screen_resolution[0] / 2) - (self.cell_size * start_point[0] + 0.5 * self.cell_size)
        self.y = (self.screen_resolution[1] / 2) - (self.cell_size * start_point[1] + 0.5 * self.cell_size)

        self.health = 100
        self.mana = 2000
        self.armor = 0
        self.inventory = []
        self.current_object = None
        self.last_anime = None
        self.stay_list = [rf'PlayerImg\StayAnimation\stay{i}.png' for i in range(10)]
        self.walk_list = [rf'PlayerImg\MovingAnimation\walk{i}.png' for i in range(8)]
        self.anime = {'stay': [True, deque([pygame.transform.scale
                                            (pygame.image.load
                                             (element),
                                             (self.cell_size * 0.5, self.cell_size * 0.7))
                                            for element in self.stay_list]), 0, self.stay_list],  # max 7
                      'move': [False, deque([pygame.transform.scale
                                             (pygame.image.load
                                              (element),
                                              (self.cell_size * 0.5, self.cell_size * 0.7))
                                             for element in self.walk_list]), 0, self.walk_list],  # max 9
                      }

        self.image = self.anime['stay'][1][0]
        self.rect = self.image.get_rect()
        self.Reversed = False  # swap animation reverse

    def get_coords(self):
        """:returns coords of players(cam)"""
        return self.x, self.y

    def x_move(self, coefficient):
        self.x += 0.041 * self.cell_size * coefficient

    def y_move(self, coefficient):
        self.y += 0.041 * self.cell_size * coefficient

    def movement(self):
        """Checking clicked buttons, if they used to move player"""
        keys = pygame.key.get_pressed()
        Flag = False  # swap animation of stay/move
        if keys:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.y_move(1)
                self.anime['move'][0] = True
                Flag = True
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.y_move(-1)
                self.anime['move'][0] = True
                Flag = True
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.x_move(1)
                self.anime['move'][0] = True
                Flag = True
                self.Reversed = True
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.x_move(-1)
                self.anime['move'][0] = True
                Flag = True
                self.Reversed = False
        if not Flag:
            self.anime['move'][0] = False
            self.anime['stay'][0] = True

    def resize_scale(self, new_cell_size):
        """:parameter new_cell_size: Need rescaled size of cell"""
        for element in self.anime:
            for index in range(len(self.anime[element][1])):
                self.anime[element][1][index] = pygame.transform.scale(pygame.image.load(self.anime[element][3][index]),
                                                                       (new_cell_size * 0.5, new_cell_size * 0.7))

        point = ((self.x - (self.screen_resolution[0] / 2)) / (-1 * self.cell_size),
                 (self.y - (self.screen_resolution[1] / 2)) / (-1 * self.cell_size))

        self.x = (self.screen_resolution[0] / 2) - (new_cell_size * point[0])
        self.y = (self.screen_resolution[1] / 2) - (new_cell_size * point[1])

        self.cell_size = new_cell_size

    def update(self):
        """Draw animation of deque for player"""
        if self.anime['move'][0]:
            if self.last_anime == 'move':
                if self.anime['move'][2] != 7:
                    self.anime['move'][2] += 1
                else:
                    self.anime['move'][2] = 0
                    self.anime['move'][1].rotate()
                    self.image = pygame.transform.flip(self.anime['move'][1][0], self.Reversed, False)
                    self.rect = self.image.get_rect()
                    self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                        int(self.rect.y + 0.5 * self.screen_resolution[1]))
            else:
                if self.anime['move'][2] != 7:
                    self.anime['move'][2] += 1
                else:
                    self.anime['move'][2] = 0

                self.anime['move'][1].rotate()
                self.image = pygame.transform.flip(self.anime['move'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()
                self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                    int(self.rect.y + 0.5 * self.screen_resolution[1]))

            self.last_anime = 'move'

        elif self.anime['stay'][0]:
            if self.last_anime == 'stay':
                if self.anime['stay'][2] != 7:
                    self.anime['stay'][2] += 1
                else:
                    self.anime['stay'][2] = 0
                    self.anime['stay'][1].rotate()
                    self.image = pygame.transform.flip(self.anime['stay'][1][0], self.Reversed, False)
                    self.rect = self.image.get_rect()
                    self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                        int(self.rect.y + 0.5 * self.screen_resolution[1]))
            else:
                if self.anime['stay'][2] != 7:
                    self.anime['stay'][2] += 1
                else:
                    self.anime['stay'][2] = 0

                self.anime['stay'][1].rotate()
                self.image = pygame.transform.flip(self.anime['stay'][1][0], self.Reversed, False)
                self.rect = self.image.get_rect()
                self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                    int(self.rect.y + 0.5 * self.screen_resolution[1]))

            self.last_anime = 'stay'

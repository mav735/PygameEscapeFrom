import pygame
from collections import deque


class Player(pygame.sprite.Sprite):
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
        self.stay_list = [rf'PlayerImg\StayAnimation\stay{i}.png' for i in range(10) for _ in range(8)]
        self.walk_list = [rf'PlayerImg\MovingAnimation\walk{i}.png' for i in range(8) for _ in range(10)]
        self.anime = {'stay': [True, deque([pygame.transform.scale
                                            (pygame.image.load
                                             (element),
                                             (self.cell_size * 0.5, self.cell_size * 0.7))
                                            for element in self.stay_list])],
                      'move': [False, deque([pygame.transform.scale
                                             (pygame.image.load
                                              (element),
                                              (self.cell_size * 0.5, self.cell_size * 0.7))
                                             for element in self.walk_list])],
                      'damage': [False],
                      'attack': [False],
                      'die': [False]}

        self.image = self.anime['stay'][1][0]
        self.rect = self.image.get_rect()
        self.Reversed = False  # swap animation reverse

    def get_coords(self):
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
            if keys[pygame.K_w]:
                self.y_move(1)
                self.anime['move'][0] = True
                Flag = True
            if keys[pygame.K_s]:
                self.y_move(-1)
                self.anime['move'][0] = True
                Flag = True
            if keys[pygame.K_a]:
                self.x_move(1)
                self.anime['move'][0] = True
                Flag = True
                self.Reversed = True
            if keys[pygame.K_d]:
                self.x_move(-1)
                self.anime['move'][0] = True
                Flag = True
                self.Reversed = False
        if not Flag:
            self.anime['move'][0] = False
            self.anime['stay'][0] = True

    def update(self):
        """draw animation of deque for player"""
        if self.anime['stay'][0]:
            self.image = pygame.transform.flip(self.anime['stay'][1][0], self.Reversed, False)
            self.rect = self.image.get_rect()
            self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                int(self.rect.y + 0.5 * self.screen_resolution[1]))
            self.anime['stay'][1].rotate()
        if self.anime['move'][0]:
            self.image = pygame.transform.flip(self.anime['move'][1][0], self.Reversed, False)
            self.rect = self.image.get_rect()
            self.rect.center = (int(self.rect.x + 0.5 * self.screen_resolution[0]),
                                int(self.rect.y + 0.5 * self.screen_resolution[1]))
            self.anime['move'][1].rotate()

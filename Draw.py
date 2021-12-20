import pygame
import os


class DrawFloor:
    def __init__(self, screen, type_texture, Map):
        """:parameter screen: surface where you draw
           :parameter type_texture: key in self.materials"""
        self.screen = screen
        with open("Settings.cfg", "r") as SettingsFile:
            self.cell_size = int(SettingsFile.readlines()[-1].rstrip())
        self.type_texture = type_texture
        self.materials = {'1': pygame.transform.scale(pygame.image.load(os.path.join('Floor', 'floor1.png')),
                                                      (self.cell_size, self.cell_size)),
                          '2': pygame.transform.scale(pygame.image.load(os.path.join('Walls', 'wall2.png')),
                                                      (self.cell_size, self.cell_size)),
                          '3': pygame.transform.scale(pygame.image.load(os.path.join('Walls', 'wall3.png')),
                                                      (self.cell_size, self.cell_size)),
                          '4': pygame.transform.scale(pygame.image.load(os.path.join('Walls', 'wall4.png')),
                                                      (self.cell_size, self.cell_size)),
                          '5': pygame.transform.scale(pygame.image.load(os.path.join('Walls', 'wall5.png')),
                                                      (self.cell_size, self.cell_size)),
                          '6': pygame.transform.scale(pygame.image.load(os.path.join('Walls', 'wall6.png')),
                                                      (self.cell_size, self.cell_size)),
                          '7': pygame.transform.scale(pygame.image.load(os.path.join('Walls', 'wall7.png')),
                                                      (self.cell_size, self.cell_size))
                          }
        self.map = Map

    def blit_floor(self, coords):
        """:parameter coords: left and top border(x, y)"""
        for row in range(50):
            for column in range(50):
                if self.map[row][column] != '-1':
                    self.screen.blit(self.materials[str(self.map[row][column])],
                                     (coords[0] + row * self.cell_size,
                                      coords[1] + column * self.cell_size))

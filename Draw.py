import pygame
import os


class DrawFloor:
    def __init__(self, screen, type_texture, cell_size):
        """:parameter screen: surface where you draw
           :parameter type_texture: key in self.materials
           :parameter cell_size: stock size of cell"""
        self.screen = screen
        self.cell_size = cell_size
        self.type_texture = type_texture
        self.materials = {'1': os.path.join('Floor', 'wood.jpg')}
        self.image = pygame.transform.scale(pygame.image.load(self.materials[type_texture]),
                                            (self.cell_size, self.cell_size))

    def blit_floor(self, coords):
        """:parameter coords: left and top border(x, y)"""
        for row in range(50):
            for column in range(50):
                self.screen.blit(self.image, (coords[0] + row * self.cell_size, coords[1] + column * self.cell_size))


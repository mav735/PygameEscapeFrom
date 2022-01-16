import pygame
import os
import configparser


class DrawFloor:
    def __init__(self, screen, type_texture, Map):
        """:parameter screen: surface where you draw
           :parameter type_texture: key in self.materials"""
        self.screen = screen

        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        self.font = pygame.font.Font(rf'PlayerImg\hp.ttf', 32)
        self.cell_size = int(config['Cell_size']['cell_size'])
        self.screen_size = list(map(int, config['Resolution']['resolution'].split(', ')))
        self.type_texture = type_texture
        self.materials = {
            '1': pygame.transform.scale(
                pygame.image.load(os.path.join('Floor', 'floor1.png')).convert(),
                (self.cell_size, self.cell_size)),
            '2': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'wall2.png')).convert(),
                (self.cell_size, self.cell_size)),
            '3': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'wall3.png')).convert(),
                (self.cell_size, self.cell_size)),
            '4': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'wall4.png')).convert(),
                (self.cell_size, self.cell_size)),
            '5': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'wall5.png')).convert(),
                (self.cell_size, self.cell_size)),
            '6': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'wall6.png')).convert(),
                (self.cell_size, self.cell_size)),
            '7': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'wall7.png')).convert(),
                (self.cell_size, self.cell_size)),
            '8': pygame.transform.scale(
                pygame.image.load(os.path.join('Walls', 'monolith.png')).convert(),
                (self.cell_size, self.cell_size))
        }
        self.map = Map
        self.im = pygame.transform.scale(pygame.image.load(r'PlayerImg/coin.png').convert_alpha(),
                                         (int(self.cell_size) * 0.2, int(self.cell_size) * 0.2))
        self.coins_text = self.font.render(str(0), False, "YELLOW")
        self.coins_text_rect = self.coins_text.get_rect(center=(self.screen_size[0] - 100, 30))

    def blit_floor(self, coords):
        """:parameter coords: left and top border(x, y)"""
        for row in range(50):
            for column in range(50):
                if self.map[row][column] != '-1' and self.map[row][column] != '0':
                    self.screen.blit(self.materials[str(self.map[row][column])],
                                     (coords[0] + row * self.cell_size,
                                      coords[1] + column * self.cell_size))

    def blit_coins(self, coins):
        self.coins_text = self.font.render(str(coins), False, "YELLOW")
        self.coins_text_rect = self.coins_text.get_rect(center=(self.screen_size[0] - 25, 30))
        self.screen.blit(self.coins_text, self.coins_text_rect)
        self.screen.blit(self.im, (self.screen_size[0] - int(self.cell_size * 0.7), 15))


class InfoPlayer:
    def __init__(self, player):
        """:parameter player: gets player class for info"""
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        self.player = player
        self.max_hp = 100 + int(config['Game']['health_lvl']) * 50
        self.FRAME = pygame.image.load(rf'PlayerImg\player_icon_frame.png').convert_alpha()
        self.font = pygame.font.Font(rf'PlayerImg\hp.ttf', 32)

    def draw(self, screen: pygame.surface.Surface, position=(0, 0)):
        """
        Draw info about player
        :parameter screen: screen blit
        :parameter position: coords for frame
        """
        try:
            x1, y1 = (0, 0)
            image = pygame.surface.Surface(self.FRAME.get_size(), pygame.SRCALPHA)

            health_length = round(264 * (self.player.health / self.max_hp) + 0.5)
            health_line = pygame.surface.Surface((health_length, 24))
            health_line.fill((255, 30, 30))
            image.blit(health_line, (x1 + 132, y1 + 12))
            image.blit(self.font.render(f'{round(self.player.health + 0.5)}/' + f'{self.max_hp}',
                                        True, (255, 255, 255)), (x1 + 220, y1 + 10))

            mana_length = round(264 * (self.player.mana / 2000) + 0.5)
            mana_line = pygame.surface.Surface((mana_length, 24))
            mana_line.fill((30, 30, 255))
            image.blit(mana_line, (x1 + 132, y1 + 52))
            image.blit(self.font.render(f'{round(self.player.mana + 0.5)}/' +
                                        f'{self.player.mana}',
                                        True, (255, 255, 255)), (x1 + 220, y1 + 50))
            image.blit(self.FRAME, (0, 0))
            screen.blit(image, (0, 0))
        except pygame.error:
            pass

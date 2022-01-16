import pygame
import configparser


class Settings:
    def __init__(self, screen_info, resolution=None):
        """:parameter screen_info: InfoScreen pygame
           :parameter resolution: resolution of screen, if None gets resolution of your display"""
        self.screen_info = screen_info
        self.max_resolution = screen_info.current_w, screen_info.current_h
        self.resolution = self.max_resolution if resolution is None else resolution
        self.cell_size = int(max(self.resolution[0] / 50, self.resolution[1] / 50) * 3)
        self.screen = pygame.display.set_mode(self.resolution,
                                              flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
                                              vsync=False)
        self.fps_value = 'False'

    def WriteSettings(self, fps_value='False'):
        """:returns File with Settings"""
        self.fps_value = fps_value
        config = configparser.ConfigParser()
        config['Resolution'] = {'resolution': f'{self.resolution[0]}, {self.resolution[1]}'}
        config['Cell_size'] = {'cell_size': str(self.cell_size)}
        config['FPS'] = {'show_fps_counter': f'{fps_value}'}
        config['Game'] = {'started': f'True', 'end': f'False', 'health_lvl': '0', 'strength_lvl':
                          '0', 'speed_lvl': '0', 'regeneration_lvl': '0', 'money': '0',
                          'level': '0', 'all_money': '0', 'killed_creatures': '0'}

        with open('Settings.cfg', 'w') as configfile:
            config.write(configfile)

    def WriteEnd(self, player, fps_value='False'):
        self.fps_value = fps_value
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        config['Game']['started'] = f'False'
        config['Game']['money'] = f'{player.all_money}'
        with open('Settings.cfg', 'w') as configfile:
            config.write(configfile)

    def InitScreen(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        config['FPS'] = {'show_fps_counter': f'{self.fps_value}'}
        return self.screen

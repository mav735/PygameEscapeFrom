import pygame_menu
import pygame
import configparser


class Menu:
    def __init__(self, settings, func):
        self.start_theme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0),  # transparent background
                                                    title_background_color=(47, 47, 47),
                                                    title_font_shadow=True,
                                                    widget_padding=(20, 50),
                                                    widget_font_antialias=True,
                                                    widget_font=pygame_menu.font.FONT_HELVETICA,
                                                    widget_font_color=(255, 255, 255),
                                                    widget_tab_size=210,
                                                    widget_background_inflate_to_selection=True,
                                                    fps=60)

        self.image = pygame.transform.scale(pygame.image.load('picture.png').convert_alpha(),
                                            (settings.resolution[0], settings.resolution[1]))
        pygame.image.save(self.image, 'start_menu.jpg')
        self.settings = settings
        self.menu_image = pygame_menu.baseimage.BaseImage(
            image_path='start_menu.jpg',
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
        )
        self.start_theme.background_color = self.menu_image
        self.go = func
        self.menu = pygame_menu.Menu('Escape from Piter', settings.resolution[0], settings.resolution[1],
                                     theme=self.start_theme)
        self.menu.add.button('Play', self.start)
        self.menu.add.button('Settings', self.settings_mode)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def settings_mode(self):
        pygame_menu.menu.Menu.get_current(self.menu).clear(True)
        self.menu.add.selector('FPS  show:', [('ON', 1), ('OFF', 2)])
        self.menu.add.button('Main  menu', self.back_to_menu)

    def start(self):
        self.go()
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        health = int(config['Game']['health_lvl'])
        strength = int(config['Game']['strength_lvl'])
        speed = int(config['Game']['speed_lvl'])
        regeneration = int(config['Game']['regeneration_lvl'])

        if config['Game']['started'] == 'False':
            pygame_menu.menu.Menu.get_current(self.menu).clear(True)
            self.menu.add.selector('Strength lvl(40 points per lvl):',
                                   [(f'{i}', i) for i in range(strength, 11)])
            self.menu.add.selector('Speed lvl(20 points per lvl):',
                                   [(f'{i}', i) for i in range(speed, 11)])
            self.menu.add.selector('Health lvl(30 points per lvl):',
                                   [(f'{i}', i) for i in range(health, 11)])
            self.menu.add.selector('Regeneration lvl(45 points per lvl):',
                                   [(f'{i}', i) for i in range(regeneration, 11)])

            self.menu.add.button('Main  menu', self.back_to_menu)

    def back_to_menu(self):
        values = []
        for widget in self.menu.get_widgets():
            try:
                values.append(int(widget.get_value()[0][0]))
            except ValueError:
                pass
        '''
        if len(values) > 2:
            config = configparser.ConfigParser()
            config.read('Settings.cfg')
            if sum(values) > int(config['Game']['money']):
                self.menu.add.image('menu.jpg', angle=10, scale=(0.15, 0.15))
        '''
        if self.menu.get_widgets()[0].get_value()[0][0] == 'ON':
            self.settings.WriteSettings('True')
        else:
            self.settings.WriteSettings('False')
        pygame_menu.menu.Menu.get_current(self.menu).clear(True)

        self.menu.add.button('Play', self.start)
        self.menu.add.button('Settings', self.settings_mode)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

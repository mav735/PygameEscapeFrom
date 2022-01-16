import pygame_menu
import pygame
import configparser


class Menu:
    def __init__(self, settings, func):
        self.start_theme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0),
                                                    # transparent background
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
        self.menu = pygame_menu.Menu('Escape from Piter', settings.resolution[0],
                                     settings.resolution[1],
                                     theme=self.start_theme)
        self.menu.add.button('Play', self.start)
        self.menu.add.button('Settings', self.settings_mode)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.coin = None
        self.heath_label = None
        self.regeneration_label = None
        self.strength_label = None
        self.speed_label = None
        self.number_of_coins = None

    def settings_mode(self):
        pygame_menu.menu.Menu.get_current(self.menu).clear(True)
        self.menu.add.selector('FPS  show:', [('ON', 1), ('OFF', 2)])
        self.menu.add.button('Main  menu', self.back_to_menu)

    def start(self):
        self.go()
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        if config['Game']['started'] == 'False':
            self.buy_menu()

    def buy_menu(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        pygame_menu.menu.Menu.get_current(self.menu).clear(True)

        self.coin = self.menu.add.image('Playerimg/coin.png', scale=(0.05, 0.05))
        self.number_of_coins = self.menu.add.label(config['Game']['money'])
        self.menu.add.vertical_margin(50)

        self.strength_label = self.menu.add.label('Strength level = ' +
                                                  config['Game']['strength_lvl'])
        self.speed_label = self.menu.add.label('Speed level = ' +
                                               config['Game']['speed_lvl'])
        self.heath_label = self.menu.add.label('Health level = ' +
                                               config['Game']['health_lvl'])
        self.regeneration_label = self.menu.add.label('Regeneration level = ' +
                                                      config['Game']['regeneration_lvl'])
        self.menu.add.vertical_margin(50)

        self.menu.add.button('Strength lvl(40 points per lvl)', self.buy_strength)
        self.menu.add.button('Speed lvl(20 points per lvl, max 10)', self.buy_speed)
        self.menu.add.button('Health lvl(30 points per lvl)', self.buy_health)
        self.menu.add.button('Regeneration lvl(45 points per lvl)', self.buy_regeneration)

        self.menu.add.button('Main  menu', self.back_to_menu)

    def buy_strength(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        print(0)
        money = int(config['Game']['money'])
        if money >= 40:
            money -= 40
            config['Game']['money'] = str(money)
            config['Game']['strength_lvl'] = str(int(config['Game']['strength_lvl']) + 1)
            with open('Settings.cfg', 'w') as configfile:
                config.write(configfile)
            self.buy_menu()

    def buy_speed(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        money = int(config['Game']['money'])
        if money >= 20 and int(config['Game']['speed_lvl']) < 10:
            money -= 20
            config['Game']['money'] = str(money)
            config['Game']['speed_lvl'] = str(int(config['Game']['speed_lvl']) + 1)
            with open('Settings.cfg', 'w') as configfile:
                config.write(configfile)
            self.buy_menu()

    def buy_health(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        money = int(config['Game']['money'])
        if money >= 30:
            money -= 30
            config['Game']['money'] = str(money)
            config['Game']['health_lvl'] = str(int(config['Game']['health_lvl']) + 1)
            with open('Settings.cfg', 'w') as configfile:
                config.write(configfile)
            self.buy_menu()

    def buy_regeneration(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        money = int(config['Game']['money'])
        if money >= 45:
            money -= 45
            config['Game']['money'] = str(money)
            config['Game']['regeneration_lvl'] = str(int(config['Game']['regeneration_lvl']) + 1)
            with open('Settings.cfg', 'w') as configfile:
                config.write(configfile)
            self.buy_menu()

    def back_to_menu(self):
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        if eval(config['Game']['started']):
            if self.menu.get_widgets()[0].get_value()[0][0] == 'ON':
                self.settings.WriteSettings('True')
            else:
                self.settings.WriteSettings('False')
        pygame_menu.menu.Menu.get_current(self.menu).clear(True)
        self.menu.add.button('Play', self.start)
        self.menu.add.button('Settings', self.settings_mode)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

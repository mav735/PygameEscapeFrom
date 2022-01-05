import pygame
import configparser


class FpsCounter(pygame.sprite.Sprite):
    def __init__(self, screen, clock):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 32)
        config = configparser.ConfigParser()
        config.read('Settings.cfg')
        self.show = config['FPS']['show_fps_counter']
        self.fps_text = self.font.render('', False, "RED")
        self.fps_text_rect = self.fps_text.get_rect(center=(50, 30))
        self.clock = clock

    def render(self):
        self.screen.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        if self.show == 'True':
            fps = self.clock.get_fps()
            text = f"{fps:2.0f} FPS"
            if fps > 30:
                color = "GREEN"
            elif 15 < fps < 30:
                color = "ORANGE"
            else:
                color = "RED"

            self.fps_text = self.font.render(text, False, color)
            self.fps_text_rect = self.fps_text.get_rect(center=(50, 30))
        else:
            pass

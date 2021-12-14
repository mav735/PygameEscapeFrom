import pygame


class Player:
    def __init__(self):
        self.health = 100
        self.mana = 2000
        self.armor = 0
        self.inventory = []
        self.current_object = None

        self.move_anime = False
        self.attack_anime = False
        self.damage_anime = False
        self.dying_anime = False

    def movement(self, event, cam):
        if event.type == pygame.K_w:
            cam.x_move(1)
            self.move_anime = True
        elif event.type == pygame.K_s:
            cam.x_move(-1)
            self.move_anime = True
        elif event.type == pygame.K_a:
            cam.y_move(-1)
            self.move_anime = True
        elif event.type == pygame.K_d:
            cam.y_move(1)
            self.move_anime = True

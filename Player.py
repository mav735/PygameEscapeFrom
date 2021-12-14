import pygame


class Player:
    def __init__(self):
        self.health = 100
        self.mana = 2000
        self.armor = 0
        self.inventory = []
        self.current_object = None
        self.x = 10
        self.y = 10
        self.move_anime = False
        self.attack_anime = False
        self.damage_anime = False
        self.dying_anime = False

    def get_coords(self):
        return self.x, self.y

    def x_move(self, coefficient):
        self.x += 3 * coefficient

    def y_move(self, coefficient):
        self.y += 3 * coefficient

    def movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.y_move(1)
                self.move_anime = True
            if event.key == pygame.K_s:
                self.y_move(-1)
                self.move_anime = True
            if event.key == pygame.K_a:
                self.x_move(1)
                self.move_anime = True
            if event.key == pygame.K_d:
                self.x_move(-1)
                self.move_anime = True

import pygame

import Draw
import Generator
import Player


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('laguha')
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

    """Classes"""
    Map = Generator.MapGenerator(infoObject)
    floor_drawer = Draw.DrawFloor(screen, '1', Map.cell_size)
    player = Player.Player()
    """------------------------------------------------------"""

    running = True
    while running:
        for event in pygame.event.get():
            player.movement(event)

        screen.fill((0, 0, 0))
        floor_drawer.blit_floor(player.get_coords())
        pygame.display.flip()

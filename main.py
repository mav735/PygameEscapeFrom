import pygame

import Draw
import Generator
import Player
import Settings

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('laguha')
    infoObject = pygame.display.Info()

    settings = Settings.Settings(infoObject)
    screen = settings.InitScreen()

    """Classes"""
    Map = Generator.MapGenerator()
    floor_drawer = Draw.DrawFloor(screen, '1', Map.get_map())
    player = Player.Player(Map.start_point)
    """------------------------------------------------------"""

    running = True
    fps = 60
    clock = pygame.time.Clock()
    player_sprite = pygame.sprite.Group()
    player_sprite.add(player)

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            pass

        player.movement()

        screen.fill((0, 0, 0))
        coords = player.get_coords()
        floor_drawer.blit_floor(coords)
        player_sprite.update()
        player_sprite.draw(screen)
        pygame.display.flip()

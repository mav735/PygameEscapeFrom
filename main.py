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
    coefficient_scaling = 3

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                coefficient_scaling = max(event.y * 0.05 + coefficient_scaling, 1)
                cell_size_new = int(max(settings.resolution[0] / 50,
                                        settings.resolution[1] / 50) * coefficient_scaling)

                settings.cell_size = cell_size_new
                settings.WriteSettings()
                screen = settings.InitScreen()

                player.resize_scale(new_cell_size=cell_size_new)
                player_sprite.update()
                player_sprite.draw(screen)

                floor_drawer = Draw.DrawFloor(screen, '1', Map.get_map())

        player.movement()

        screen.fill((47, 47, 47))
        coords = player.get_coords()
        player_sprite.update()

        floor_drawer.blit_floor(coords)
        player_sprite.draw(screen)
        pygame.display.flip()

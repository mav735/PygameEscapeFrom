import pygame

import Draw
import Generator
import Player
import Settings
import Fps

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('laguha')
    infoObject = pygame.display.Info()

    settings = Settings.Settings(infoObject)
    settings.WriteSettings()

    screen = settings.InitScreen()
    clock = pygame.time.Clock()

    """Classes"""
    Map = Generator.MapGenerator()
    floor_drawer = Draw.DrawFloor(screen, '1', Map.get_map())
    player = Player.Player(Map.start_point)
    fps_counter = Fps.FpsCounter(screen, clock)
    """------------------------------------------------------"""

    running = 1
    FPS = 60
    player_sprite = pygame.sprite.Group()
    player_sprite.add(player)
    coefficient_scaling = 3
    all_sprites = pygame.sprite.Group()
    all_sprites.add(fps_counter)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            if event.type == pygame.MOUSEWHEEL:
                if coefficient_scaling != max(event.y * 0.05 + coefficient_scaling, 1) and \
                        max(event.y * 0.05 + coefficient_scaling, 1) < 3.8:
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
        all_sprites.update()
        floor_drawer.blit_floor(coords)
        player_sprite.draw(screen)
        fps_counter.render()
        pygame.display.flip()

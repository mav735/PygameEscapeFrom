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
    k = 3

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                k = max(event.y * 0.3 + k, 1)
                settings.cell_size = int(max(settings.resolution[0] / 50,
                                             settings.resolution[1] / 50) * k)
                settings.WriteSettings()

                x = (player.screen_resolution[0] / 2 - player.x - 0.5 * player.cell_size) / player.cell_size
                y = (player.screen_resolution[1] / 2 - player.y - 0.5 * player.cell_size) / player.cell_size
                player = Player.Player((x, y))

                player_sprite = pygame.sprite.Group()
                player_sprite.add(player)

                screen = settings.InitScreen()
                floor_drawer = Draw.DrawFloor(screen, '1', Map.get_map())


        player.movement()

        screen.fill((47, 47, 47))
        coords = player.get_coords()
        floor_drawer.blit_floor(coords)
        player_sprite.update()
        player_sprite.draw(screen)
        pygame.display.flip()

import pygame
import Menu
import Draw
import Generator
import Player
import Settings
import Fps
import Enemy
import configparser


def start_the_game():
    surface = settings.InitScreen()
    clock = pygame.time.Clock()

    """Classes"""
    Map = Generator.MapGenerator()
    floor_drawer = Draw.DrawFloor(surface, '1', Map.get_map())
    player = Player.Player((23, 4), Map.get_monolith())

    enemy = Enemy.EnemyTroll((3, 3), (player.x, player.y), player)
    enemy_2 = Enemy.EnemyTroll((2, 2), (player.x, player.y), player)
    enemy_3 = Enemy.EnemyTroll((1, 1), (player.x, player.y), player)

    fps_counter = Fps.FpsCounter(surface, clock)
    hp_mana_bar = Draw.InfoPlayer(player)
    """------------------------------------------------------"""

    running = 1
    FPS = 60
    player_sprite = pygame.sprite.Group()
    player_sprite.add(player)
    enemy_sprite = pygame.sprite.Group()
    enemy_sprite.add(enemy)
    enemy_sprite.add(enemy_2)
    enemy_sprite.add(enemy_3)
    coefficient_scaling = 3
    all_sprites = pygame.sprite.Group()
    all_sprites.add(fps_counter)
    sys_exit = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                sys_exit = True
            if event.type == pygame.MOUSEWHEEL:
                '''
                if coefficient_scaling != max(event.y * 0.05 + coefficient_scaling, 1) and \
                        max(event.y * 0.05 + coefficient_scaling, 1) < 3.8:
                    coefficient_scaling = max(event.y * 0.05 + coefficient_scaling, 1)
                    cell_size_new = int(max(game_settings.resolution[0] / 50,
                                            game_settings.resolution[1] / 50) * coefficient_scaling)

                    game_settings.cell_size = cell_size_new
                    game_settings.WriteSettings()
                    surface = game_settings.InitScreen()
                    old_coords = player.get_coords()
                    player.resize_scale(new_cell_size=cell_size_new)
                    enemy.resize_scale(new_cell_size=cell_size_new, player_pos=old_coords)
                    player_sprite.update()
                    player_sprite.draw(surface)
                    enemy_sprite.update((player.x, player.y))
                    enemy_sprite.draw(surface)

                    floor_drawer = Draw.DrawFloor(surface, '1', Map.get_map())
                '''
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.attack()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                player.health += 1000

        player.movement(Map.get_map())

        for sprite in enemy_sprite.sprites():
            sprite.movement(Map.get_map())
            if player.anime['attack'][0]:
                if sprite.attack():
                    sprite.health -= player.damage

            if sprite.attack():
                player.health -= sprite.damage

        surface.fill((47, 47, 47))
        coords = player.get_coords()
        player.update()

        end = player.end()
        if end:
            running = 0
        enemy_sprite.update((player.x, player.y))

        all_sprites.update()
        floor_drawer.blit_floor(coords)

        player_sprite.draw(surface)
        enemy_sprite.draw(surface)
        hp_mana_bar.draw(surface)
        fps_counter.render()
        pygame.display.flip()

    if not sys_exit:
        settings.WriteEnd(player)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('laguha')
    infoObject = pygame.display.Info()
    settings = Settings.Settings(infoObject)
    settings.WriteSettings()
    screen = settings.InitScreen()
    menu = Menu.Menu(settings, start_the_game)
    menu.menu.mainloop(screen)
    config = configparser.ConfigParser()
    config.read('Settings.cfg')

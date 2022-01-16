import random
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
    player = Player.Player(Map.start_point, Map.get_monolith())

    cfg = configparser.ConfigParser()
    cfg.read('Settings.cfg')
    cfg['Game']['level'] = str(int(cfg['Game']['level']) + 1)
    with open('Settings.cfg', 'w') as configfile:
        cfg.write(configfile)
    print(f"LEVEl {cfg['Game']['level']}\nPlayer = {Map.start_point}", f'Monolith = {Map.monolith}',
          f'money = {player.all_money}', f'hp = {player.health}', '', sep='\n')
    used_points = [Map.start_point, Map.monolith]
    enemy = []
    for i in range(20):
        while True:
            point = [random.randint(0, 49), random.randint(0, 49)]
            if point not in used_points and Map.get_map()[point[0]][point[1]] == '1':
                used_points.append(point)
                enemy.append(random.choices([
                    Enemy.EnemyTroll(point, (player.x, player.y), player),
                    Enemy.EnemyBeast(point, (player.x, player.y), player)]))
                break

    fps_counter = Fps.FpsCounter(surface, clock)
    hp_mana_bar = Draw.InfoPlayer(player)
    """------------------------------------------------------"""

    running = 1
    FPS = 60
    player_sprite = pygame.sprite.Group()
    player_sprite.add(player)
    enemy_sprite = pygame.sprite.Group()
    for entity in enemy:
        enemy_sprite.add(entity)
    coefficient_scaling = 3
    cfg = configparser.ConfigParser()
    cfg.read('Settings.cfg')
    all_sprites = pygame.sprite.Group()
    all_sprites.add(fps_counter)
    sys_exit = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
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

            if pygame.key.get_pressed()[pygame.K_h]:
                player.health += 100

            if pygame.key.get_pressed()[pygame.K_m]:
                player.all_money += 25

        player.movement(Map.get_map())

        for sprite in enemy_sprite.sprites():
            sprite.movement(Map.get_map())
            if player.anime['attack'][0]:
                if sprite.attack():
                    sprite.health -= player.damage

            if sprite.attack():
                player.health -= sprite.damage

            if sprite.health <= 0 and sprite.coins_earned:
                player.all_money += sprite.cost

                cfg['Game']['all_money'] = str(int(cfg['Game']['all_money']) + sprite.cost)
                cfg['Game']['killed_creatures'] = str(int(cfg['Game']['killed_creatures']) + 1)

                with open('Settings.cfg', 'w') as configfile:
                    cfg.write(configfile)

                sprite.coins_earned = False

        surface.fill((47, 47, 47))
        coords = player.get_coords()
        player.update()

        if player.end() or player.death():
            running = 0
        enemy_sprite.update((player.x, player.y))

        all_sprites.update()
        floor_drawer.blit_floor(coords)
        floor_drawer.blit_coins(player.all_money)

        player_sprite.draw(surface)
        enemy_sprite.draw(surface)
        hp_mana_bar.draw(surface)
        fps_counter.render()
        pygame.display.flip()

    if not sys_exit and running == 0:
        settings.WriteEnd(player)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('laguha')
    infoObject = pygame.display.Info()
    settings = Settings.Settings(infoObject)
    settings.WriteSettings()
    screen = settings.InitScreen()
    menu = Menu.Menu(settings, start_the_game, screen)
    menu.menu.mainloop(screen)
    config = configparser.ConfigParser()
    config.read('Settings.cfg')

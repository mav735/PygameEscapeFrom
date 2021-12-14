import Draw
import Generator
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('laguha')
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
    Map = Generator.MapGenerator(infoObject)
    floor_drawer = Draw.DrawFloor(screen, '1', Map.cell_size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Map.left += 10

        screen.fill((0, 0, 0))
        floor_drawer.blit_floor(Map.get_coords())
        pygame.display.flip()

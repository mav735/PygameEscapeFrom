import pygame_widgets
import pygame
import time
from pygame_widgets.progressbar import ProgressBar

startTime = time.time()

pygame.init()
win = pygame.display.set_mode((1000, 600))

progressBar = ProgressBar(win, 100, 100, 100, 40, lambda: 1 - (time.time() - startTime) / 10, curved=True,
                          incompletedColour="WHITE", completedColour="RED")

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    pygame_widgets.update(events)
    pygame.display.update()
import pygame
from pygame.draw import *
pygame.init()

FPS = 3
screen = pygame.display.set_mode((1300, 700))
screen.fill((80, 80, 80))

bl = (0, 0, 0)
rd = (250, 0, 0)
yel = (250, 250, 0)

circle(screen, yel, (650, 350), 200)
circle(screen, bl, (650, 350), 200, 2)

circle(screen, rd, (550, 270), 50)
circle(screen, bl, (550, 270), 50, 2)

circle(screen, rd, (730, 260), 40)
circle(screen, bl, (730, 260), 40, 2)

circle(screen, bl, (550, 270), 20)
circle(screen, bl, (730, 260), 20)

rect(screen, bl, (550, 450, 210, 30))
def recang(x, y, a, b, k):
    return(polygon(screen, (0, 0, 0), [(x, y), (x+b*k, y-a*k),
                                  (x+b*k+a, y-a*k+b), (x+a, y+b), (x, y)]))
recang(450, 150, -25, 60, 3)
recang(850, 200, -20, -45, 4)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
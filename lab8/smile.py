import pygame
from pygame.draw import *
pygame.init()

FPS = 3
screen = pygame.display.set_mode((1300, 700))
screen.fill((80, 80, 80))

circle(screen, (250, 250, 0), (650, 350), 200)
circle(screen, (0, 0, 0), (650, 350), 200, 2)
circle(screen, (250, 0, 0), (550, 270), 50)
circle(screen, (0, 0, 0), (550, 270), 50, 2)
circle(screen, (250, 0, 0), (730, 260), 40)
circle(screen, (0, 0, 0), (730, 260), 40, 2)
circle(screen, (0, 0, 0), (550, 270), 20)
circle(screen, (0, 0, 0), (730, 260), 20)

rect(screen, (0, 0, 0), (550, 450, 210, 30))

def recang(x, y, a, b, k):
    return(polygon(screen, (0, 0, 0), [(x, y), (x+a*k, y-a*k),
                                  (x+a*k-b*k, y-a*k+b*k), (x-b*k, y+b*k), (x, y)]))
print(recang(250, 350, 100, 200, 3))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
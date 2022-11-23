import pygame
from pygame.draw import *
from random import randint

pygame.init()

screen = pygame.display.set_mode((1300, 700))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():
    '''рисует новый шарик '''
    global x, y, r
    x = randint(100, 1200)
    y = randint(100, 600)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def click(event):
    print(x, y, r)

def catch_check(event):
    global x, y, r
    if (event.pos[0]-x)**2 + (event.pos[1]-y)**2 <= r**2:
        return True
    else:
        return False

clock = pygame.time.Clock()
finished = False
score = 0

while not finished:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if catch_check(event):
                score += 1
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

print("Ваш счёт: ", score)

pygame.quit()
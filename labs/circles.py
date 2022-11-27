import pygame
from pygame.draw import *
from random import randint

pygame.init()

A = 1300
B = 700
Rmin = 10
Rmax = 100
screen = pygame.display.set_mode((A, B))
FPS = 150
n = 3

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def draw_circles():
    '''рисует новые n кружков '''
    global x, y, r, color, vx, vy
    x = []
    y = []
    r = []
    vx = []
    vy = []
    color = []
    for i in range(n):
        x += [randint(Rmax, A-Rmax)]
        y += [randint(Rmax, B-Rmax)]
        r += [randint(Rmin, Rmax)]
        vx += [randint(1, 5)*(2*randint(0, 1)-1)]
        vy += [randint(1, 5)*(2*randint(0, 1)-1)]
        color += [COLORS[randint(0, 5)]]
        circle(screen, color[i], (x[i], y[i]), r[i])

def catch_check(event):
    '''проверяет, попал ли игрок в кружок'''
    global x, y, r
    for i in range(n):
        if (event.pos[0]-x[i])**2 + (event.pos[1]-y[i])**2 <= r[i]**2:
            return True
    return False

def move_circles():
    for i in range(n):
        x[i] += vx[i]
        y[i] += vy[i]

def hit_check():
    for i in range(n):
        if min(A-x[i], x[i]) <= r[i]:
            vx[i] = -vx[i]
        if min(B-y[i], y[i]) <= r[i]:
            vy[i] = -vy[i]

def new_circles():
    for i in range(n):
        circle(screen, color[i], (x[i], y[i]), r[i])

score = 0
shrift = pygame.font.SysFont('Times New Roman', 30)
text_color = CYAN
clock = pygame.time.Clock()
finished = False

draw_circles()
while not finished:
    clock.tick(FPS)
    move_circles()
    hit_check()
    new_circles()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if catch_check(event):
                score += 1
    text = shrift.render("Ваш счёт: " + str(score), 1, text_color)
    screen.blit(text, (3, 3))
    pygame.display.update()
    screen.fill(BLACK)

print("Ваш счёт: ", score)

pygame.quit()
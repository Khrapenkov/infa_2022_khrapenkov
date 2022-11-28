import pygame
from pygame.draw import *
from random import randint

pygame.init()

WIDTH = 1300
HIGHT = 700
Rmin = 30
Rmax = 60
Vmin = 7
Vmax = 10
screen = pygame.display.set_mode((WIDTH, HIGHT))
FPS = 80
n = 5

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def create_circles():
    '''создаёт и рисует произвольные n кружков '''
    global x, y, r, color, vx, vy
    x = []
    y = []
    r = []
    vx = []
    vy = []
    color = []
    for i in range(n):
        x += [randint(Rmax, WIDTH-Rmax)]
        y += [randint(Rmax, HIGHT-Rmax)]
        r += [randint(Rmin, Rmax)]
        vx += [randint(Vmin, Vmax)*(2*randint(0, 1)-1)]
        vy += [randint(Vmin, Vmax)*(2*randint(0, 1)-1)]
        color += [COLORS[randint(0, 5)]]
        circle(screen, color[i], (x[i], y[i]), r[i])

def catch_check(event):
    '''проверяет, попал ли игрок в кружок, и удаляет данные о кружке, в который попали'''
    global x, y, r
    for i in range(n):
        if (event.pos[0]-x[i])**2 + (event.pos[1]-y[i])**2 <= r[i]**2:
            x.remove(x[i])
            y.remove(y[i])
            r.remove(r[i])
            vx.remove(vx[i])
            vy.remove(vy[i])
            color.remove(color[i])
            return True
    return False

def new_circle():
    '''создаёт и рисует новый кружок: заносит данные о нём в список кружков; т.е. вместе с
    функцией "catch_check(event)" заменяет пойманный кружок на новый'''
    global x, y, r, color, vx, vy
    x += [randint(Rmax, WIDTH - Rmax)]
    y += [randint(Rmax, HIGHT - Rmax)]
    r += [randint(Rmin, Rmax)]
    vx += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
    vy += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
    color += [COLORS[randint(0, 5)]]
    circle(screen, color[n-1], (x[n-1], y[n-1]), r[n-1])

def move_circles():
    '''создаёт новые координаты центров кружков'''
    for i in range(n):
        x[i] += vx[i]
        y[i] += vy[i]

def wall_check():
    '''проверяет необходимость отскока и отражает скорости кружков если нужно'''
    for i in range(n):
        if min(WIDTH-x[i], x[i]) <= r[i]:
            vx[i] = -vx[i]
        if min(HIGHT-y[i], y[i]) <= r[i]:
            vy[i] = -vy[i]

def draw_circles():
    '''в отличие от функции "create_circules()" рисует уже заданные и перемещённые
    функцией "move_circles()" кружки'''
    for i in range(n):
        circle(screen, color[i], (x[i], y[i]), r[i])

score = 0
shrift = pygame.font.SysFont('Times New Roman', 30)
text_color = RED
clock = pygame.time.Clock()
finished = False

create_circles()
while not finished:
    clock.tick(FPS)
    move_circles()
    wall_check()
    draw_circles()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if catch_check(event):
                new_circle()
                score += 1
    text = shrift.render("Ваш счёт: " + str(score), True, text_color)
    screen.blit(text, (1, 1))
    pygame.display.update()
    screen.fill(BLACK)

print("Ваш счёт: ", score)

pygame.quit()
import pygame
from pygame.draw import *
from random import randint

WIDTH = 1300
HEIGHT = 700
Rmin = 30
Rmax = 60
Vmin = 7
Vmax = 10
FPS = 80
n = 5  # количество кружков на экране

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Circles:
    def __init__(self, screen):
        self.screen = screen
        self.x = []
        self.y = []
        self.r = []
        self.vx = []
        self.vy = []
        self.color = []

    def create(self):
        """Создаёт и рисует произвольные n кружков """

        for i in range(n):
            self.x += [randint(Rmax, WIDTH - Rmax)]
            self.y += [randint(Rmax, HEIGHT - Rmax)]
            self.r += [randint(Rmin, Rmax)]
            self.vx += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
            self.vy += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
            self.color += [COLORS[randint(0, 5)]]
            circle(self.screen, self.color[i], (self.x[i], self.y[i]), self.r[i])

    def catch_check(self, event):
        """Проверяет, попал ли игрок в кружок, и удаляет данные о кружке, в который попали"""
        for i in range(n):
            if (event.pos[0] - self.x[i]) ** 2 + (event.pos[1] - self.y[i]) ** 2 <= self.r[i] ** 2:
                self.x.remove(self.x[i])
                self.y.remove(self.y[i])
                self.r.remove(self.r[i])
                self.vx.remove(self.vx[i])
                self.vy.remove(self.vy[i])
                self.color.remove(self.color[i])
                return True
        return False

    def new(self):
        """Создаёт и рисует новый кружок: заносит данные о нём в список кружков; т.е. вместе с
        функцией "catch_check(event)" заменяет пойманный кружок на новый"""
        self.x += [randint(Rmax, WIDTH - Rmax)]
        self.y += [randint(Rmax, HEIGHT - Rmax)]
        self.r += [randint(Rmin, Rmax)]
        self.vx += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
        self.vy += [randint(Vmin, Vmax) * (2 * randint(0, 1) - 1)]
        self.color += [COLORS[randint(0, 5)]]
        circle(self.screen, self.color[n - 1], (self.x[n - 1], self.y[n - 1]), self.r[n - 1])

    def move(self):
        """Создаёт новые координаты центров кружков"""
        for i in range(n):
            self.x[i] += self.vx[i]
            self.y[i] += self.vy[i]

    def wall_check(self):
        """Проверяет необходимость отскока и отражает скорости кружков если нужно"""
        for i in range(n):
            if min(WIDTH - self.x[i], self.x[i]) <= self.r[i]:
                self.vx[i] = -self.vx[i]
            if min(HEIGHT - self.y[i], self.y[i]) <= self.r[i]:
                self.vy[i] = -self.vy[i]

    def draw(self):
        """В отличие от функции "create_circles()" рисует уже заданные и перемещённые
        функцией "move_circles()" кружки"""
        for i in range(n):
            circle(self.screen, self.color[i], (self.x[i], self.y[i]), self.r[i])


def main():
    pygame.init()
    score = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    shrift = pygame.font.SysFont('Times New Roman', 30)
    text_color = (255, 255, 255)
    clock = pygame.time.Clock()
    circles = Circles(screen)
    circles.create()
    finished = False

    while not finished:
        clock.tick(FPS)
        circles.wall_check()
        circles.move()
        circles.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if circles.catch_check(event):
                    circles.new()
                    score += 1
        text = shrift.render("Ваш счёт: " + str(score), True, text_color)
        screen.blit(text, (1, 1))
        pygame.display.update()
        screen.fill(BLACK)

    print("Ваш счёт: ", score)

    pygame.quit()


if __name__ == '__main__':
    main()

import math
from random import randint
from pygame.draw import *

import pygame

FPS = 50

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
GUN_WIDTH = 30  # ширина пушки
GUN_LENGTH = 100  # длина пушки
GUN_RADIUS = 20  # радиус колёс пушки
X, Y = 50, 550  # начальное положение пушки и мяча


class Ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = X
        self.y = Y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[randint(0, 5)]
        self.live = 700

    def move(self):
        """Перемещает мяч по прошествии единицы времени."""
        self.x += self.vx
        self.y -= self.vy
        self.vx -= self.vx * 0.02  # сопротивление воздуха
        self.vy -= self.vy * 0.02 + 20 / FPS  # сопротивление воздуха и гравитация
        if abs(self.vx) <= 0.05:
            self.vx = 0
        if abs(self.vy) <= 0.05:
            self.vy = 0
        if (self.vx > 0 and WIDTH - self.x <= self.r) or (self.vx < 0 and self.x <= self.r):
            self.vx = -self.vx * 0.95
        if HEIGHT - self.y <= self.r:
            self.vy = -self.vy * 0.95

    def draw(self):
        if self.live > 0:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
            self.live -= 1

    def hit_test(self, obj):
        return obj.hittest(self)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.x = X
        self.y = Y
        self.length = GUN_LENGTH
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1  # angle
        self.color = GREY
        self.bullet = 0
        self.balls = []
        self.length = GUN_LENGTH

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += randint(2, 8)
        self.an = math.atan2((new_ball.y - event.pos[1]), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        self.balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.length = GUN_LENGTH

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - self.x != 0:
                self.an = math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        w = GUN_WIDTH
        a = self.length
        x = self.x
        y = self.y
        sina = math.sin(self.an)
        cosa = math.cos(self.an)
        polygon(self.screen, self.color, [(x + w / 2 * sina, y + w / 2 * cosa),
                                          (x + w / 2 * sina + a * cosa, y + w / 2 * cosa - a * sina),
                                          (x - w / 2 * sina + a * cosa, y - w / 2 * cosa - a * sina),
                                          (x - w / 2 * sina, y - w / 2 * cosa),
                                          (x + w / 2 * sina, y + w / 2 * cosa)])
        circle(self.screen, BLACK, (x, y), GUN_RADIUS)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.length += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.x = None
        self.y = None
        self.r = None
        self.color = None
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 750)
        self.y = randint(300, 551)
        self.r = randint(2, 50)
        self.color = GAME_COLORS[randint(0, 5)]

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, ball):
        if (ball.x - self.x) ** 2 + (ball.y - self.y) ** 2 <= (ball.r + self.r) ** 2:
            return True
        return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    gun = Gun(screen)
    balls = gun.balls
    clock = pygame.time.Clock()
    target = Target(screen)
    shrift = pygame.font.SysFont('Times New Roman', 25)
    text_color = BLACK
    finished = False

    while not finished:
        gun.draw()
        target.draw()
        for b in balls:
            b.draw()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        for b in balls:
            if b.hit_test(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
            b.move()
        gun.power_up()
        text1 = shrift.render("Удачных попаданий: " + str(target.points) +
                              "  Использовано снарядов: " + str(gun.bullet), True, text_color)
        screen.blit(text1, (1, 1))
        pygame.display.update()
        screen.fill(WHITE)

    pygame.quit()


if __name__ == '__main__':
    main()

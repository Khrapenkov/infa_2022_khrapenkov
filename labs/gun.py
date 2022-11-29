import math
from random import choice
from pygame.draw import *

import pygame


FPS = 30

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
GUN_WIDTH = 30 #ширина пушки
GUN_LENGTH = 100 #длина пушки
GUN_RADIUS = 20 #радиус колёс пушки
X, Y = 50, 550 #начальное положение пушки и мяча
class Ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = X
        self.y = Y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        '''Перемещает мяч по прошествии единицы времени.'''
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 10 // FPS
        if WIDTH - self.x <= self.r:
            self.vx = -self.vx
        if HEIGHT - self.y <= self.r:
            self.vy = -self.vy

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME

        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.x = X
        self.y = Y
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1 #angle
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((new_ball.y-event.pos[1]), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((self.y-event.pos[1]) / (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        a = GUN_WIDTH
        b = GUN_LENGTH
        x = self.x
        y = self.y
        sina = math.sin(self.an)
        cosa = math.cos(self.an)
        polygon(screen, self.color, [(x + a/2*sina, y + a/2*cosa),
                                (x + a/2*sina + b*cosa, y + a/2*cosa - b*sina),
                                (x - a/2*sina + b*cosa, y - a/2*cosa - b*sina),
                                (x - a/2*sina, y - a/2*cosa),
                                (x + a/2*sina, y + a/2*cosa)])
        circle(screen, BLACK, (x, y), GUN_RADIUS)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = choice(list(range(600, 781)))
        y = self.y = choice(list(range(300, 551)))
        r = self.r = choice(list(range(2, 50))) #[range()]?
        color = self.color = choice(GAME_COLORS)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
shrift = pygame.font.SysFont('Times New Roman', 30)
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
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()
    text = shrift.render("Ваш счёт: " + str(bullet), True, text_color)
    screen.blit(text, (1, 1))
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()
import random
import time

from pygame import Vector2
import pygame
from pygame.locals import *


pygame.init()

win = pygame.display.set_mode((1000, 1020))
pygame.display.set_caption("Balloon Shooter")

bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill((0, 0, 0))

colors = [(255, 0, 0), (20, 123, 200), (84, 255, 159), (132, 112, 255), (255, 215, 0), (255, 140, 0), (240, 255, 240)]


def wrap_position(position, screen):
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)  # this will let the balloon re-appear on the opposite side of its direction.

def display_win():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('Congratulations!', 1, (255, 255, 255))
    text2 = font.render('You are a good player!', 1, (255, 255, 255))
    win.blit(text, (win.get_width() // 2 - (text.get_width() // 2), (win.get_height() // 2 - (text.get_height() // 2))))
    win.blit(text2, (win.get_width() // 2 - (text.get_width() // 2), (win.get_height() // 2 - (text.get_height() // 2)+60)))

def display_lose():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('You Lose!', 1, (255, 255, 255))
    win.blit(text, (win.get_width() // 2 - (text.get_width() // 2), (win.get_height() // 2 - (text.get_height() // 2))))

def display_author():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Created by Potoro Pao', 1, (255, 255, 255))
    win.blit(text, (win.get_width()-text.get_width(),610))

def display_countdown(timing):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render(f'Count DOWN: {timing}', 1, (255, 255, 255))
    win.blit(text, (0,0))

class Crosshair:
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)

    def movement(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            self.velocity = Vector2(-5, 0)
            self.position += self.velocity
        if pressed[K_RIGHT]:
            self.velocity = Vector2(5, 0)
            self.position += self.velocity
        if pressed[K_UP]:
            self.velocity = Vector2(0, -5)
            self.position += self.velocity
        if pressed[K_DOWN]:
            self.velocity = Vector2(0, 5)
            self.position += self.velocity

    def update(self):
        pygame.draw.rect(win, (0, 180, 0), (self.position[0], self.position[1], 10, 50))
        pygame.draw.rect(win, (0, 180, 0), (self.position[0] - 20, self.position[1] + 20, 50, 10))



class Balloon:
    def __init__(self, position, colors):
        self.position = Vector2(position)
        self.velocity = Vector2(0, -1)
        self.color = random.choice(colors)
        self.radius = 50

    def movement(self):
        self.position += self.velocity

    def update(self):
        self.position = wrap_position(self.position, win)
        pygame.draw.circle(win, self.color, self.position, self.radius)
    def explode(self,cpos):
        pressed = pygame.key.get_pressed()
        if pressed[K_z]:
            if self.position.distance_to(cpos) <= self.radius:
                try:
                    balloon_list.remove(b)
                except:
                    pass


game_over = False

balloon_list = []
for i in range(10):
    balloon_list.append(Balloon((random.randint(35, win.get_width() - 35),
                                 random.randint(0, win.get_height()))
                                , colors))
cross = Crosshair((win.get_width() // 2, win.get_height() // 2))
clock = pygame.time.Clock()

timing=1000
countdown=1

while not game_over:
    timing-=countdown
    dt = clock.tick(60)

    win.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    for b in balloon_list:
        b.movement()
        b.explode(cross.position)
        b.update()

    cross.movement()
    cross.update()
    if len(balloon_list) == 0:
        countdown=0
        display_win()
        display_author()
    display_countdown(timing)
    if timing==0:
        display_lose()
        time.sleep(1)
        game_over=True

    pygame.display.update()
pygame.quit()

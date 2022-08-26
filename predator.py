import pygame
import sys
from random import randint as ri
sys.path.append("..")
from pygame_projects.vector import Vector

class Predator:
    def __init__(self, x, y, r):
        self.pos = Vector(x, y)
        self.speed = 6
        self.r = r
        self.score = 0

    def move(self, keys_pressed):
        v = Vector(0, 0)
        pressed = False
        if keys_pressed[pygame.K_w]:
            v.add(Vector(0, -1))
            pressed = True
        if keys_pressed[pygame.K_s]:
            v.add(Vector(0, 1))
            pressed = True
        if keys_pressed[pygame.K_a]:
            v.add(Vector(-1, 0))
            pressed = True
        if keys_pressed[pygame.K_d]:
            v.add(Vector(1, 0))
            pressed = True

        if pressed:
            v.setMag(self.speed)
        self.update(v)

    def edges(self, width, height):
        if self.pos.x + self.r > width:
            self.pos.x = width - self.r - 1
        if self.pos.x - self.r < 0:
            self.pos.x = self.r + 1
        if self.pos.y + self.r > height:
            self.pos.y = height - self.r - 1
        if self.pos.y - self.r < 0:
            self.pos.y = self.r + 1

    def update(self, vel):
        self.pos.add(vel)

    def show(self, win):
        pygame.draw.circle(win, (190, 3, 252), (self.pos.x, self.pos.y), self.r)
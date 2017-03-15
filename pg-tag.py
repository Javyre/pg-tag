import pygame
import random
import sys
import time
from pygame.locals import *
from Vec2 import *

SW = 500
SH = 500

pygame.init()

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("zach is sitting next to me right now")

class Player:
    def __init__(self, x, y, w, h, speed=500, color=(255,0,0), controls=(K_UP, K_DOWN, K_RIGHT, K_LEFT)):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.ku, self.kd, self.kr, self.kl = controls
        self.directions = {"up": (0, -self.speed), "down": (0, self.speed), "left": (-self.speed, 0), "right": (self.speed, 0)}
        self.displacement = Vec2d(0,0)
    def move(self, direction, dtime):
        self.displacement += direction*dtime
        self.rect = self.rect.move(int(self.displacement.x), int(self.displacement.y))
        self.displacement -= (int(self.displacement.x), int(self.displacement.y))
    def control(self, dtime):
        keys = pygame.key.get_pressed()
        direction = Vec2d(0,0)
        if keys[self.ku]:
            direction += self.directions["up"]
        if keys[self.kd]:
            direction += self.directions["down"]
        if keys[self.kl]:
            direction += self.directions["left"]
        if keys[self.kr]:
            direction += self.directions["right"]
        self.move(direction, dtime)
    def update(self, screen, dtime):
        self.control(dtime)
        pygame.draw.rect(screen, self.color, self.rect)



class game (object):
    def run(self):
        p1 = Player(50, 50, 50, 100, controls=(K_w, K_s, K_d, K_a))
        p2 = Player(50, 50, 100, 50, color=(0, 0, 255))
        players = [p1, p2]
        running = True
        dtime = 0
        stime = 0
        while running:
            stime = time.time()
            keys = pygame.key.get_pressed()
            screen.fill((0,0,0))

            p1.move(Vec2d(300,200), dtime)
            for player in players:
                player.update(screen, dtime)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            dtime = time.time()-stime
        # pygame.time.delay(20)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game().run()
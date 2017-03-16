#! /usr/bin/env python3
import pygame as pg
import sys
import random
from Vec2 import Vec2d

SCREEN_DIMENSIONS = (500, 500)


class GameObject(object):
    def __init__(self, game, x, y, w, h, *args, **kwargs):
        self.g = game
        self.color = kwargs.pop('color', (0, 0, 255))
        self.velocity = Vec2d(0, 0)
        self.displacement = Vec2d(0, 0)
        self.rect = pg.Rect(x, y, w, h)
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def move(self, direction):
        self.displacement += direction*self.g.dtime
        self.rect = self.rect.move(int(self.displacement.x),
                                   int(self.displacement.y))
        self.displacement -= (int(self.displacement.x),
                              int(self.displacement.y))

    def update(self):
        self.velocity *= 0.5
        self.move(self.velocity)
        pg.draw.rect(self.g.screen, self.color, self.rect)


class Player(GameObject):
    def init(self, speed=500, color=(255, 0, 0),
             controls=(pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_LEFT)):
        self.exploding = False
        self.speed = speed
        self.ku, self.kd, self.kr, self.kl = controls
        self.directions = {"up":    (0, -self.speed),
                           "down":  (0, self.speed),
                           "left":  (-self.speed, 0),
                           "right": (self.speed, 0)}

    def control(self):
        keys = pg.key.get_pressed()
        direction = Vec2d(0, 0)
        if keys[self.ku]:
            direction += self.directions["up"]
        if keys[self.kd]:
            direction += self.directions["down"]
        if keys[self.kl]:
            direction += self.directions["left"]
        if keys[self.kr]:
            direction += self.directions["right"]
        if direction != (0, 0):
            self.velocity = Vec2d(0, 0)
        self.velocity += direction

    def update(self):
        if not self.exploding:
            self.velocity.y += self.velocity.y * 1.2 * self.g.dtime \
                             * (-1 if self.velocity.y > 0 else -1)
            self.velocity.x += self.velocity.x * 1.2 * self.g.dtime \
                             * (-1 if self.velocity.x > 0 else -1)
        else:
            self.velocity *= self.g.dtime * 200
            if self.velocity.x > 500 or self.velocity.x < -500:
                self.exploding = False
            if self.velocity.y > 500 or self.velocity.y < -500:
                self.exploding = False
        self.control()
        self.move(self.velocity)

        screen_rect = self.g.screen.get_rect()
        if self.rect.right < screen_rect.left:
            self.rect.left = screen_rect.right
        if self.rect.left > screen_rect.right:
            self.rect.right = screen_rect.left
        if self.rect.bottom < screen_rect.top:
            self.rect.top = screen_rect.bottom
        if self.rect.top > screen_rect.bottom:
            self.rect.bottom = screen_rect.top

        others = [p for p in self.g.players if not (p is self)]
        for i in self.rect.collidelistall([o.rect for o in others]):
            other = others[i].rect
            intersect = self.rect.clip(other)
            if intersect.w < intersect.h:
                if other.centerx > self.rect.centerx:
                    self.rect.x -= intersect.w
                    self.velocity = Vec2d(-400,
                                          7*(self.rect.centery-other.centery))
                    others[i].velocity = \
                        Vec2d(400, 7*(other.centery-self.rect.centery))
                    self.exploding = others[i].exploding = True
            elif intersect.w > intersect.h:
                if other.centery > self.rect.centery:
                    self.rect.y -= intersect.h
                    self.velocity = Vec2d(7*(self.rect.centerx-other.centerx),
                                          -400)
                    others[i].velocity = \
                        Vec2d(7*(other.centerx-self.rect.centerx), 400)
                    self.exploding = others[i].exploding = True

        pg.draw.rect(self.g.screen, self.color, self.rect)


class game(object):
    players = []
    dtime = 0
    running = False

    def insert_player(self, p):
        self.players.append(p)
        return p

    def init(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_DIMENSIONS, pg.RESIZABLE)
        pg.display.set_caption("Tag!")

        self.main_font = pg.font.SysFont('arial', 24)
        self.clock = pg.time.Clock()

        self.p1 = self.insert_player(
            Player(self, 50, 100, 50, 50,
                   controls=(pg.K_w, pg.K_s, pg.K_d, pg.K_a),
                   color=(86, 98, 70)))
        self.p2 = self.insert_player(
            Player(self, 100, 50, 50, 50,
                   color=(164, 194, 165)))

    def update(self):
        # self.p1.move(Vec2d(300, 200))
        for p in self.players:
            p.update()

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.VIDEORESIZE:
                self.screen = pg.display.set_mode((e.w, e.h),
                                                  pg.RESIZABLE)

    def game_loop(self):
        self.running = True
        ftime = 0
        fps = ''

        while self.running:
            self.screen.fill((241, 242, 235))

            self.update()
            self.handle_events()

            # display fps
            # report fps 3 times per second
            if ftime >= 1/3:
                fps = str(int(self.clock.get_fps()))
                ftime = 0
            fps_t = self.main_font.render(fps, True, (128, 129, 129))
            self.screen.blit(fps_t, (self.screen.get_width()
                                     - fps_t.get_width(),
                                     self.screen.get_height()
                                     - fps_t.get_height()))
            # fps displayed

            pg.display.flip()

            self.dtime = float(self.clock.tick(self.max_fps)/1000)
            ftime += self.dtime

    def run(self, fps=0):
        self.max_fps = fps
        self.init()
        self.game_loop()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game().run(fps=int(sys.argv[1]) if len(sys.argv) > 1 else 0)

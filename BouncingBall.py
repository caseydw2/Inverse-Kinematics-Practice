import pygame as pg
import numpy as np

WIDTH = 1600
HEIGHT = 1000
size = (WIDTH, HEIGHT)
screen = pg.display.set_mode(size)
clock = pg.time.Clock()


class Ball:
    def __init__(self, xPos, ypos, iv, radius, color) -> None:
        self.xpos = xPos
        self.ypos = ypos
        self.iv = iv
        self.radius = radius
        self.color = color

    def draw_ball(self, screen):
        pg.draw.circle(screen, color=self.color, center=(self.xpos, self.ypos), radius=self.radius)

    def update(self):
        tval = 1 / 10
        self.iv += np.array([0, 16 * tval])
        self.iv *= 0.995
        self.xpos += self.iv[0]
        self.ypos += self.iv[1]
        if self.ypos > HEIGHT - 50:
            self.ypos = HEIGHT - 50
            self.iv[1] *= -1
        if self.xpos > WIDTH - 50:
            self.xpos = WIDTH - 50
            self.iv[0] *= -1
        if self.xpos < 50:
            self.xpos = 50
            self.iv[0] *= -1


if __name__ == "__main__":
    ball = Ball(WIDTH / 2, HEIGHT / 2, np.array([5.0, 5.0]), 50, (0, 0, 0))
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        screen.fill((225, 225, 225))
        ball.draw_ball(screen)
        ball.update()
        pg.display.flip()
        clock.tick(60)

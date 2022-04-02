# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:45:35 2022

@author: Casey
"""
import numpy as np
import pygame as pg

RED = (225, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (225, 225, 0)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
INDIGO = (46, 43, 95)
VIOLET = (139, 0, 255)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

Colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]


class Segment:
    def __init__(self, a, b, length, angle):
        # Segement starting position
        self.apos = a
        # Segment ending position
        self.bpos = b
        self.length = length
        # Angle from the Horizontal
        self.angle = angle

    def get_a(self):
        # Find a through polar coordinates
        delta = -1 * self.bpos + self.apos
        self.angle = np.arctan2(delta[1], delta[0])
        newa = self.length * \
            np.array([np.cos(self.angle), np.sin(self.angle)])+self.bpos
        return newa

    def draw_segment(self, surface, COLOR):
        pg.draw.line(surface, COLOR, self.apos, self.bpos, width=3)

    def update(self, bposi):
        self.bpos = bposi
        self.apos = self.get_a()


def list_seg(num):
    # Create a list of segments where the (i+1)th segments b position is the ith a position.
    seglist = [Segment(np.array([350, 350-(600/num)]),
                       np.array([350, 350]), (600/num), 0)]
    for i in range(num-1):
        seglist.append(
            Segment(np.array([350, 350+(600/((i+1)*num))]), seglist[i].apos, (600/num), 0))
    return seglist


# Initialize window size
WIDTH = 700
HEIGHT = 700
size = (WIDTH, HEIGHT)

# Create screen for screen
screen = pg.display.set_mode(size)
done = False
clock = pg.time.Clock()

seglist = list_seg(70)

# While loop for quit
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    screen.fill(WHITE)

    i = 0
    num = len(seglist)
    mod = int(num / 5)

    for index, segment in enumerate(seglist):
        # Cycle through the colors with a "continuous" line between consecutive
        # colors
        if index % mod == 0:
            i += 1
        modi = index % mod
        COLOR = ((1-modi/mod) *
                 np.array(Colors[i-1]) + modi/mod * np.array(Colors[i]))
        COLOR = tuple(COLOR)
        segment.draw_segment(screen, COLOR)

    # Update the screen
    pg.display.flip()

    # Have the first segment follow the mouse.
    seglist[0].bpos = np.array(pg.mouse.get_pos())
    seglist[0].apos = seglist[0].get_a()

    for index, segment in enumerate(seglist):
        if index == 0:
            pass
        else:
            segment.update(seglist[index-1].apos)

    clock.tick(60)

pg.quit()

# -*- coding: utf-8 -*-.
"""
Created on Mon Mar 14 16:45:35 2022

@author: Casey
"""
import numpy as np
import pygame as pg

# Initialize Colors
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

# Initialize window size
WIDTH = 700
HEIGHT = 700
size = (WIDTH, HEIGHT)
T_num = 3


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

    def draw_segment(self, surface, COLOR, WIDTH):
        pg.draw.line(surface, COLOR, self.apos, self.bpos, width=WIDTH)

    def update(self, bposi):
        self.bpos = bposi
        self.apos = self.get_a()


def list_seg(num, factor):
    # Create a list of segments where the (i+1)th segments b position is the
    # ith a position.
    seglist = [Segment(np.array([350, 350-(600/num)]),
                       np.array([350, 350]), (600/num), 0)]
    for i in range(num-1):
        seglist.append(
            Segment(np.array([350, 350+(600/((i+1)*num))]), seglist[i].apos,
                    (300/num), 0))
    return seglist


class Tentacle:
    def __init__(self, factor, seg_num, base):
        self.factor = factor
        self.seg_num = seg_num
        self.base = base
        self.segments = list_seg(seg_num, self.factor)

    def update(self):
        self.segments[0].bpos = np.array(pg.mouse.get_pos())
        self.segments[0].apos = self.segments[0].get_a()

        # Set every segments b position to the a position of the segment infront
        # it.
        for index, segment in enumerate(self.segments[1:]):
            segment.update(self.segments[index].apos)

        # Make the bottom segment fixed to the middle bottom of the screen
        segmentsbkwrd = self.segments[::-1]
        segmentsbkwrd[0].bpos = self.base
        segmentsbkwrd[0].apos = segmentsbkwrd[0].get_a()

        # Adjust the segments going from the bottom segment.
        for index, segment in enumerate(segmentsbkwrd[1:]):
            segment.bpos = segmentsbkwrd[index].apos
            segment.apos = segment.get_a()

    def show(self, screen):
        i = 0
        num = len(self.segments)
        mod = int(num / 5)

        for index, segment in enumerate(self.segments):
            # Cycle through the colors with a "continuous" line between
            # consecutive colors
            if index % mod == 0:
                i += 1
                modi = index % mod
                COLOR = ((1-modi/mod) * np.array(Colors[i-1]) + modi/mod *
                         np.array(Colors[i]))
                COLOR = tuple(COLOR)
                segment.draw_segment(screen, COLOR, 2*i+4)


# Create screen for screen
screen = pg.display.set_mode(size)
base = np.array((WIDTH/2, HEIGHT - 1))
done = False
clock = pg.time.Clock()
tentacles = []
for i in range(T_num):
    theta = (2*np.pi / 3)*i
    pos = np.array((100 * np.cos(theta) + WIDTH /
                   2, 100*np.sin(theta) + HEIGHT/2))
    tentacles.append(Tentacle(1, 200, pos))

# While loop for quiting screen
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    screen.fill(WHITE)

    for tentacle in tentacles:
        tentacle.show(screen)
    # i = 0
    # num = len(seglist)
    # mod = int(num / 5)

    # for index, segment in enumerate(seglist):
    #     # Cycle through the colors with a "continuous" line between consecutive
    #     # colors
    #     if index % mod == 0:
    #         i += 1
    #     modi = index % mod
    #     COLOR = ((1-modi/mod) * np.array(Colors[i-1]) + modi/mod *
    #              np.array(Colors[i]))
    #     COLOR = tuple(COLOR)
    #     segment.draw_segment(screen, COLOR, 2*i+4)

    # Update the screen
    pg.display.flip()

    # Have the first segment follow the mouse.
    # seglist[0].bpos = np.array(pg.mouse.get_pos())
    # seglist[0].apos = seglist[0].get_a()

    # # Set every segments b position to the a position of the segment infront
    # # it.
    # for index, segment in enumerate(seglist[1:]):
    #     segment.update(seglist[index].apos)

    # # Make the bottom segment fixed to the middle bottom of the screen
    # seglistbkwrd = seglist[::-1]
    # seglistbkwrd[0].bpos = base
    # seglistbkwrd[0].apos = seglistbkwrd[0].get_a()

    # # Adjust the segments going from the bottom segment.
    # for index, segment in enumerate(seglistbkwrd[1:]):
    #     segment.bpos = seglistbkwrd[index].apos
    #     segment.apos = segment.get_a()

    for tentacle in tentacles:
        tentacle.update()
    clock.tick(60)

pg.quit()

# -*- coding: utf-8 -*-.
"""
Created on Mon Mar 14 16:45:35 2022

@author: Casey
"""
import numpy as np
import pygame as pg
from math import pi
from BouncingBall import Ball
#Tentacle Parameters
Tentacle_Number = 10
Radius = 300
Segment_Number = 20
Length = 200

#Window Parameters
WIDTH = 1600
HEIGHT = 1000

#Ball Parameters
Follow_Ball = True

RED = (225, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (225, 225, 0)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
INDIGO = (46, 43, 95)
VIOLET = (139, 0, 255)
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
GREY_LIGHT= (169,169,169)
GREY_DARK= (113,113,113)

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

    def draw_segment(self, surface, COLOR, WIDTH):
        pg.draw.line(surface, COLOR, self.apos, self.bpos, width=WIDTH)

    def update(self, bposi):
        self.bpos = bposi
        self.apos = self.get_a()

def list_seg(num,length = 600):
    
    # Create a list of segments where the (i+1)th segments b position is the
    # ith a position.
    seglist = [Segment(np.array([350, 350-(length/num)]),
                       np.array([350, 350]), (length/num), 0)]
    for i in range(num-1):
        seglist.append(
            Segment(np.array([350, 350+(length/((i+1)*num))]), seglist[i].apos,
                    (length/num), 0))
    return seglist



class Tentacle:
    def __init__(self,base,length) -> None:
        self.base = base
        self.segments = list_seg(Segment_Number,length)

    def update_forward(self, reach_for):
        seglist = self.segments
        # Have the first segment follow the mouse.
        seglist[0].bpos = seglist[0].get_a()
        seglist[0].apos = np.array(reach_for)

        # Set every segments b position to the a position of the segment infront
        # it.
        for index, segment in enumerate(seglist[1:]):
            segment.update(seglist[index].apos)
    
    def update_backward(self):
            # Make the bottom segment fixed to the base.
            seglist = self.segments
            seglistbkwrd = seglist[::-1]
            seglistbkwrd[0].bpos = self.base
            seglistbkwrd[0].apos = seglistbkwrd[0].get_a()

            # Adjust the segments going from the bottom segment.
            for index, segment in enumerate(seglistbkwrd[1:]):
                segment.bpos = seglistbkwrd[index].apos
                segment.apos = segment.get_a()
    
    def color_tentacle_rainbow(self):
        seglist = self.segments
        i = 0
        num = len(seglist)
        mod = int(num / 5)

        for index, segment in enumerate(seglist):
            # Cycle through the colors with a "continuous" line between consecutive
            # colors
            if index % mod == 0:
                i += 1
            modi = index % mod
            COLOR = ((1-modi/mod) * np.array(Colors[i-1]) + modi/mod *
                    np.array(Colors[i]))
            COLOR = tuple(COLOR)
            segment.color = COLOR
            

    def draw_tentacle(self):
        num = len(self.segments)
        mod = int(num / 5)
        i = 0
        for index,segment in enumerate(self.segments):
            if index % mod == 0:
                i += 1
            segment.draw_segment(screen, segment.color, 2*i+4)
    
def find_bases(num,r=75):
    bases = []
    angles = np.arange(0,num) * 2*pi/num
    for angle in angles:
        base = np.array([int(r*np.cos(angle)),int(r*np.sin(angle))]) + CENTER
        bases.append(base)
    return bases
    

if __name__ == "__main__":
    # Initialize window size
    size = (WIDTH, HEIGHT)
    CENTER = np.array([WIDTH/2,HEIGHT/2])
    # Create screen for screen
    screen = pg.display.set_mode(size)
    base = np.array((WIDTH/2, HEIGHT-1))
    done = False
    clock = pg.time.Clock()

    ball = Ball(WIDTH/2,HEIGHT/2,np.array([-70.0,-50.0]),25,color=RED)
    tent_list = []
    bases = find_bases(Tentacle_Number,Radius)
    for base in bases:
        tent_list.append(Tentacle(base,Length))
    for tentacle in tent_list:
        tentacle.color_tentacle_rainbow()



 # While loop for quiting screen
    while not done:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                done = True
        screen.fill(GREY_LIGHT)

        if Follow_Ball:
            follow = (ball.xpos,ball.ypos)
        else:
            follow = pg.mouse.get_pos()

        mouse = pg.mouse.get_pos()
        for tentacle in tent_list:
            tentacle.draw_tentacle()
            tentacle.update_forward(follow)
            tentacle.update_backward()

        ball.draw_ball(screen)
        ball.update()
    #     # Update the screen
        pg.display.flip()



        clock.tick(60)

    pg.quit()
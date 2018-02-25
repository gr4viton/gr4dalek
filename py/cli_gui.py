#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from drawille import Canvas, Turtle
from math import sin, radians, atan2, degrees, ceil

from gamepad_control import GamePadControler as GPC

c = Canvas()

for x in range(0, 1800, 1):
    c.set(x/10, 10 + sin(radians(x)) * 10)
        
print(c.frame())


class DirectionView():

    def __init__(self):
        
        self.invx = False
        self.invy = True

        self.can = Canvas()
        self.can.clear()

        s = 8
        decimal_points = 2
        self.dp = 10^decimal_points

        max_ = 512
        max_y = ceil(max_/s)
        max_x = ceil(max_/s)

        half_y = round(max_y/2)
        half_x = round(max_x/2)

        half_dx = round(half_x * 0.8)
        half_dy = round(half_y * 0.8)

        self.half_d = [half_dx, half_dy]

        self.half_x, self.half_y = half_x, half_y

        self.sdx, self.sdy = (0, 0)

        for x in range(0, max_x):
            for y in range(0, max_y):
                if x==0 or x==max_x-1 or y==0 or y==max_y-1:
                    self.can.set(x,y)
                if x==half_x and y==half_y:
                    self.can.set(x,y)
    
        xs = [ 1, -1, 1, -1, 0, 1, 0, -1]
        ys = [ 1, +1,-1, -1, 1, 0,-1,  0]
        self.zip_xs_ys = list(zip(xs,ys))
        
    def round(self, value):
        return round(value * self.dp) / self.dp

    def get_xy(self, x, y):
        return self.sdx + x, self.sdy - y

    def set_cursor(self, show):
        if show:
            [self.can.set(*self.get_xy(x, y)) for x, y in self.zip_xs_ys]
        else:
            [self.can.unset(*self.get_xy(x, y)) for x, y in self.zip_xs_ys]
        
    @property
    def multx(self):
        return 1 if not self.invx else -1
        
    @property
    def multy(self):
        return 1 if not self.invy else -1

    def show_direction(self, direction):
#        print(dir(self.can))
        self.set_cursor(False)
        
        if direction is None:
            return
        self.x, self.y = direction[0:2]

        dx, dy = [ d * maxd for d, maxd in zip(direction[0:2], self.half_d) ]    
        if dx is None and dy is None:
            return

        if len(direction) < 3:
            rad = atan2(float(dy), float(dx))
            deg = degrees(rad)
        else:
            deg = direction[2]
            rad = radians(deg)

        self.sdx = round(self.multx * dx + self.half_x)

        self.sdy = round(self.multy * dy + self.half_y)
            
        #self.can.set(self.sdx, self.sdy)
        self.set_cursor(True)
        
        dp = self.dp
        print(self.can.frame())

        #print('angle = ', round(deg*dp)/dp, ' deg = ', round(rad*dp)/dp, ' rad')a

        print(self.round(self.x), ', ', self.round(self.y), ', ', self.round(deg), '°')
        #print('sdx,sdy] = ', self.sdx, ', ', self.sdy)

if __name__ == '__main__':
    print('Hey')
    gpc = GPC()
    dv_left = DirectionView()
    dv_right = DirectionView()
    while(1):
        gpc.update(info=0)

#        data = gpc.childs['rightstick'].data
#        data = gpc.btns['LHstick'].data
        left = gpc.btns['leftstick'].fdata
        right = gpc.btns['rightstick'].fdata

        dv_left.show_direction(left)
        dv_right.show_direction(right)


        


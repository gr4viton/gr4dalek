
from __future__ import print_function
from drawille import Canvas, Turtle
from math import sin, radians, atan2, degrees, ceil

from main import GamePadControler as GPC

c = Canvas()

for x in range(0, 1800, 1):
    c.set(x/10, 10 + sin(radians(x)) * 10)
        
print(c.frame())

can = Canvas()
def show_direction(direction):
#    print(dir(can))
    can.clear()
    

    s = 8
    decimal_points = 2
    dp = 10^decimal_points
    h = ceil(256/s)
    w = ceil(256/s)

    if direction is None:
        return
    dx, dy = direction
    dx = (dy*256 + dx)/256
    
    dy = 256/2

    if dx is None and dy is None:
        return

    sdx = round(dx/s)
    sdy = round(dy/s)

    rad = atan2(float(dy), float(dx))
    deg = degrees(rad)

    for x in range(0, h):
        for y in range(0, w):
            if x==0 or x==w-1 or y==0 or y==h-1:
                can.set(x,y)
            if x==h/2 and y==h/2:
                can.set(x,y)

            if x==sdx and y==sdy:
                can.set(x,y)


    print(can.frame())
    print('angle = ', round(deg*dp)/dp, ' deg = ', round(rad*dp)/dp, ' rad')
    print('dir[x,y] = ', dx, ', ', dy)
if __name__ == '__main__':
    print('Hey')
    gpc = GPC()
    while(1):
        gpc.update()

        data = gpc.childs['rightstick'].data
        data = gpc.btns['LHstick'].data
        show_direction(data)

        


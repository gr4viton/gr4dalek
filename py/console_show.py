
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
    max_y = ceil(256/s)
    max_x = ceil(256/s)

    half_y = round(max_y/2)
    half_x = round(max_x/2)

    print('directionXYdeg' , direction)
    if direction is None:
        return

    dx, dy = [ d* maxd for d, maxd in zip(direction[0:2], [half_x, half_y]) ]    

    if dx is None and dy is None:
        return

    if len(direction)<3:
        rad = atan2(float(dy), float(dx))
        deg = degrees(rad)
    else:
        deg = direction[2]
        rad = radians(deg)

    sdx = round(dx + half_x)
    sdy = round(dy + half_y)

    for x in range(0, max_x):
        for y in range(0, max_y):
            if x==0 or x==max_x-1 or y==0 or y==max_y-1:
                can.set(x,y)
            if x==half_x and y==half_y:
                can.set(x,y)

            if x==sdx and y==sdy:
                can.set(x,y)


    print(can.frame())
    print('angle = ', round(deg*dp)/dp, ' deg = ', round(rad*dp)/dp, ' rad')
    print('dx,dy] = ', dx, ', ', dy)
    print('sdx,sdy] = ', sdx, ', ', sdy)

if __name__ == '__main__':
    print('Hey')
    gpc = GPC()
    while(1):
        gpc.update()

        data = gpc.childs['rightstick'].data
        data = gpc.btns['LHstick'].data
        data = gpc.btns['leftstick'].fdata
        show_direction(data)

        


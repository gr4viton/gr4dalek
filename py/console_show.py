
from __future__ import print_function
from drawille import Canvas, Turtle
from math import sin, radians, atan2, degrees, ceil

from main import GamePadControler as GPC

c = Canvas()

for x in range(0, 1800, 1):
    c.set(x/10, 10 + sin(radians(x)) * 10)
        
print(c.frame())


class DirectionView():

    def __init__(self):
        self.can = Canvas()
        self.can.clear()

        s = 8
        decimal_points = 2
        self.dp = 10^decimal_points

        max_ = 256
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
        

    def show_direction(self, direction):
#        print(dir(self.can))
        [self.can.unset(self.sdx + x, self.sdy + y) for x, y in self.zip_xs_ys]

        if direction is None:
            return
        dx, dy = [ d* maxd for d, maxd in zip(direction[0:2], self.half_d) ]    

        if dx is None and dy is None:
            return

        if len(direction)<3:
            rad = atan2(float(dy), float(dx))
            deg = degrees(rad)
        else:
            deg = direction[2]
            rad = radians(deg)

        self.sdx = round(dx + self.half_x)
        self.sdy = round(dy + self.half_y)
            
        #self.can.set(self.sdx, self.sdy)
        [self.can.set(self.sdx + x, self.sdy + y) for x, y in self.zip_xs_ys]
        
        dp = self.dp
        print(self.can.frame())
        #print('angle = ', round(deg*dp)/dp, ' deg = ', round(rad*dp)/dp, ' rad')
        #print('dx,dy] = ', dx, ', ', dy)
        #print('sdx,sdy] = ', self.sdx, ', ', self.sdy)

if __name__ == '__main__':
    print('Hey')
    gpc = GPC()
    dv = DirectionView()
    while(1):
        gpc.update(info=0)

#        data = gpc.childs['rightstick'].data
#        data = gpc.btns['LHstick'].data
        data = gpc.btns['leftstick'].fdata
        dv.show_direction(data)


        


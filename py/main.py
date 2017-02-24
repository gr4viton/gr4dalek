import sys

class GamePadButton():
    
    def __init__(self, address, kind, name, dir1=None, dir2=None):
        self.name = name
        self.add = address
        self.kind = kind
        if dir1 is not None:
            self.dir = [int(dir1), int(dir2)]
        self.state = 0

    def __repr__(self):
        return ''.join([str(word) for word in ['type=', self.kind,
                        ', add= ',self.add,
                        ', name="',self.name,
                        '", state= ', self.state]])
           
class GamePadControler():
    def __init__(self):
        self.open()
        actions = \
"""
1,0:b:A button
1,1:b:B button
1,3:b:X button
1,4:b:Y button
1,6:b:L1 button
1,7:b:R1 button
1,10:b:SELECT button
1,11:b:START button

2,0:s:Left horizontal stick
2,1:s:Left vertical stick
2,2:s:Right horizontal stick
2,3:s:Right vertical stick

2,4:b:R2 button
2,5:b:L2 button

2,6,1,128:a:Left arrow
2,6,255,127:a:Right arrow
2,6,1,128:a:Up arrow
2,7,255,127:a:Down arrow

"""
        self.longer_addresses = [(2,6), (2,7)]

        minimal_line = '1,1:b:A'
        x = [line for line in actions.split('\n')]
        x = [line.split(':') for line in x if len(line)>=len(minimal_line)]
        self.states = {tuple([int(add) for add in address.split(',')]):list(data) 
                            for address, *data in x}
        print(self.states)

        self.btns = {key : GamePadButton(key, *value) 
                for key, value in self.states.items()}

#        for key, value in self.states.items():
#            print(key, value)
#            btn = GamePadButton(key, *value) 
#            self.btns.append(btn)
#            print(btn)

        print(self.btns)
        
        
    def open(self):
        self.pipe = open('/dev/input/js0', 'rb') #open joystick 
        action = []
    
    def update(self):
        self.readData()
        print(self.state)
        add = self.state[6:8]
        data = self.state[4:6]
        print('data', data)
        print('address', add)
        
#        self.btns[

    def readData(self):
        action = []
        stop = 1
        while stop == 1:
            for character in self.pipe.read(1):
                action += [int(character)]
                if len(action) == 8:
                    self.state = action
                    action = []
                    stop = 2
                    ##when joystick is stationary code hangs here.


if __name__ == '__main__':
    gpc = GamePadControler()
    while(1):
        gpc.update()

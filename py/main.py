import sys

class GamePadButton():
    
    def __init__(self, address, kind, abbreviation,name):
        self.abbr = abbreviation
        self.name = name
        self.add = address
        self.kind = kind
        self.state = 0
        self.data = None

    def update(self, data):
        self.data = data
        self.state = sum(data) > 0

    def __repr__(self):
        return ''.join([str(word) for word in ['type=', self.kind,
                        ', add= ',self.add,
                        ', name="',self.name,
                        '", state= ', self.state,
                        ', data=', self.data]])
           
class GamePadControler():
    def __init__(self):
        self.open()
        actions = \
"""
1,0:b:A:A button
1,1:b:B:B button
1,3:b:X:X button
1,4:b:Y:Y button
1,6:b:L1:L1 button
1,7:b:R1:R1 button
1,10:b:select:SELECT button
1,11:b:start:START button

2,0:s:LHstick:Left horizontal stick
2,1:s:LVstick:Left vertical stick
2,2:s:RHstick:Right horizontal stick
2,3:s:RVstick:Right vertical stick

2,4:b:R2:R2 button
2,5:b:L2:L2 button

2,6:a:leftright:Horizontal arrows
2,7:a:updown:Vertical arrows
"""

        
        minimal_line = '1,1:b:A'
        x = [line for line in actions.split('\n')]
        x = [line.split(':') for line in x if len(line)>=len(minimal_line)]
        self.states = {tuple([int(add) for add in address.split(',')]):list(data) 
                            for address, *data in x}
        print(self.states)

        self.btns = {key : GamePadButton(key, *value) 
                for key, value in self.states.items()}

        named = {btn.abbr : btn for btn in self.btns.values()}
        self.btns.update(named)

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
        print('>>>>> GOT NEW ACTION')
        print(self.state)
        add = tuple(self.state[6:8])
        data = self.state[4:6]
        print('data', data)
        print('address', add)
        
        if self.btns.get(add) is not None:
            self.btns[add].update(data)
            print(self.btns[add])

        print(self.btns['updown'].state)

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

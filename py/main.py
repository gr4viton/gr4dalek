import sys
from math import atan2, degrees
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# now, to clear the screen
cls()

class GamePadSwHotkey(object):
#    hw_btn_attr_names = ['kind', 'add', 'data']

    def __init__(self, abbreviation, name, hw_btns, format_func):
        self.hw_btns = hw_btns
        self.format_func = format_func
        self._state = False
        self.name = name
        self.abbr = abbreviation
        self._fdata = None
        self.kind = 'h'

        if hw_btns is not None and format_func is not None:
#            if len(hw_btns) != len(self.format_funcs):
#                raise 'number of hw_btns in hw_btns list must be the same as format_funcs'
#            print('')
            pass
        else:
            raise 'hw_btns and format_funcs must not be empty!'

    @property
    def fdata(self):
        self.update_fdata()
        return self._fdata

    #def kind(self):
    #    return self.hw_btn.kind

 #   def __getattr__(self, name):
  #      if name in self.hw_btn_attr_names:
   #         return self.hw_btn.__dict__[name]
#        elif name == 'state':
#            print('NAME IS STATE')
#            self.update_state()
#            return self.state
    #    else:
     #       return self.__dict__[name]

    def update_fdata(self):
 #       print(hw_btns)

        datas = [hw_btn.fdata for hw_btn in self.hw_btns]
#        print(datas)
        self._fdata = self.format_func(*datas)

    def __str__(self):
        return ''.join([str(word) for word in [
                        self.kind,
                        '= ', self.abbr, ' = ', self.name,
                        ', fdata= ', self.fdata,]])
           
class GamePadSwChildControl():
    def __init__(self, abbreviation, name, parents):
        self.abbr = abbreviation
        self.name = name
        self.data = [None, None]
        self.parent_names = parents

    def __str__(self):
        return ''.join([str(word) for word in [
                        self.abbr,' = ',self.name, ' = ', self.data
                        ]])


class GamePadHwButton():
    
    def __init__(self, address, kind, abbreviation, name, format_function=None):
        self.abbr = abbreviation
        self.name = name
        self.add = address
        self.kind = kind
        self.state = False
        self.child = self.trigger = self.data = None
        self.ffunc = None
        if format_function is not None:
            if type(format_function) is str:
                format_function = GamePadControler.format_funcs[format_function]
            self.ffunc = format_function
        self.fdata = None


    def update(self, data):
        self.data = data
        self.state = sum(data) > 0
        if self.ffunc is not None:
            self.fdata = self.ffunc(self.data)

    def __repr__(self):
        return ''.join([str(word) for word in [
                        self.kind,'=hwa', self.add,
#                        '= ', self.abbr, ' = ', self.name,
                        '= ', self.abbr, 
                        ', state= ', self.state,
                        ', data=', self.data,
                        ', fdata= ', self.fdata]])
           
class GamePadControler():
    
    def format_directionXY(xdata, ydata):
        if xdata is None:
            x = 0
        else:
            x = xdata

        if ydata is None:
            y = 0
        else:
            y = ydata

        return [x,y]

    def format_directionXYDegree(xdata, ydata):
        xy = GamePadControler.format_directionXY(xdata, ydata)
        print(xy)
        deg = degrees(atan2(float(xy[0]),float(xy[1])))
        return xy + [deg]


    def format_trigger_upleft_arrows(data):
        if data == [1, 128]:
            return True
        else:
            return False

    def format_trigger_downright_arrows(data):
        if data == [127, 255]:
            return True
        else:
            return False


    def format_2byte(data):
        if data is not None:
            val = data[1]*255 + data[0]  
            valorig = val
            half = 32640
            if val == 0:
                val = 0
            elif val <= half:
                val = val 
            elif val > half:
                val = val - 2*half -1
            val = val / half
            return val

    format_funcs = {'format_2byte': format_2byte}

    def __init__(self):
        self.open()

        sw_childs = \
"""leftstick:Left stick:LVstick:LHstick
rightstick:Right stick:RVstick:RHstick"""

        x = [line.split(':') for line in sw_childs.split('\n')]
        self.childs = {}
        self.childs.update({abbr :GamePadSwChildControl(abbr, name, hw_btn_names) 
                                for abbr, name, *hw_btn_names in x})



        hw_btns_text = \
"""
1,0:b:A:A button
1,1:b:B:B button
1,3:b:X:X button
1,4:b:Y:Y button
1,6:b:L1:L1 button
1,7:b:R1:R1 button
1,10:b:select:SELECT button
1,11:b:start:START button

2,0:s:LHstick:Left horizontal stick:format_2byte
2,1:s:LVstick:Left vertical stick:format_2byte
2,2:s:RHstick:Right horizontal stick:format_2byte
2,3:s:RVstick:Right vertical stick:format_2byte

2,4:b:R2:R2 button
2,5:b:L2:L2 button

2,6:a:leftright:Horizontal arrows
2,7:a:updown:Vertical arrows
"""

        
        minimal_line = '1,1:b:A'
        x = [line for line in hw_btns_text.split('\n')]
        x = [line.split(':') for line in x if len(line)>=len(minimal_line)]
        self.states = {tuple([int(add) for add in address.split(',')]):list(data) 
                            for address, *data in x}
        print(self.states)
        
        
        self.hw_btns = {}
        for key, value in self.states.items():
#            if len(value) > 3: # child 
#                value[3] = self.childs[value[3]]
            self.hw_btns.update({key: GamePadHwButton(key, *value)})

        self.btns = {btn.abbr : btn for btn in self.hw_btns.values()}

        sw_hotkeys = \
"""up:UP arrow:updown:format_trigger_upleft_arrows
down:DOWN arrow:updown:format_trigger_downright_arrows
leftstick:Left stick:LHstick,LVstick:format_directionXYDegree
left:LEFT arrow:leftright:format_trigger_upleft_arrows
right:RIGHT arrow:leftright:format_trigger_downright_arrows"""

        x = [line.split(':') for line in sw_hotkeys.split('\n')]
        self.btns.update({abbr : GamePadSwHotkey(
                                abbr, name, 
                                [self.btns[hw_btn] for hw_btn in hw_btns.split(',')],
                                GamePadControler.__dict__[format_func]
                                )
                            for abbr, name, hw_btns, format_func in x})


        [print(str(btn)) for btn in self.btns.values()]
        [print(str(stc)) for stc in self.childs.values()]
    def open(self):
        self.pipe = open('/dev/input/js0', 'rb') #open joystick
        action = []
    
    def update(self):
        self.read_data()
        cls()
        print('>>>>> GOT NEW ACTION ', self.state)
        add = tuple(self.state[6:8])
        data = tuple(self.state[4:6])
        print('data', data)
        print('address', add)
        
        if self.hw_btns.get(add) is not None:
            self.hw_btns[add].update(data)
            print(self.hw_btns[add])

        #print(self.btns['up'])
   #     print(self.btns['up'])
   #     print(self.btns['down'])
   #     print(self.btns['left'])
   #     print(self.btns['right'])

        print(self.childs['leftstick'])
        print(self.childs['rightstick'])
        


        
    def read_data(self):
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

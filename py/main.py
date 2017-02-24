import sys


class GamePadControl():
    def __init__(self):
        self.open()

    def open(self):
        self.pipe = open('/dev/input/js0', 'rb') #open joystick 
        self.action = []
    
    def updateState(self):
        self.state = self.eadGamePadData()

while True:
    StickValue = readStik(pipe)
    print ("StickValue")

    def readGamePadData(self):
        action = []
        stop = 1
        while stop == 1:
            for character in self.pipe.read(1):
                self.action += [int(character)]
                if len(self.action) == 8:
                    self.state = action
                    action = []
                    stop = 2
                    ##when joystick is stationary code hangs here.

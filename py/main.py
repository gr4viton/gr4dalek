#!/usr/bin/env python
#
# Bitbang'd SPI interface with an MCP3008 ADC device
# MCP3008 is 8-channel 10-bit analog to digital converter
#  Connections are:
#     CLK => SCLK  
#     DOUT =>  MISO
#     DIN => MOSI
#     CS => CE0

import time
import sys
#import spidev

from struct import unpack, pack
from cli_gui import DirectionView
from gamepad_control import GamePadControler as GPC
 
import wiringpi as wp

from stmcom import StmCom

from visual import VisualControl


class DalekRPi():
    def __init__(self):

        self.init_com()
        self.init_gamepad()
        self.init_visual()

    def init_visual(self):
        self.vc = VisualControl()
        

    def init_com(self):
        self.com = StmCom()

    def on_exit(self):
        self.com.on_exit()

    def init_gamepad(self):
        self.gpc = GPC()
        self.dv_left = DirectionView()
        self.dv_right = DirectionView()
        self.show_direction = False

    def run(self):
        self.vc.run()

        self.update_loop()

    def update_loop(self):
        stick_names = ('leftstick', 'rightstick')
        stick_dvs = (self.dv_left, self.dv_right)
        while True:
            i = 0

            self.gpc.update(info=0, clear_screen=True)
            
            for name, dv in zip(stick_names, stick_dvs):
                fdata, changed = self.gpc.btns[name].fdata_changed
            
                if self.show_direction:
                    dv.show_direction(fdata)
                
                if  changed:
                    self.com.write_pot_uart(name, fdata)

    



if __name__ == '__main__':
    print('Hey')
    dalek = DalekRPi()
    dalek.run()
    dalek.on_exit()

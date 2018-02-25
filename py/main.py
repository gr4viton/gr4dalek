#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bitbang'd SPI interface with an MCP3008 ADC device.

MCP3008 is 8-channel 10-bit analog to digital converter
Connections are:
    CLK => SCLK  
    DOUT =>  MISO
    DIN => MOSI
    CS => CE0
"""

import time
import sys
#import spidev

from struct import unpack, pack
from cli_gui import DirectionView
from gamepad_control import GamePadControler as GPC
 
import wiringpi as wp

from stmcom import StmCom
sys.path.append("/home/pi/DEV/gr4dalek/micropy/src")

from actions import Actions as Act

# from visual import VisualControl


class DalekRPi():
    def __init__(self):

        self.init_com()
        self.init_gamepad()
        self.init_visual()

    def init_visual(self):
      #  self.vc = VisualControl()
        self.vc = None

    def init_com(self):
        self.com = None
        self.com = StmCom()

    def on_exit(self):
        self.com.on_exit()

    def init_gamepad(self):
        self.gpc = GPC()
        self.dv_left = DirectionView()
        self.dv_right = DirectionView()
        self.show_direction = False
        self.show_direction = True

    def run(self):

        try:
            self.vc.run()
        except:
            print('no visual control')

        self.update_loop()

    def btn(self, abbreviation):
        return self.gpc.btns.get(abbreviation)

    def update_loop(self):
        stick_names = ('leftstick', 'rightstick')
        stick_dvs = (self.dv_left, self.dv_right)
        while True:
            i = 0

            self.gpc.update(info=0, clear_screen=True)
            a_btn = self.btn('A')
            a_pressed = a_btn.state
            a_chng = a_btn.changed_down
            print('a pressed = ', a_pressed)
            print('a changed_down = ', a_chng)
            if a_chng:
                fdata = [0, 0, 0]
                [self.com.write_pot_uart(name, fdata) for name in stick_names]
                # self.com.send_data('HEY!')

            abbs = 'up down left right'.split()
            xyzs = [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0]]
            btns_dict = {
                self.btn(abb): xyz
                for abb, xyz in zip(abbs, xyzs)
            }

            for btn, xyz in btns_dict.items():
                if btn.fdata_changed and btn._state:
                    self.com.write_pot_uart('leftstick', fdata)

            if self.btn('L1').changed_down:
                self.com.start(Act.motor_control)

            if self.btn('R1').changed_down:
                self.com.stop(Act.motor_control)

            for name, dv in zip(stick_names, stick_dvs):
                fdata, changed = self.gpc.btns[name].fdata_changed
                
                if self.show_direction:
                    dv.show_direction(fdata)
                
                if changed:
                    self.com.write_pot_uart(name, fdata)


if __name__ == '__main__':
    print('Hey')
    dalek = DalekRPi()
    dalek.run()
    dalek.on_exit()

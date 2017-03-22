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


class DalekRPi():
    def __init__(self):
        #self.init_gamepad()
        self.init_wiringpi()

    def init_wiringpi(self):
        self.init_uart()
        #self.init_spi()

    def init_uart(self):
        self.uart = wp.serialOpen('/dev/ttyAMA0', 9600)
        wp.serialPuts(self.uart, 'hello')
        wp.serialClose(self.uart)


    def init_spi(self):
#            https://projects.drogon.net/raspberry-pi/wiringpi/pins/
        wp.wiringPiSetup()

        self.SPIchannel = 1 #SPI Channel (CE1)
        SPIspeed = 500000 #Clock Speed in Hz
        spi_mode = 0 # cpol 0, cpha 0, cedg 1

        ret = wp.wiringPiSPISetupMode(self.SPIchannel, SPIspeed, spi_mode)
        if ret == -1:
            print('SPI setup returned error')
            return
#           print(str(dir(wp)).replace(' ', '\n'))
        print('>> SPI initialized')
        ret = wp.wiringPiSPIGetFd(self.SPIchannel)
        print('spi file-descriptor', ret)

        print('starting spi loop')
        i=0
        while True:
        
            self.write_pot(i)
            time.sleep(1)
            i += 1

    def write_pot_spi(self, input):
        """ Split an integer input into a two byte array to send via SPI
        """
        
        data = input
        try:
            ret = wp.wiringPiSPIDataRW(self.SPIchannel, 'a')
        except e:
            print('error')
            print(e)
        print('got returned')
        print('returned data', data)


    def init_gamepad(self):
        self.gpc = GPC()
        self.dv_left = DirectionView()
        self.dv_right = DirectionView()
        
    def run(self):
        self.update_loop()


    def update_loop(self):
        while(1):
            self.gpc.update(info=0)

            left = self.gpc.btns['leftstick'].fdata
            right = self.gpc.btns['rightstick'].fdata

            self.dv_left.show_direction(left)
            self.dv_right.show_direction(right)

if __name__ == '__main__':
    print('Hey')
    dalek = DalekRPi()
    print('eof')
    pass

    dalek.run()

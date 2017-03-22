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

#class ControlSTM():
#    def __init__(self):


class DalekRPi():
    def __init__(self):
        self.init_wiringpi()
        self.init_gamepad()

    def init_wiringpi(self):
        self.init_uart()
        #self.init_spi()



    def init_uart(self):
        self.ch_end = '\n'

        self.uart = wp.serialOpen('/dev/ttyAMA0', 115200)
        
        self.send_str('>>>>>J')

        print(str(dir(wp)).replace(' ', '\n'))
    
    def on_exit(self):
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


    def send_str(self, data):
        checksum = 0
        for ch in data:
            checksum ^= ord(ch)
                
        print('checksum', checksum, 'for str', data)
        data = data + self.ch_end + chr(checksum)

        
        wp.serialPuts(self.uart, data)
        wp.serialFlush(self.uart)
        print('sent data', data.encode())


    def write_pot_uart(self, input):
        
        data = str(input)+'\n'
        
        data = '_'.join([ str(round(val, 2)) for val in input])

        self.send_str(data)

    def update_loop(self):
        stick_names = ('leftstick', 'rightstick')
        stick_dvs = (self.dv_left, self.dv_right)
        while True:
            i = 0

            self.gpc.update(info=0)
            
            for name, dv in zip(stick_names, stick_dvs):
                fdata, changed = self.gpc.btns[name].fdata_changed
            
                dv.show_direction(fdata)
                
                if  changed:
                    self.write_pot_uart(fdata)



if __name__ == '__main__':
    print('Hey')
    dalek = DalekRPi()
    dalek.run()
    dalek.on_exit()

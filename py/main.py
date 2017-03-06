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
import spidev

from cli_gui import DirectionView
from gamepad_control import GamePadControler as GPC
 

class DalekRPi():
        def __init__(self):
            #self.init_gamepad()
            self.init_spi()

        def init_spi(self):
            self.spi = spidev.SpiDev()
            self.spi.open(0,0)
            self.spi.max_speed_hz = 60000
    
            a = [1]
            print(a)
            i = 0
            while True:
                #[0x42])
                print('sent', a)
                resp = self.spi.xfer(a)
                print('got', resp[0])
                time.sleep(1)
                
                i += 1
                #a =a [i, i+1, i+2, i+3]
                a = [i]

        def write_pot(input):
            """ Split an integer input into a two byte array to send via SPI
            """
            msb = input >> 8
            lsb = input & 0xFF
            self.spi.xfer([msb, lsb])

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
                                    
def buildReadCommand(channel):
    startBit = 0x01
    singleEnded = 0x08

# Return python list of 3 bytes
#   Build a python list using [1, 2, 3]
#   First byte is the start bit
#   Second byte contains single ended along with channel #
#   3rd byte is 0
    return []

def processAdcValue(result):
    '''Take in result as array of three bytes. 
    Return the two lowest bits of the 2nd byte and
    all of the third byte'''
    pass

def readAdc(channel):
    if ((channel > 7) or (channel < 0)):
        return -1
    r = spi.xfer2(buildReadCommand(channel))
    return processAdcValue(r)




if __name__ == '__main__':
    print('Hey')
    dalek = DalekRPi()
    dalek.run()

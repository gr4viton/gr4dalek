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
 
import wiringpi



SPIchannel = 1 #SPI Channel (CE1)
SPIspeed = 500000 #Clock Speed in Hz
wiringpi.wiringPiSetupGpio()
wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)



sendData = str(42) #will send TWO bytes, a byte 4 and a byte 2
recvData = wiringpi.wiringPiSPIDataRW(SPIchannel, sendData)
#recvData now holds a list [NumOfBytes, recvDataStr] e.g. [2, '\x9A\xCD']

#alternatively, to send a single byte:
sendData = chr(42) #will send a single byte containing 42
recvData = wiringpi.wiringPiSPIDataRW(SPIchannel, sendData)
#recvData is again a list e.g. [1, '\x9A']


time.p

class DalekRPi():
        def __init__(self):
            #self.init_gamepad()
            self.init_spi()

        def init_spi(self):
            self.spi = spidev.SpiDev()
            self.spi.open(0,0)
            self.spi.max_speed_hz = 60000
            print(dir(self.spi))
            print('lsb first = big endian =', self.spi.lsbfirst)
            self.spi_mode = 0
            print('polarity =', self.spi.mode)
            #self.
            maxi = 2**31-1
            maxi = 15
            i = 1
            print('spi loop starting')
            
            while True:
                #[0x42])
                #i = i*2
                i = i+1
                if i >= maxi:
                    i = 0
                a = pack('<b', i)
                aa = [int(B) for B in a]

                print('____')
                print('sent', i, aa, a, sep='\t')
                resp = self.spi.xfer2(a)
                print('got', resp[0], sep='\t')
                time.sleep(1)
            self.spi.close()
            exit()
                

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

if __name__ == '__main__':
    print('Hey')
    dalek = DalekRPi()
    dalek.run()

#!/usr/bin/python
#
#  lcd_i2c.py
#  lcd1602 class for character display initialization and usage via micropython
#  Supports 16x2 and 20x4 screens.
#
# Author : gr4vion
# Date   : 28-10-2016
#
# On the base of: Matt Hawkins
# http://www.raspberrypi-spy.co.uk/
# and 2013-2015 Danilo Bargen RPILCD
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------
import pyb
from pyb import I2C 


class lcd1602():
    # Define some device parameters
    I2C_ADDR  = None # I2C device address
    LCD_WIDTH = 16   # Maximum characters per line
    NUM_LINES = 2    # Number of lines

    # Define some device constants
    LCD_CHR = 1 # Mode - Sending data
    LCD_CMD = 0 # Mode - Sending command

    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

    line_nums = [LCD_LINE_1, LCD_LINE_2, LCD_LINE_3, LCD_LINE_4]

    LCD_BACKLIGHT_ON = 0x08  # On
    LCD_BACKLIGHT_OFF = 0x00  # Off
    backlight = LCD_BACKLIGHT_ON 

    ENABLE = 0b00000100 # Enable bit

    # Timing constants
    E_PULSE = 0.0005*1000000 #us
    E_DELAY = 0.0005*1000000 #us

    E_PULSE = int(E_PULSE)
    E_DELAY = int(E_DELAY)
    # Open I2C interface
    #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    #bus = smbus.SMBus(1) # Rev 2 Pi uses 1
    blank_char = ' '

    # # # BIT PATTERNS # # #

    # Commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # Flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # Flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # Flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    # Flags for RS pin modes
    RS_INSTRUCTION = 0x00
    RS_DATA = 0x01
    null_char = ' '

    
    def __init__(self, i2c, lcd_addr,  LCD_WIDTH=16, NUM_LINES=2, backlight_status=True):
        self.i2c = i2c
        self.I2C_ADDR = lcd_addr
        self.LCD_WIDTH = LCD_WIDTH 
        self.NUM_LINES = NUM_LINES 
        self.backlight_status = backlight_status
        self.update_backligth()
        self._cursor_pos = [0,0]
#        self.lcd_a = lcd_addr
        self.row_offsets = [0x00, 0x40, self.LCD_WIDTH, 0x40 + self.NUM_LINES]
        self.send_init_sequence()

    def update_backligth(self):
        self.set_backligth(self.backlight_status)

    def set_backligth(self, status=True):
        self.backlight = self.LCD_BACKLIGHT_ON if status else self.LCD_BACKLIGHT_OFF

    def send_init_sequence(self):
      # Initialise display
      self.send_cmd(0x33) # 110011 Initialise
      self.send_cmd(0x32) # 110010 Initialise
      self.send_cmd(0x06) # 000110 Cursor move direction
      self.send_cmd(0x0C) # 001100 Display On,Cursor Off, Blink Off 
      self.send_cmd(0x28) # 101000 Data length, number of lines, font size
      self.send_cmd(0x01) # 000001 Clear display
      pyb.udelay(self.E_DELAY)

    def i2c_write_byte(self, add, byte):
      self.i2c.send(byte, addr=add)  

    def send_cmd(self, bits):
        self.send_byte(bits, self.LCD_CMD)

    def send_char(self, bits):
        self.send_byte(bits, self.LCD_CHR)

    def send_byte(self, bits, mode):
      # Send byte to data pins
      # bits = the data
      # mode = 1 for data
      #        0 for command

      bits_high = mode | (bits & 0xF0) | self.backlight
      bits_low = mode | ((bits<<4) & 0xF0) | self.backlight

      # High bits
      self.i2c_write_byte(self.I2C_ADDR, bits_high)
      self.lcd_toggle_enable(bits_high)

      # Low bits
      self.i2c_write_byte(self.I2C_ADDR, bits_low)
      self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
      # Toggle enable
      pyb.udelay(self.E_DELAY)
      self.i2c_write_byte(self.I2C_ADDR, (bits | self.ENABLE))
      pyb.udelay(self.E_PULSE)
      self.i2c_write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
      pyb.udelay(self.E_DELAY)


    def print_warning(self, topic=None, **kwargs):
        if topic == 'line_max':
            print('Cannot disp on line indexed {}.',
                'LCD initialized with only {} horizontal lines!'.format(
                line_num, self.NUM_LINES))
        elif topic == 'pos_max':
            print('Cannot disp on pos indexed {}.',
                'LCD initialized with only {} vertical chars!'.format(
                pos, self.LCD_WIDTH))

    def _set_cursor_pos(self, pos, pos_char=None):
        if pos_char is not None:
            self._cursor_pos[0] = pos
            self._cursor_pos[1] = pos_char
        else:
            # heap safe
            self._cursor_pos[0] = pos[0]
            self._cursor_pos[1] = pos[1]



        self.send_cmd(self.LCD_SETDDRAMADDR | \
                self.row_offsets[self._cursor_pos[0]] \
                + self._cursor_pos[1])
        #usleep(50)


    def disp_char(self, new_char, line_num, pos):
      if line_num > self.NUM_LINES:
          self.print_warning('line_max', line_num=line_num)
          return
      if pos > self.LCD_WIDTH:
          self.print_warning('pos_max', pos=pos)
          return
        
      self._set_cursor_pos(line_num, pos)

      byte = ord(new_char)

      self.send_char(byte)


    def disp(self, message, line_num):
      # Send string to display line
      if line_num > self.NUM_LINES:
          self.print_warning('line_max', line_num=line_num)
          return
      line = self.line_nums[line_num]


    #  message = message.ljust(LCD_WIDTH," ")

      self.send_cmd(line)
      #print(message)

      #if LCD_WIDTH > len(message):
      #  length = len(message)
      #else:
      #  length = LCD_WIDTH

      length = len(message)
      for i in range(self.LCD_WIDTH):

        if i >= length:
          byte = ord(self.blank_char)
        else:
          byte = ord(message[i])

        self.send_char(byte)
    
    def clear(self):
        self.disp(self.null_char*16, 0)

def main():
  # Main program block

  # Initialise display
  
  lcd = lcd1602()
#  lcd_init()

  while True:

    # Send some test
    lcd.disp("RPiSpy         <", 0)
    lcd.disp("I2C LCD        <", 1)

    pyb.delay(500)
  
    # Send some more text
    lcd.disp(">         RPiSpy", 0)
    lcd.disp(">        I2C LCD", 1)

    pyb.delay(500)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd.send_cmd(0x01)


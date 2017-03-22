import pyb
#from pyb import I2C, SPI, UART

#import staccel
import math

#import os
#import gc # garbage collection for writing?

#import microsnake
#from microsnake import MicroSnakeGame as Game
#from microsnake import move_arrow_pressed

import shared_globals

#from shared_globals import move_arrow_pressed as move_arrow_pressed

#from struct import unpack, pack # not interrupt safe = using heap
#import binascii as ba

#import lcd_i2c

#from dcmotor import DCMotor

import micropython
#import boot
#boot.print_version()

#micropython.alloc_emergency_exception_buf(100)
#print('Micropython alloc_emergency_exception_buffer set to 100')

#import operator # dict sorting
#try: 
#    print('try importing pins')
#    import pins
#except ImportError:
#    print('pins not found')

#from machine import Pins

#print('>>>>>>> shape assert')
#a = [[[1,2],[1,2]],[[1,2],[1,2]]]
#print(shared_globals.print_shape(a))

class FakePin():
    def value(q, value):
        pass

class DCMotor():

    def __init__( q, name, in1_pin, in2_pin, 
            tim_num, tim_channel, tim_pin, 
            dir_en=1, tim_freq=30000): 

         #       print(q.__dict__)
        q.name = name.strip()
        q.in1_pin = in1_pin
        q.in2_pin = in2_pin
        q.tim_num = int(tim_num)
        q.tim_channel = int(tim_channel)
        q.tim_pin = tim_pin
        q.dir_en = int(dir_en)
        q.tim_freq = float(tim_freq)

        q.velocity = 0
        
        if dir_en:
            q.in1 = pyb.Pin(in1_pin, pyb.Pin.OUT_PP)
            q.in2 = pyb.Pin(in2_pin, pyb.Pin.OUT_PP)
            q.in1.value(0)
            q.in2.value(0)
        else:
            q.in1 = FakePin()
            q.in2 = FakePin()

        q.tim = pyb.Timer(tim_num)
        q.tim.init(freq=tim_freq)        
#        q.en = q.tim.channel(tim_channel, pyb.Timer.PWM, pin=tim_pin)
        q.en = q.tim.channel(tim_channel, pyb.Timer.PWM, pin=pyb.Pin(tim_pin))
        q.en.pulse_width_percent(0)

#        MyMapperDict = { 'LeftMotorDir' : pyb.Pin.cpu.C12 }
#        pyb.Pin.dict(MyMapperDict)
#        g = pyb.Pin("LeftMotorDir", pyb.Pin.OUT_OD)


    def vel(q, vel=0):
        if vel < -100:
            vel = -100
        elif vel > 100:
            vel = 100

        if vel == 0:
            q.in1.value(0)
            q.in2.value(0)
#            q.dir_en = 0
        else:
#            q.dir_en = 1
            if vel > 0:
                q.in1.value(1)
                q.in2.value(0)
            elif vel < 0:
                q.in1.value(0)
                q.in2.value(1)
            if vel != q.velocity:
                q.en.pulse_width_percent(abs(vel))

#        print(vel, ' = ', q.name, ' velocity')
        q.velocity = vel

    def __str__(q):
        ls = ['DCm[', q.name, 
            '] in1,in2,tim,dir_en =[', 
            q.in1_pin, ',', q.in2_pin, ',', q.tim_pin, ',', q.dir_en, 
            ']=[', q.in1.value(), ',', q.in2.value(),'], vel=', q.velocity]
        return ''.join([str(a) for a in ls])


import pyb

import math

import shared_globals

#from shared_globals import move_arrow_pressed as move_arrow_pressed

from dcmotor import DCMotor

class DifDrive():
    def __init__(q):
        q.init_dcs()

    def init_dcs(q):
        
        q.dcms = []
        q.dc = {}
        # name, in1_pin, in2_pin, tim_num, tim_channel, tim_pin, dir_en=1, tim_freq=30000
        tim_strs = \
"""LF E0 E1 4 1 B6 1
RF E2 E3 4 2 B7 1
LB E0 E1 4 3 B8 0
RB E2 E3 4 4 B9 0"""
        for tim_str in tim_strs.split(';'):
            print(tim_str)
            tim_ls = tim_str.split()

            for i in [3,4,6]:
                tim_ls[i] = int(tim_ls[i])

            print(tim_ls)                
            dcm = DCMotor(*tim_ls)
            q.dcms.append(dcm)        
            q.dc[tim_ls[0]] = dcm
        print(len(q.dcms), 'motors initialized')


    def left_turn(q, value):
        q.dc['LF'].vel(value)
        q.dc['LB'].vel(value)

    def right_turn(q, value):
        q.dc['RF'].vel( value)
        q.dc['RB'].vel( value)

    def go_old(q, value, right=None):
        if right is None:
            left, right = value
        else:
            left = value
        q.left_turn(left)
        q.right_turn(right)


class MecDrive():
    def __init__(q):
        q.init_dcs()

    def init_dcs(q):
        q.dcms = []
        q.dc = {}
        # name, in1_pin, in2_pin, tim_num, tim_channel, tim_pin, dir_en=1, tim_freq=30000
 # rf lf rb lb       
        tim_strs = \
"""RF D7 D5 4 1 B6 1
LF D3 D1 4 2 B7 1
RB E0 E1 4 3 B8 1
LB E2 E3 4 4 B9 1"""
#E0 brown -> red D7 u front
        for tim_str in tim_strs.split('\n'):
            print(tim_str)
            tim_ls = tim_str.split()

            for i in [3,4,6]:
                tim_ls[i] = int(tim_ls[i])

            print(tim_ls)                
            dcm = DCMotor(*tim_ls)
            q.dcms.append(dcm)        
            q.dc[tim_ls[0]] = dcm
        print(len(q.dcms), 'motors initialized')

    def go(q, vels):
        # rf lf rb lb       
        for dc, vel in zip(q.dcms, vels):
            #if vel != 0:
            #    print(dc.name, vel)
            dc.vel(vel, info=True)
            #if vel != 0:
             #   print(dc)

    def stop(q):
        q.go([0, 0, 0, 0])


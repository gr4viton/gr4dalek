
import pyb

import math

import shared_globals

#from shared_globals import move_arrow_pressed as move_arrow_pressed

from dcmotor import DCMotor

class Drive(object):

    def __init__(q, drive_config):
        q.init_dcs(drive_config)

    def parse_drive_line(q, drive_line):
        ls = drive_line.split()
        for i in [3,4,6]:
            ls[i] = int(ls[i])
        keys = [
            'name', 'in1_pin', 'in2_pin', 'tim_num', 'tim_channel',
            'tim_pin', 'dir_en', 'tim_freq'
        ]
        drive_dict = {}
        for i_key, val in enumerate(ls):
            key = keys[i_key]
            drive_dict[key] = val

        return drive_dict

    def parse_config(q, drive_config_str):
        print('drive_conifg')
        print(drive_config_str)
        drive_lines = [
            drive_line.strip() for drive_line in drive_config_str.split('\n')
            if drive_line.strip()
        ]
        
        drive_config = []
        for drive_line in drive_lines:
            print(drive_line)
            drive_dict = q.parse_drive_line(drive_line)
            print(drive_dict)
            drive_config.append(drive_dict)

        return drive_config

    def init_dcs(q, drive_config):
        q.dcms = []
        q.dc = {}

        if isinstance(drive_config, dict):
            drive_config = drive_config
        elif isinstance(drive_config, str):
            drive_config = q.parse_config(drive_config)

        print(drive_config)                
            
        for drive_dict in drive_config:
            dcm = DCMotor(**drive_dict)
            q.dcms.append(dcm)        
            q.dc[drive_dict['name']] = dcm

        print(len(q.dcms), 'motors initialized')

    def go(q, vels):
        raise NotImplementedError('go must be implemented!')

    def stop(q):
        raise NotImplementedError('stop must be implemented!')


class DriveUnlinked(Drive):

    def __init__(q, drive_config):
        super().__init__(drive_config)

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

class DriveDifferential():

    def __init__(q):
        # rf lf rb lb       
        drive_config = """
            LF E0 E1 4 1 B6 1
            RF E2 E3 4 2 B7 1
            LB E0 E1 4 3 B8 0
            RB E2 E3 4 4 B9 0
        """
        # E0 brown -> red D7 u front
        super().__init__(drive_config)

    def left_turn(q, value):
        q.dc['LF'].vel(value)
        q.dc['LB'].vel(value)

    def right_turn(q, value):
        q.dc['RF'].vel( value)
        q.dc['RB'].vel( value)

    def go(q, value, right=None):
        if right is None:
            left, right = value
        else:
            left = value
        q.left_turn(left)
        q.right_turn(right)

    def stop(q):
        q.go([0, 0, 0, 0])

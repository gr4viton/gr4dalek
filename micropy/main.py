print('>>>>>>>>> STARTING MICROPYTHON ON STM32F4')
import pyb
from pyb import I2C, SPI

import staccel
import math

import os
#import gc # garbage collection for writing?

#import microsnake
from microsnake import MicroSnakeGame as Game
#from microsnake import move_arrow_pressed
import shared_globals

#from shared_globals import move_arrow_pressed as move_arrow_pressed

import lcd_i2c

import micropython
import boot
boot.print_version()

micropython.alloc_emergency_exception_buf(100)
print('Micropython alloc_emergency_exception_buffer set to 100')

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


#x = [0,1,2,3]
#move_arrow_pressed = None
#micropython
#microsnake.move_arrow_pressed = move_arrow_pressed

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
        for dc, vel in zip(q.dcms, vels):
            #if vel != 0:
            #    print(dc.name, vel)
            dc.vel(vel*0.8)

class State():
    def __init__(q, btns_state, vels, name):
        q.btns_state = btns_state 
        q.vels = vels
        q.name = name

class ButtonControl():
    state = None
    def __init__(q):
        
#r d l u
        states_str = \
"""0 0 0 0 0 0 0 0 idle
0 0 0 1 100 100 100 100 front
0 0 1 0 -100 100 -100 100 turn_left
0 1 0 0 -100 -100 -100 -100 reverse 
1 0 0 0 100 -100 100 -100 turn_right
0 0 1 1 100 -100 -100 100 go_left
1 0 0 1 -100 100 100 -100 go_right"""

#r d l u
        states_str_test = \
"""0 0 0 0 0 0 0 0 idle
0 0 0 1 100 0 0 0 RF
0 0 1 0 0 0 100 0 RB
0 1 0 0 0 100 0 0 LF
1 0 0 0 0 0 0 100 LB"""

 #       states_str = states_str_test
        states_list = states_str.split('\n')

        q.states = []
        for state_str in states_list:
            btns_state = []
            vels = []

            state_list = state_str.split()

            for i in range(4):
                btns_state.append(int(state_list[i])==1)
            for i in [4,5,6,7]:
                vels.append(float(state_list[i]))

            name = state_list[-1]

            state = State(btns_state, vels, name)
            print('state', btns_state, vels, name)
            q.states.append(state)
        
        q.state = q.states[0]

    def querry_state(q):
        q.btns_pressed = shared_globals.btns_pressed
        for state in q.states:
            if state.btns_state == q.btns_pressed:
#                print(state.btns_state, '?=', q.btns_pressed)                
                if q.state != state:
                    q.state = state                
                    return state, q.state
        return None

                    



class Machine():
    n = 0
    leds = None
#    move_arrow_pressed = None

    def on_press(q):
        print('pressed!')
#        print('Machine.turned', Machine.turned)
        act = pyb.millis()
        if (act - Machine.turn_time) > Machine.turn_delay:
            Machine.turned = True
            Machine.turn_time = act
        print('Machine.turned', Machine.turned)
        
        # print(q.ac.xyz()) # MemoryError:


    def on_tim4(q):
        #lambda t:pyb.LED(3).toggle()
        try:
            n = Machine.n        
            n = (n + 2) % 2
    
            Machine.leds[n].toggle()
            Machine.n = n
        except TypeError as ex:
            #print(ex.strerror)
            print('error')
    
    
    def __init__(q):
#        q.show_gpio()

        q.init_spi()

        q.init_buttons()
        q.init_control()

        q.init_leds()

        q.init_DCs()
 #       q.init_lcd()

        q.main_loop()
        
    def init_DCs(q):
        q.dd = MecDrive()

    def init_spi(q):
        print('spi initialization')
        q.spi = SPI(2, SPI.SLAVE, baudrate=60000, polarity=1, phase=0, crc=0x7)
        q.spi.init(mode=SPI.SLAVE)
        byte_count = 4
        q.byte_format = 'utf-8'
        write_buf = bytearray(byte_count) 
        read_buf = bytearray(byte_count) 
        print('spi loop started', write_buf)
        old_read_buf = bytearray(byte_count)
        while True:
            q.spi.write_readinto(write_buf, read_buf)
            same = sum([1 for B1, B2 in zip(read_buf, old_read_buf) if B1 == B2])
            if same <  byte_count:
                #read = [byte.decode(q.byte_format) for byte in read_buf]
                
#                [print(B1, B2) for B1, B2 in zip(read_buf, old_read_buf)]
                read = read_buf.decode(q.byte_format)
                print('sent', write_buf)
                print('got', read)
            old_read_buf = [B for B in read_buf]
            pyb.delay(100)
        pass       


    def init_control(q):
        q.control = ButtonControl()

    def clear_lcds(q):
        for lcd in q.lcds:
            lcd.clear()

    def state_changed(q, old_state, state):
        print(state.name, "= current state")     
        if state.name != 'idle':
            print('state_vels =', state.vels)
            for dc in q.dd.dcms:
                print(dc)

    def main_loop(q):
        a = 0

        v = 0
        vmin, vmax = 0, 4
        vstep = 1
        st = [[100, 0], [0, 100], [100, 100]]
        vmax = len(st)
        #vmin, vmax = -62, 62
        state = None
        while(1):
            a += 1

#            r,d,l,u = q.btns_pressed
            change = q.control.querry_state()
            state = q.control.state
                
 #           print(state.vels)
 


            if change is not None:
                q.dd.go(state.vels)
                q.state_changed(*change)

            if a % 500000 == 0:        
                pass
                print(state.name, "= current state")            

            if a == 1000000:
                print(str(a) + 'cycles')
                q.leds[0].toggle()
                a = 0
            pass

        #pyb.wfi() # https://docs.micropython.org/en/latest/pyboard/library/pyb.html
        #pyb.standby()
        pyb.info()

    def init_leds(q):
        q.leds = []
        for i in range(4):
            q.leds.append(pyb.LED(i+1))

    def init_buttons(q):
        
        sw = pyb.Switch()
        sw.callback(q.on_press)
        
        # sw.callback(lambda:print('press!'))
        pins = ['A' + str(i) for i in range(1, 8, 2)]
#        pins = ['D' + str(i) for i in range(0, 7, 2)]
#        pins = ['A7']

        print('Initializing buttons:', pins)

#        q.on_btn_press = {}
        q.btn_extints = []
        q.btns = []
        b_callbacks = []

        mapper = range(len(pins))
#        bs.append(lambda x: print(mapper[0], ': line', x))
#        bs.append(lambda x: print(mapper[1], ': line', x))
#        bs.append(lambda x: print(mapper[2], ': line', x))
#        bs.append(lambda x: print(mapper[3], ': line', x))  

        def on_arrow_button(mapped, line):
            shared_globals.move_arrow_pressed = mapped
#            shared_globals.btns[mapped] = True
            value = q.btns[mapped].value()
            shared_globals.btns_pressed[mapped] = value == 0

            #print('on_arrow_button=', mapped)
            print('btns (RDLU):', shared_globals.btns_pressed)
#            print('mapped var', mapped, ': line', line)

        # must not use for-loop (would be optimised out!)
        b_callbacks.append(lambda x: on_arrow_button(mapper[0], x))
        b_callbacks.append(lambda x: on_arrow_button(mapper[1], x))
        b_callbacks.append(lambda x: on_arrow_button(mapper[2], x))
        b_callbacks.append(lambda x: on_arrow_button(mapper[3], x))


        for i, pin_id in enumerate(pins):

            new_callback = b_callbacks[i]

            btn = pyb.Pin(pin_id)

            btn_exting = pyb.ExtInt(pin_id, pyb.ExtInt.IRQ_RISING_FALLING, 
                    pyb.Pin.PULL_UP, new_callback)

            q.btn_extints.append(btn_exting)
            q.btns.append(btn)

        shared_globals.btns_pressed = [False, False, False, False]        

    def init_i2c(q, bus=2, role=I2C.MASTER, baudrate=115200, self_addr=0x42):
        q.i2c = I2C(bus)

        q.addr = self_addr
        q.br = baudrate
        q.i2c.init(role, addr=q.addr, baudrate=q.br)          
                
        print('I2C initialized: self_addr=0x{0:02X} = {0} dec, br={1}'.\
                format(q.addr, q.br))

    def char_range(q, c1, c2):
        """Generates the characters from `c1` to `c2`, inclusive."""
        for c in range(ord(c1), ord(c2)+1):
            yield chr(c)

    def init_lcd(q):

        q.init_i2c()

        scan = q.i2c.scan()
        print('Scanned addresses [dec]:', scan)

        lcd_as = scan
        q.lcds = []
#        q.lcds = [ for as in lcd_as]
        for lcd_a in lcd_as:
            new_lcd = lcd_i2c.lcd1602(q.i2c, lcd_a)
            q.lcds.append(new_lcd)
        

        for i, lcd in enumerate(q.lcds):
            txt = 'Loading...lcd[{}]'.format(i)
            lcd.disp(txt, 0)

        for i, ch in enumerate(q.char_range('a', 'Z')):
            lcd_num = i % len(q.lcds)
            lcd = q.lcds[lcd_num]
            txt = 'lcd[{}] = {}'.format(lcd_num, ch)
            lcd.disp(txt, 0)
            pyb.delay(300)
        
        q.lcd_a = scan[0]
        print('i2c initialization ended.')

    def show_gpio(q):

        print('>> dir(pyb.Pin.board)', dir(pyb.Pin.board))
        print('>> dir(pyb.Pin.cpu)', dir(pyb.Pin.cpu))
        
        try:
            print('>> pins.pins()')
            pins.pins()
            print('>> pins.af()')
            pins.af()
        except:
            print('pins not imported')


    def init_accel(q):
        
        q.ac = staccel.STAccel()
        ac = q.ac


        #from pyb import Accel

        #accel = pyb.Accel()



def run():
    m = Machine()
    print('End of machine program!')

if __name__ == '__main__':
    run()

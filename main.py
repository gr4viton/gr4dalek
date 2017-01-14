print('>>>>>>>>> STARTING MICROPYTHON ON STM32F4')
import pyb
from pyb import I2C 

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
micropython.alloc_emergency_exception_buf(100)

#import operator # dict sorting



try: 
    print('try importing pins')
    import pins
except ImportError:
    print('pins not found')

#from machine import Pins



#print('>>>>>>> shape assert')
#a = [[[1,2],[1,2]],[[1,2],[1,2]]]
#print(shared_globals.print_shape(a))


#x = [0,1,2,3]
#move_arrow_pressed = None
#micropython
#microsnake.move_arrow_pressed = move_arrow_pressed
class DCMotor():
    def __init__(q):
        q.velocity = 0
        q.in1 = pyb.Pin('C9', pyb.Pin.OUT_PP)
        q.in2 = pyb.Pin('C8', pyb.Pin.OUT_PP)

        tim3 = pyb.Timer(3)
        tim3.init(freq=100)        
        q.en = tim3.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PC7)
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
        else:
            if vel > 0:
                q.in1.value(1)
                q.in2.value(0)
            elif vel < 0:
                q.in1.value(0)
                q.in2.value(1)
            q.en.pulse_width_percent(abs(vel))
        print('velocity set to', vel)
        q.velocity = vel

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
        q.init_buttons()
        q.init_leds()
        q.init_DCs()

 #       q.init_lcd()

        q.main_loop()

    def init_DCs(q):
        q.dcs = []

#        q.dcs.append(
        dcm = DCMotor()
        q.dcs.append(dcm)

        q.dcm = dcm

    def clear_lcds(q):
        for lcd in q.lcds:
            lcd.clear()

    def main_loop(q):
        a = 0
        vel = 0
        vstep = 1
        while(1):
            a += 1

            if a % 10000 == 0:
                #q.demo_lcd()
                vel = (vel+vstep) % 200
                if vel == 199:
                    vstep = -vstep
                if vel == 0:
                    vstep = -vstep
                q.dcm.vel(vel-100)
                pass
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

        q.on_btn_press = {}
        q.btns = []

        bs = []
        mapper = range(len(pins))
#        bs.append(lambda x: print(mapper[0], ': line', x))
#        bs.append(lambda x: print(mapper[1], ': line', x))
#        bs.append(lambda x: print(mapper[2], ': line', x))
#        bs.append(lambda x: print(mapper[3], ': line', x))  

        def on_arrow_button(mapped, line):
            shared_globals.move_arrow_pressed = mapped
            print('on_arrow_button=', mapped)
#            print('mapped var', mapped, ': line', line)

        # must not use for cycle (would be optimised out!)
        bs.append(lambda x: on_arrow_button(mapper[0], x))
        bs.append(lambda x: on_arrow_button(mapper[1], x))
        bs.append(lambda x: on_arrow_button(mapper[2], x))
        bs.append(lambda x: on_arrow_button(mapper[3], x))


        for i, pin_id in enumerate(pins):

            new_callback = bs[i]
            new_btn = pyb.ExtInt(pin_id, pyb.ExtInt.IRQ_FALLING, 
                    pyb.Pin.PULL_UP, new_callback)

            q.btns.append(new_btn)
        

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




if __name__ == '__main__':
    m = Machine()
    print('End of machine program!')


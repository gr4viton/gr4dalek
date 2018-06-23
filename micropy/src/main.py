print('>>>>>>>>> STARTING MICROPYTHON ON STM32F4')
import pyb
from pyb import I2C, SPI, UART

import staccel
import math
from math import sin, cos, radians, degrees

import os
#import gc # garbage collection for writing?

#import microsnake
#from microsnake import MicroSnakeGame as Game
#from microsnake import move_arrow_pressed

import shared_globals

#from shared_globals import move_arrow_pressed as move_arrow_pressed

from struct import unpack, pack # not interrupt safe = using heap
import binascii as ba

#import lcd_i2c

from robot_drives import DriveUnlinked
from btn_control import ButtonControl

from state import State

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

from actions import Actions as Act


class GamepadControl():

    #github.com/piborg/zeroborg/blob/master/zbMecanumJoy.py
    def __init__(q):
        # from right strick
        q.strafe_stick_vals = [0,0,0]
        # from left stick horizontal

        q.rot = 0
        # from left stick vertical

        q.slow_factor = 0.5
        q.slow = False
        q.speed_rot_stick_vals = [0,0,0]

        q.vel_min = 0.05
        q.vel_max = 1
        q.rot_min = 0.05
        q.max_pwr, q.min_pwr = 100, 60
        q.maxmin_pwr = q.max_pwr - q.min_pwr
        print('max, min, maxmin = ', q.max_pwr, q.min_pwr, q.maxmin_pwr)
        q.vels = [0,0,0,0]

    def calc_vels(q):
        """Mecanum wheel calculation."""
        *q.vels, q.vel_angle = q.strafe_stick_vals
        rot_val, speed_val, _ = q.speed_rot_stick_vals
        print(rot_val)
        q.rot = rot_val * math.pi / 10

        q.speed_factor = (abs(speed_val) + 1)/2

        print('slow', q.slow)
        print('speed_factor', q.speed_factor)
        print('vel_min', q.vel_min)

        for vel in q.vels:
            if vel < q.vel_min:
                vel = 0
        if q.rot < q.rot_min:
            q.rot = 0


        # q.vels = [-q.vels[0], +q.vels[1]]

        q.rot = radians(10)
        q.rot = radians(0)

        strafe_speed = math.sqrt(sum([vel**2 for vel in q.vels]))
        print('strafe_speed', strafe_speed)
        # Determine the four drive power levelsa

        # offset_angle
        q.vel_angle = radians(q.vel_angle)
        angle = q.vel_angle + math.pi/4

        print('angle', degrees(angle))

        # FR FL BR BL = vels
        gons = [cos, sin, sin, cos]
        facs = [1, -1, -1, 1]
        q.vels = [
            strafe_speed * gon(angle) + fac * q.rot
            for fac, gon in zip(facs, gons)
        ]
        print('vels', q.vels)

        # Scale the drive power if any exceed 100%
        max_scale = max([abs(vel) for vel in q.vels])
        print('max_scale', max_scale)
        if max_scale > 1.0:
            q.vels = [
                vel * q.speed_factor / max_scale
                for vel in q.vels
            ]

        if q.slow:
            q.vels = [vel * q.slow_factor for vel in q.vels]

        q.vels = [
            ((abs(vel) - q.vel_min) * q.maxmin_pwr + q.min_pwr)
            * math.copysign(1, vel) * int(vel != 0)
            for vel in q.vels
        ]
        print('vels final', q.vels)


    def __str__(q):
        mot_names = 'FR FL BR BL'.split()
        lst = ['Mecanum wheel actual control state:\n']
        [ lst.extend(['|', mot_names[i], '= ', round(q.vels[i], 2), '\n'])
                            for i in range(4)]
        return ''.join([str(i) for i in lst])


    def process_stick_cmd(q, cmd):
        q.cmd = cmd
        print('got cmd', cmd)
        input_type, str_vals = cmd.split(Act.gamepad_input_del)
        vals = [float(val) for val in str_vals.split(Act.num_del)]


        if Act.strafe_stick in input_type:
            q.strafe_stick_vals = vals
        elif Act.speed_rot_stick in input_type:
            q.speed_rot_stick_vals = vals


        q.calc_vels()
        print(q)
        #q.drive.go(q.wheel_vels)


class Machine():
    n = 0
    leds = None
#    move_arrow_pressed = None
    turn_delay = 10
    turn_time = pyb.millis()
    turned = None
    actions = {
        Act.gamepad: True,
        Act.motor_control: False,
        Act.motor_slow: False,
    }

    def on_press(q):
        print('pressed!')
#        print('Machine.turned', Machine.turned)
        act = pyb.millis()

        prev = Machine.turn_time
        if (act - prev) > Machine.turn_delay:
            Machine.turned = True
            Machine.turn_time = act
        print('Machine.turned', Machine.turned)
        q.send_ack()
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

    def check_pwm(q):
        tim_num = 4
        pin = 'B6'
        ch = 1
        freq = 1000

        tim = pyb.Timer(tim_num)
        tim.init(freq=freq)
        tpin = pyb.Pin(pin)
        tim.channel(ch, pyb.timer.PWM, pin=tpin)
        tim.pulse_width_percent(50)

    def __init__(q):
        q.leds = None

        # rf lf rb lb
        # nam in1, in2, tim_num, tim_ch, tim_pin, dir_en
        drive_config = """
            RF D7 D5 4 1 B6 1
            LF D3 D1 4 2 B7 1
            RB E0 E1 4 3 B8 1
            LB E2 E3 4 4 B9 1
        """

        drive_config = """
            RF D1 D7 3 1 B4 1
            LF D5 D3 3 2 B5 1
            RB E0 E1 3 3 B0 1
            LB E2 E3 3 4 B1 1
        """

        q.check_pwm()

        # D5 D7, D3 D1 - makes the problem reverse - not turning when going both straight or both back

        # E0 brown -> red D7 u front
        q.drive_config = drive_config

        q.actions[Act.motor_control] = False

#        q.show_gpio()
#        q.init_spi()
 #       q.init_lcd()

       # q.init_leds()
        q.init_uart()

      #  q.init_buttons()
        q.init_control()

        q.init_DCs()

        q.main_loop()


    def init_DCs(q):

        q.drive = DriveUnlinked(q.drive_config)


    def init_spi(q):
        print('spi initialization')
        q.spi = SPI(2, SPI.SLAVE, baudrate=500000, polarity=0, phase=0, firstbit=SPI.LSB, crc=None) #0x7)
        q.spi.init(mode=SPI.SLAVE)
        q.byte_count = 1
        q.byte_format = 'utf-8'
        q.pack_format = '<b'

        q.read_buf = bytearray(q.byte_count)
        q.i = 0
        q.old_read_buf = bytearray(q.byte_count)

        print('Initializing SPI chip select')
        pin_CS_id = 'B12'
        callback = q.on_spi_CS
        q.pin_CS = pyb.Pin(pin_CS_id)
#        pyb.ExtInt(pin_CS_id, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, callback)
#        pyb.ExtInt(pin_CS_id, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback)
        pyb.ExtInt(pin_CS_id, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_UP, callback)
        q.rr = list(range(q.byte_count))
        q.ww = list(range(q.byte_count))

        return

    def hexint(q, b):
        return int(ba.hexlify(b), 16)

    def on_spi_CS(q, line):
        print('on_spi_CS')
        try:
            q.spi.readinto(q.read_buf)
            i=0
            while i<q.byte_count:
                q.rr[i] = int(q.read_buf[i] >> 1)
                i+=1
            print('buffer read = ', q.rr, q.read_buf, sep='\t')
            q.leds[3].toggle()
        except Exception as e:
            print('something wrong happened', e)



    def init_control(q):
        q.control = ButtonControl()
        q.jcontrol = GamepadControl()


    def clear_lcds(q):
        for lcd in q.lcds:
            lcd.clear()

    def state_changed(q, old_state, state):
        print(state.name, "= current state")
        if state.name != 'idle':
            print('state_vels =', state.vels)
            for dc in q.drive.dcms:
                print(dc)

    def init_uart(q):
        """
        [TX RX], [TX RX]
        USART 6 = PC6 PC7 ?
        """
        q.baud = 115200
        q.uart = UART(6, q.baud)
        q.uart.deinit()
        q.uart.init(q.baud, bits=8, parity=None, stop=1,
                read_buf_len=100, flow=0, timeout=10 )
        q.buf = []

    def send_ack(q):
        q.uart.write(Act.ok)
        print('sent ACK!')

    def send_nack(q):
        q.uart.write(Act.nok)
        print('sent NACK!')

    def uart_process(q, print_got_char=False):
        #print(q.uart)

        parity_check = False
        q.cmd = None
        new_command = False
        while q.uart.any() and not new_command:
            c = chr(q.uart.readchar())
            if print_got_char:
                print('got char', c)
            if parity_check != True:
                if c == Act.cmd_end:
                    q.cmd = ''.join(q.buf)
 #                   print('>>! got some cmd', q.cmd)
                    q.buf = []
                    parity_check = True
                else:
                    q.buf.append(c)
            else:
                packet = q.cmd
                checksum = 0
                for el in packet:
                    checksum ^= ord(el)
                #print('calculated parity =', checksum)
                #print('got parity', ord(c))
                if ord(c) == checksum:
                    #print('>>> parity good')
                    print('>>> got full cmd', q.cmd)
                    new_command = True
                    q.send_ack()
                else:
                    print('bad parity!')
                    q.send_nack()
                    q.cmd = None

    def set_action_state(q, action_key, state):
        q.actions[action_key] = state
        print('{act} initialized to {state}'.format(
            act=action_key, state=state
        ))
        print(q.actions)

    def cmd_process(q):
        if q.cmd:

            action = None
            if Act.turn_on in q.cmd:
                print('turn on cmd')
                action = True
            elif Act.turn_off in q.cmd:
                print('turn off cmd')
                action = False

            if action is not None:
                found = False
                for action_key in q.actions.keys():
                    if action_key in q.cmd:
                        q.set_action_state(action_key, action)
                        found = True
                #if not q.actions[Act.motor_control]:
                    #print('Stopped motors, cause motor_control is off.')
 #                   q.drive.stop()

                if not found:
                    print('No known action found for action_key = {act}'.format(
                        act=q.cmd))

            else:
                if q.actions[Act.gamepad]:
                    q.jcontrol.process_stick_cmd(q.cmd)
                    q.jcontrol.slow = q.actions[Act.motor_slow]


    def main_loop(q):
        a = 0

        vstep = 1
        state = None
        q.send_ack()
        while True:
            a += 1

            # gpio button control
#            r,d,l,u = q.btns_pressed

            change = q.control.querry_state()
            state = q.control.state
            if change is not None:
                #if q.motor_control:
                #    q.drive.go(state.vels)
                q.state_changed(*change)

            # gamepad stick control
            q.uart_process()
            q.cmd_process()
            if q.actions[Act.motor_control]:
                q.drive.go(q.jcontrol.vels)

            if a % 500000 == 0:
                pass
                print(state.name, "= current state")

            if a == 1000000:
                print(str(a) + 'cycles')
                if q.leds:
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

        # late closures
        # http://docs.python-guide.org/en/latest/writing/gotchas/#late-binding-closures
        if False:
            b_callbacks = [
                lambda x, i=i: on_arrow_button(mapper[i], x)
                for i in range(4)
            ]

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

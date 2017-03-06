# main.py -- put your code here!
import pyb
from pyb import I2C 

try: 
    import pins
except: ImportError:
    print('pins not found')

import staccel
import math

#from machine import Pins
class m():
    def __init__(self):
        self.init_servo()

    def init_servo(self):
        tim4 = pyb.Timer(4)
        #tim4.callback(self.on_press)
        tim4.init(freq=10)
        t4ch4 = tim4.channel(4, pyb.Timer.PWM, pin=pyb.Pin.board.LED_BLUE, pulse_width=420000)
#        ch2 = tim.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X2, pulse_width=210000)
 #       ch3 = tim.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3, pulse_width=420000)
        #s1 = pyb.Servo(1)

        # servo
        t1 = pyb.Timer(1)        
        prc = 50
        serv = t1.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PE9, pulse_width=42)
#                           pulse_width_percent=prc)
        t1.init(freq=1000)
        #t1.init(prescaler=83, period=999)
        
        
        # buzzer
        tim3 = pyb.Timer(3)
        tim3.init(freq=1000)        
        #t3ch1 = tim3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PC6, pulse_width=420000)
        #t3ch1.pulse_width_percent(50)
        
        t3ch2 = tim3.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PC7, pulse_width=420000)
        t3ch2.pulse_width_percent(50)
        

        Machine.leds = [pyb.LED(i) for i in range(1,5)]



        #led = pyb.P
        a = 0
        duty = 0
        
        sduty_min = 40
        sduty_max = 77
        sduty = sduty_min
        
        
        sum_ones = 1
        sum_zeros = 1
        
        last_was_one = False
        calc_duty = 0
        while True:
            
            if pyb.Pin.board.PC6 == 0:
                print(pyb.Pin.board.PC6)
                if last_was_one == True:
                    calc_duty = sum_ones / (sum_zeros + sum_ones)
                    sum_zeros = 1
                    sum_ones = 0                    
                last_was_one = False
                sum_zeros += 1
            else:
                sum_ones += 1
                last_was_one = True

            #if a<50:
            duty = abs(100*ac.x())
            t4ch4.pulse_width_percent(duty)
            
            #sduty = abs(ac.x()) * 0.24 + 0.05
            #sduty = int(sduty*100000)
            serv.pulse_width_percent(sduty)
            #serv.pulse_width(int(sduty))
            
            #t3ch1.pulse_width_percent(duty)
            freq = duty * 100 + 1000
            freq = 50
            tim3.freq(freq)
            
            #sduty = duty
            #sduty = sduty*1000
            sduty = sduty+1
            if sduty > sduty_max:
                sduty = sduty_min
            #sduty = duty
            t3ch2.pulse_width_percent(sduty)
            
            pyb.Pin
            #pyb.delay(1)
            if a < 1000:
                a += 1
            else:
                a = 0
                print([ac.x(), ac.y(), ac.z()], '= acc', ) 
                #print(tim)
                print('{}% duty cycle'.format(duty))
                print('{} freq'.format(freq))
                print('{} sduty cycle'.format(sduty))
                print('{} calculated duty cycle'.format(calc_duty))
                #print(pyb.millis())#
                #pyb.delay(50)
                



def servos_functional():
    tim3 = pyb.Timer(3)
    tim3.init(freq=50)        
    
    t3ch2 = tim3.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PC7, pulse_width=420000)
    button = pyb.Switch()
    
    ac = staccel.STAccel()
    
    
    serv_type = -1
    last_a = a = cur_a = 0
    last_a = [0,0,0,0,0]
    w = 0.5
    
    x = 0
    min_x = 0
    max_x = 100
    inc = 0.5
    
    min_d = 1/20*100 
    max_d = 2/20*100
    
    tower_pro = (2.5, 13.5)
    tower_pro_bright = (5, 10)
    
    min_d, max_d = tower_pro_bright 
    maxmin_d = max_d - min_d
    while True:
#        x += 1
        x += inc
        if x>max_x:
            #x = min_x
            inc *= -1
        elif x<min_x:
            #x = max_x
            inc *= -1
            
        
        print('1')

        cur_a = (ac.x() + 1) / 2 *100
        w = abs(ac.y())
#        a = (w) * cur_a + (1-w) * last_a
#        last_a = cur_a
        
        last_a = last_a[1:]  + [cur_a]
        ln = len(last_a)
        le = (ln + 1)*2
        w = (2*ln-1)/le
        
        
        a = w * cur_a
        for l in last_a:
            a += l/le
        
        if button():
            serv_type *= -1
            
        if serv_type == 1:
            duty_var = x
        else:
            duty_var = a
        
        duty = min_d + (duty_var/100) * maxmin_d
        t3ch2.pulse_width_percent(duty)
        pyb.delay(5)
        print('x={}, duty = {}, w = {}'.format(x, duty, w))
    
    pass

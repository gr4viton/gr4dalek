
import wiringpi as wp


class Stm2Rpi():
    num_del = '_'
    cmd_end = '\n'
    gamepad_input_del = ':'
    speed_rot_stick = 'R'
    strafe_stick = 'L'
    
    turn_on = '>>>'
    turn_off = '<<<'
    gamepad='J'

    ok='ok'
    nok='KO'

class StmCom():
    def __init__(self):
        self.init_uart()

    def init_uart(self):

        self.ch_end = '\n'

        self.uart = wp.serialOpen('/dev/ttyAMA0', 115200)
        self.CTS = True
        
        self.send_str('>>>>>J')

        print(str(dir(wp)).replace(' ', '\n'))
    
    def on_exit(self):
        wp.serialClose(self.uart)

    def init_spi(self):
#            https://projects.drogon.net/raspberry-pi/wiringpi/pins/
        wp.wiringPiSetup()

        self.SPIchannel = 1 #SPI Channel (CE1)
        SPIspeed = 500000 #Clock Speed in Hz
        spi_mode = 0 # cpol 0, cpha 0, cedg 1

        ret = wp.wiringPiSPISetupMode(self.SPIchannel, SPIspeed, spi_mode)
        if ret == -1:
            print('SPI setup returned error')
            return
        print('>> SPI initialized')
        ret = wp.wiringPiSPIGetFd(self.SPIchannel)
        print('spi file-descriptor', ret)

        print('starting spi loop')
        i=0
        while True:
        
            self.write_pot(i)
            time.sleep(1)
            i += 1

    def write_pot_spi(self, input):
        """ Split an integer input into a two byte array to send via SPI
        """
        
        data = input
        try:
            ret = wp.wiringPiSPIDataRW(self.SPIchannel, 'a')
        except e:
            print('error')
            print(e)
        print('got returned')
        print('returned data', data)


    def send_str(self, data):
        self.get_ack()
        if self.CTS == False:
            print('not send - ack not got yet')
            return

        checksum = 0
        for ch in data:
            checksum ^= ord(ch)
                
        print('checksum', checksum, 'for str', data)
        data = data + self.ch_end + chr(checksum)

        
        wp.serialPuts(self.uart, data)
        #wp.serialFlush(self.uart)
        print('sent data', data.encode())
        self.CTS = False

        self.get_ack()

    
    def get_ack(self):
        buf = []
        while not self.CTS:
            while wp.serialDataAvail(self.uart):
                c = chr(wp.serialGetchar(self.uart))
                buf.append(c)
                str_buf = ''.join(buf)
                print('buf', str_buf.encode())
                if Stm2Rpi.ok in str_buf:
                    self.CTS = True
                    print('got ACK')
                    #wp.serialFlush(self.uart)
                elif Stm2Rpi.nok in str_buf:
                    self.CTS = True
                    print('got NACK')


    def write_pot_uart(self, name, fdata):
        
        abrev = name[0].upper() + Stm2Rpi.gamepad_input_del 
        data = abrev + Stm2Rpi.num_del.join([ str(round(val, 3)) for val in fdata])

        self.send_str(data)


    
    

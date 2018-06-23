#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import wiringpi as wp

from actions import Actions as Act


class StmCom():
    def __init__(self):
        self.init_uart()

    def init_uart(self):

        self.ch_end = '\n'

        rpi_ver = 3
        i_ser = 1 if rpi_ver == 3 else 0
        ser_path = ['/dev/ttyAMA0', '/dev/ttyS0'][i_ser]

        ret = wp.serialOpen(ser_path, 115200)
        if ret == -1:
            print('UART setup returned error')
            return
        else:
            self.uart = ret
            print('UART init with id = {id_}'.format(id_=ret))
        self.CTS = True

        self.start(Act.gamepad)

        # [print(a) for a in dir(wp)]

    def start(self, cmd):
        self.cmd(cmd, True)

    def stop(self, cmd):
        self.cmd(cmd, False)

    def cmd(self, cmd, enable=True):
        if enable:
            action = Act.turn_on
        else:
            action = Act.turn_off
        data = '{act} {cmd}'.format(act=action, cmd=cmd)
        self.send_cmd(data)

    def on_exit(self, uart=None):
        if uart is None:
            uart = self.uart
        wp.serialClose(uart)

    def init_spi(self):
        """he here: https://projects.drogon.net/raspberry-pi/wiringpi/pins/ ."""
        wp.wiringPiSetup()

        self.SPIchannel = 1  # SPI Channel (CE1)
        SPIspeed = 500000  # Clock Speed in Hz
        spi_mode = 0  # cpol 0, cpha 0, cedg 1

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
        except Exception as ex:
            print('error')
            print(ex)
            print(ret)
        print('got returned')
        print('returned data', data)

    def send_cmd(self, data):

        print('>>> Serial send str: {cmd}'.format(cmd=data))
        self.get_ack()

        if self.CTS is False:
            print('not send - ack not got yet')
            return

        checksum = 0
        for ch in data:
            checksum ^= ord(ch)

        print('> checksum = {ch}'.format(ch=checksum))
        data = data + self.ch_end + chr(checksum)

        self.send_data(data)

        self.get_ack()

    def send_data(self, data):
        wp.serialPuts(self.uart, data)
        # wp.serialFlush(self.uart)
        print('> sent data = {dat}'.format(dat=data.encode()))
        self.CTS = False

    @property
    def data_avail(self):
        return wp.serialDataAvail(self.uart)

    def get_ack(self):
        buf = []
        while not self.CTS:
            while self.data_avail:

                cdata = wp.serialGetchar(self.uart)

                print('> got = {cdata}'.format(cdata=cdata))

                c = chr(cdata)
                buf.append(c)
                str_buf = ''.join(buf)
                print('> in buf = ', str_buf.encode())

                if Act.ok in str_buf:
                    self.CTS = True
                    print('got ACK')
                    # wp.serialFlush(self.uart)
                elif Act.nok in str_buf:
                    self.CTS = True
                    print('got NACK')

    def write_pot_uart(self, name, fdata):

        abrev = name[0].upper() + Act.gamepad_input_del
        vals = [str(round(float(val), 3)) for val in fdata]
        data = abrev + Act.num_del.join(vals)

        self.send_cmd(data)

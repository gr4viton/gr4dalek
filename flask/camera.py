#!/usr/bin/python
import sys
import os

class Camera():
    def __init__(self):
        self.stream_path = '/home/pi/stream/out.jpg'
        self.default_img_path = '/home/pi/stream/default.jpg'

        self.default_frame = open(self.default_img_path, 'rb').read()
        self.frame = self.default_frame

        self.stream_dir = '/home/pi/stream/'

        self.fifo_buff = self.stream_dir + 'jpg'
        self.server_waits = self.stream_dir + 'server_waits'
        self.client_wants = self.stream_dir + 'client_wants'

    def get_frame(self):
        if os.path.exists(self.fifo_buff):
            self.frame = open(self.fifo_buff, 'rb', 0).read()
        return self.frame
        
    def get_frame_locking(self):
        client_wants = os.path.exists(self.client_wants)
        server_waits = os.path.exists(self.server_waits)
        if not server_waits:
            if not client_wants:
                os.mkfifo(self.client_wants)
        else: 
            # server waits
            if os.path.exists(self.fifo_buff):
                self.frame = open(self.fifo_buff, 'rb', 0).read()
                if client_wants:
                    os.remove(self.client_wants)
                if server_waits:
                    os.remove(self.server_waits)
            else:
                pass
        return self.frame

    def get_frame_disk(self):
        new = open(self.stream_path, 'rb').read()
        if new is None:
            return self.default_frame
        else:
            self.frame = new
            return self.frame



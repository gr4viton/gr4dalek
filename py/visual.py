import cv2

import numpy as np
import time

from StepEnum import DataDictParameterNames as dd
import os

global almanach
almanach = None

class CameraControl():

    def __init__(self, id):
        self.id = id
        self.frame = None

        self.open()
        self.close()
            
        self.fps = 0
        self.frame_count = 0

        db = { dd.resolution: (640,480) }

        #self.db = DataBlock(db)
        self.db = dict(db)

    def open(self):
        self.cap = cv2.VideoCapture(self.id)
        # warmup camera
        time.sleep(0.1)

        if self.cap.isOpened():
            print('Camera id ', self.id, ' opened!')
        else:
            print('Camera id ', self.id, ' can not be opened!')


    def open_ifnot(self):
        if not self.cap.isOpened():
            self.open()

    def close(self):
        self.cap.release()
        if not self.cap.isOpened():
            print('Capture id ', self.id, ' closed!')
        else:
            print('Capture id ', self.id, ' could not be closed!')

    def get_frame(self):
        self.open_ifnot()

        ret, frame = self.cap.read()
        self.frame = frame
        
        while not True:
            ret, frame = self.cap.read()
            print(frame.shape)

        if ret:
            self.frame_count += 1
            print('Camera id ', self.id, ' captured frame ', 
                self.frame_count) #, self.frame.shape)
        else:
            print('Camera id ', self.id, ' capture failed')
            #self.db[dd.stop_it] = 'capture failed'
            self.close()
            time.sleep(1)
        return frame


class VisualChain():
    delimiter = ','

    def __init__(self, str_steplist):
        self.create_steplist(str_steplist)
        self.db = dict()
        self.__init_ipc__()

    def __init_ipc__(self):

        self.stream_dir = '/home/pi/stream/'

        self.fifo_buff = self.stream_dir + 'jpg'
        self.server_waits = self.stream_dir + 'server_waits'
        self.client_wants = self.stream_dir + 'client_wants'

        self.db[dd.fifo_buff] = self.fifo_buff
        self.db[dd.fifo_free_suffix] = 0


    def create_steplist(self, str_steplist):
        """ Creates visual steps list
        """
        global almanach
        step_strs = str_steplist.split(VisualChain.delimiter)
        step_strs = [step_str.strip() for step_str in step_strs]
        self.steps = [ almanach[step_str] 
                for step_str in step_strs if step_str is not None]

    def run(self, db = None):
        self.db[dd.stop_it] = None

        db = self.db
        for step in self.steps:
            if not db[dd.stop_it]:
                db = step.run(db)

        self.db = db
        self.out = self.db[dd.im]
        


class DataBlock(dict):
    def __init__(self, datablock):
        self.__dict__.update(datablock)

class VisualStep():
    def __init__(self, name, fnc, verbal=False, store_output=False):
        self.name = name
        self.verbal = verbal
        self.fnc = fnc
        self.store_output = store_output
        self.out = None

    def run(self, frame):
        out = self.fnc(frame)
        
        if self.store_output:
            self.out = out
        if self.verbal:
            print('Finished: ',name)
        return out

class VisualControl():
    def __init__(self):
        self.init_almanach()
        self.init_chains()
        self.init_cams()


        self.run()

    def init_cams(self):
        self.cam = CameraControl(0)
        self.chain.db[dd.stream] = self.cam
        
    def init_chains(self):
        #VisualChain.alamanach = self.almanach

        #str_steplist = 'capture, gray, save, rename' 
        str_steplist = 'capture, gray, resize, save_fifo' 
        self.chain = VisualChain(str_steplist)

    def init_almanach(self):

        self.almanach = {}
        def _get_im_(db):
            im = db.get(dd.im, None)
            if im is not None:
                return im
            else:
                print('No image in datablock!')
                return None

        def _stop_it_(db, message):
            db[dd.stop_it] = message

        def step_fcn_decorator(step_fcn):
            def func_wrapper(db):
                func.__dict__['db']
                return db
            return func_wrapper


        def gray(db):
            im = _get_im_(db)
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            db[dd.im] = gray
            return db
        
        def save(db):
            im = _get_im_(db)
            save_path = db.get(dd.save_path, None)
            if not save_path:
                save_path = '/home/pi/stream/out.jpg'
                db[dd.save_path] = save_path
            cv2.imwrite(save_path, im)
            #print('image saved to <', save_path, '> !!!')
            return db

        def save_fifo(db):
            im = _get_im_(db)

            ret, jpeg = cv2.imencode('.jpg', im)
            im_data = jpeg.tobytes()
            
#            return save_locking(db, im_data)
            return save_now(db, im_data)

        def save_now(db, im_data):
            fifo_buff = db[dd.fifo_buff]
            if not os.path.exists(fifo_buff):
                os.mkfifo(fifo_buff)
            open(fifo_buff, 'wb', 0).write(im_data)

            return db


        def save_locking(db, im_data):
            server_waits = os.path.exists(db[dd.server_waits])
            client_wants = os.path.exists(db[dd.client_wants])

            #if server_waits and not client_wants:
                # delete server_waits
             #   os.remove(db[dd.server_waits])

            if not server_waits:
                if not client_wants:
                    fifo_buff = db[dd.fifo_buff]
                    with open(fifo_buff, 'wb', 0) as f:
                        f.write(im_data)
                    print('written')
                else:
                    os.mkfifo(db[dd.server_waits])
                    print('server waits')
            elif 0:
                # client may be dead
                no_response_counter = db[dd.no_response_counter] + 1
                no_response_max = db[dd.no_response_max]
                no_response_max = 1
                print('client_wants', no_response_counter)
                if no_response_counter >= no_response_max:
                    db[dd.no_response_counter] = 0
                    os.remove(db[dd.server_waits])
                    if client_wants:
                        os.remove(db[dd.client_wants])


            return db

        def rename(db):
            save_path = db.get(dd.save_path, None)
            rename_path = db.get(dd.rename_path, None)
            if not rename_path:
                rename_path = '/home/pi/stream/out.mjpg'
                db[dd.rename_path] = rename_path
            os.rename(save_path, rename_path)
            #print('image renamed to <', rename_path, '> !!!')
            return db

        def capture(db):
            stream = db[dd.stream]
            if not stream:
                _stop_it_(db, 'no stream')
            im = stream.get_frame()
            if im is None:
                _stop_it_(db, 'stream image capture failuter')
            db[dd.im] = im
            return db
        

        def resize(db):
            im = _get_im_(db)
            im = cv2.resize(im, (300,200))
            return db


        def add_visual_step(name, fnc, verbal=False, store_output=False):
            self.almanach[name] = VisualStep(name, fnc, verbal, store_output)

        avs = add_visual_step

        avs('gray', gray)
        avs('save', save)
        avs('resize', resize)
        avs('rename', rename)
        avs('capture', capture)
        avs('save_fifo', save_fifo)


        global almanach
        almanach = self.almanach


    def run(self):
        while True:
            self.chain.run()



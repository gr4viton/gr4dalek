from threading import Thread
from settings import logging
import cv2

import arrow

class VideoStreamBase(object):

    def __init__(self, config):
        self.config = config
        self.running = False
        self.frame_count = 0
        self.fps_start = None

        self._pre_config(config)
        self._base_start_stream()
        self._post_config(config)

    def _base_pre_config(self, config):
        """Configure camera before stream start."""
        logging.info('> pre config')
        self._pre_config(config)

    def _base_post_config(self, config):
        """Configure camera after stream start."""
        logging.info('> post config')
        self._post_config(config)

    def _base_start_stream(self):
        """Start camera stream after its _pre_config."""
        logging.info('> start stream')
        self._start_stream()
        self.running = True

    def set_frame(self, frame):
        self.frame = frame
        self.frame_count += 1
        if self.fps_start is None:
            self.fps_start = arrow.utcnow()
        else:
            now = arrow.utcnow()
            dif = now - self.fps_start
            dif_sec = dif.total_seconds()
            if dif_sec > 1:
                fps = self._get_fps(dif_sec)
                logging.info('{fps:.2f} FPS'.format(fps=fps))
                self.fps_start = arrow.utcnow()
                self.frame_count = 0

    def _get_fps(self, dif):
        return self.frame_count / dif

    @property
    def stopped(self):
        return not self.running

    @property
    def name(self):
        name = self.config.name
        if not name:
            name = self.title
        return name

    def _pre_config(self, config):
        """Configure camera before stream start."""
        pass

    def _post_config(self, config):
        """Configure camera after stream start."""
        pass

    def start_thread(self):
        """Start the thread to read frames from the video stream."""
        thr = Thread(target=self.update, name=self.name, args=())
        # thr.daemon = True
        thr.start()
        self.thread = thr

    def update_loop(self):
        """Function to run in separate thread which updates the self.fram with actual camera capture."""
        while self.running:
            self._update_frame()
        self.release()

    @property
    def last_frame(self):
        return self.frame
        if self.frame is not None:
            logging.info('last_frame called - return frame of size = {siz}'.format(siz=self.frame.size))
        else:
            logging.info('frame None')
        return self.frame

    def last_frame_bytes(self):
        frame = self.last_frame
        # frame = imutils.resize(frame, width=600)

        if frame is None:
            logging.info('frame is None')
            return b'0'
        ret2, jpeg = cv2.imencode('.jpg', frame)
        byts = jpeg.tobytes()
        return byts

    def read(self):
        return self.get_frame()

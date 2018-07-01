from threading import Thread
from settings import logging


class VideoStreamBase(object):

    def __init__(self, config):
        self.config = config
        self.running = False
        self.frame_count = 0

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
        self.running = True
        self._start_stream()

    def set_frame(self, frame):
        self.frame = frame
        self.frame_count += 1
        if self.frame_count % 25 == 0:
            logging.info('frame_count = {fc}'.format(fc=self.frame_count))

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

    def start(self):
        """Start the thread to read frames from the video stream."""
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()

    def update(self):
        """Function to run in separate thread which updates the self.fram with actual camera capture."""
        self._update()

    def get_frame(self):
        print('get frame called - return frame of size = {siz}'.format(siz=self.frame.size))
        return self.frame

    def read(self):
        return self.get_frame()

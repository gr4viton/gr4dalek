from .base import VideoStreamBase
from .cv_options import VideoCaptureProperty as prop
import cv2


class VideoStreamCV(VideoStreamBase):

    base_title = 'camera_source'

    @property
    def title(self):
        return '{base}_{num}'.format(base=self.base_title, num=self.source_number)

    @property
    def source_number(self):
        return self.config.source_number

    def _start_stream(self):
        self.stream = cv2.VideoCapture(self.source_nunmber)
        (self.grabbed, self.frame) = self.stream.read()

    def _post_config(self, config):
        self.stream.set(prop.width, config.width)
        self.stream.set(prop.height, config.height)

    def _update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if not self.running:
                self.stream.release()
                return

            # otherwise, read the next frame from the stream
            self.grabbed, self.frame = self.stream.read()

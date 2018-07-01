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
        self.stream = cv2.VideoCapture(self.source_number)
        (self.grabbed, self.frame) = self.stream.read()

    def _post_config(self, config):
        args = ['width', 'height']
        for arg in args:
            self._set_stream_property(arg)

    def _set_stream_property(self, prop_name):
        prop_id = getattr(prop, prop_name).value
        config_value = getattr(self.config, prop_name)
        if config_value is not None:
            self.stream.set(prop_id, config_value)

    def _update(self):
        while self.running:
            self.grabbed, frame = self.stream.read()
            self.set_frame(frame)

        self.stream.release()

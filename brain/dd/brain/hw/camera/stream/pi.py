from .base import VideoStreamBase
from picamera.array import PiRGBArray
from picamera import PiCamera
from settings import logging


class VideoStreamPi(VideoStreamBase):

    base_title = 'raspberry_pi_camera_module'

    @property
    def title(self):
        return self.base_title

    def _pre_config(self, config):

        self.camera = PiCamera()

        args = ['resolution', 'framerate']
        for arg in args:
            self._set_stream_property(arg)

        self.rawCapture = PiRGBArray(self.camera, size=config.resolution)
        self.frame = None

    def _set_stream_property(self, prop_name):
        config_value = getattr(self.config, prop_name)
        if config_value is not None:
            setattr(self.camera, prop_name, config_value)

    def _start_stream(self):
        self.stream = self.camera.capture_continuous(
            self.rawCapture,
            format="bgr",
            use_video_port=True
        )

    def _update_frame(self):
        logging.info(dir(self.stream))

        picamera_frame = self.stream.gi_frame
        frame = picamera_frame.array
        self.set_frame(frame)
        self.rawCapture.truncate(0)
        return

        for picamera_frame in self.stream:
            # grab the frame from the stream
            # clear the stream in preparation for the next frame
            frame = picamera_frame.array
            self.set_frame(frame)

            self.rawCapture.truncate(0)
            break

    def release(self):
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()

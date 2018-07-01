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

    def _update(self):
        # keep looping infinitely until the thread is stopped

        while self.running:
            for picamera_frame in self.stream:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                frame = picamera_frame.array
                self.set_frame(frame)

                self.rawCapture.truncate(0)

                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                #if not self.running:
        logging.info('ending the update loop')

        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        return

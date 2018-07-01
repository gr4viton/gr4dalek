import time
import logging
import cv2

from hw.camera.stream.selector import VideoStreamSelector
import imutils


class Camera:
    cap = None
    out = None

    @staticmethod
    def set_stream(config):
        try:
            if Camera.cap:
                logging.debug("CameraUsb busy")
                Camera.cap.stop()

            # Camera.cap = VideoStream(usePiCamera=True).start()
            logging.info('select video stream')
            video_stream = VideoStreamSelector.from_config()
            Camera.cap = video_stream
            Camera.cap.start()
            time.sleep(2)

        except Exception as exception:
            msg = exception
            logging.error("Error setting up camera: {msg}".format(msg=msg))

    @staticmethod
    def get_frame():
        default = b'0'

        if not Camera.cap:
            return default

        if Camera.cap.running:

            # logging.info('frame_count = {fc}'.format(fc=Camera.cap.frame_count))

            logging.info('cap read')
            frame = Camera.cap.read()
            frame = imutils.resize(frame, width=600)

            ret2, jpeg = cv2.imencode('.jpg', frame)
            byts = jpeg.tobytes()
            return byts
        else:
            return default

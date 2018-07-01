import logging
import cv2
import time
from imutils.video.videostream import VideoStream


class Camera:
    cap = None
    out = None

    @staticmethod
    def set_stream():
        try:
            if Camera.cap:
                logging.debug("CameraUsb busy")
                Camera.cap.stop()

            Camera.cap = VideoStream(usePiCamera=False).start()
            time.sleep(2)

        except Exception as exception:
            msg = exception
            logging.error("Error setting up camera: {msg}".format(msg=msg))

    @staticmethod
    def get_frame():
        if Camera.cap:
            frame = Camera.cap.read()
            # frame = imutils.resize(frame, width=400)

            ret2, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return b'0'




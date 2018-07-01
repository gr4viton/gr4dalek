import logging
import cv2


class Camera:
    cap = None
    out = None

    @staticmethod
    def set_stream(config=None):
        try:
            if Camera.cap:
                logging.info('releasing')
                Camera.cap.release()
            Camera.cap = cv2.VideoCapture(0)
            logging.info('videocap')
        except Exception as exception:
            msg = exception
            logging.error("Error setting up camera: {msg}".format(msg=msg))

    @staticmethod
    def get_frame():
        if Camera.cap:
            ret1, frame = Camera.cap.read()
            logging.info('cap read')
            ret2, jpeg = cv2.imencode('.jpg', frame)
            byts = jpeg.tobytes()
            return byts
        else:
            return b'0'

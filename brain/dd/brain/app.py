from flask import Flask, render_template, Response
import logging
import cv2
from multiprocessing import Process
import picamera
import picamera.array


class Streamer:
    app = Flask(__name__)  # , template_folder='templates')
    stream = None
    camera = None

    @staticmethod
    @app.route('/')
    def index():
        return render_template('streaming.html')

    @staticmethod
    def gen():
        while True:
            frame = Streamer.camera.get_frame()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
            )

    @staticmethod
    @app.route('/video_feed')
    def video_feed():
        return Response(
            Streamer.gen(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )

    @staticmethod
    def start(camera_type='usb'):
        if camera_type == 'usb':
            cam = CameraUsb
        elif camera_type == 'module':
            cam = CameraModule
        elif camera_type == 'pi':
            cam = Camera

        Streamer.camera = cam
        Streamer.camera.set_stream()
        Streamer.stream = Process(
            target=Streamer.app.run,
            args=('0.0.0.0', 5000),
            kwargs={'debug': False},  # imutils does not work with debug
        )
        Streamer.stream.start()

    @staticmethod
    def shutdown():
        if Streamer.stream:
            Streamer.stream.terminate()
            Streamer.stream.join()
            Streamer.stream = None
            return True
        else:
            return False


class CameraUsb:
    cap = None
    out = None

    @staticmethod
    def set_stream():
        try:
            if CameraUsb.cap:
                logging.debug("CameraUsb busy")
                CameraUsb.cap.release()
            CameraUsb.cap = cv2.VideoCapture(0)
        except Exception as exception:
            logging.error(dir(exception))
            # logging.error("Error setting up camera: " + exception)

    @staticmethod
    def get_frame():
        ret1, frame = CameraUsb.cap.read()
        ret2, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

import arrow

class CameraModule:
    cap = None
    out = None
    now = None
    last_image = None

    @staticmethod
    def set_stream():
        try:
            if CameraModule.cap:
                logging.debug("CameraUsb busy")

            print('with camera')
            # with picamera.PiCamera() as camera:
                # camera.start_preview()
                # CameraModule.cap = camera
                # print('start_preview')

        except Exception as exception:
            logging.error("Error setting up camera: " + exception)

    @staticmethod
    def get_frame():
        # camera = CameraModule.cap
        if CameraModule.now is None:
            CameraModule.now = arrow.utcnow()

        dif = arrow.utcnow() - CameraModule.now
        if dif.seconds < 1 and CameraModule.last_image:
            return CameraModule.last_image

        print('get_frame_start')
        with picamera.PiCamera() as camera:
            print('start_preview')
            camera.start_preview()
            with picamera.array.PiRGBArray(camera) as stream:
                print('capture')
                camera.capture(stream, format='bgr')
                image = stream.array
                print(image.size)
                CameraModule.last_image = image.tobytes()

                return CameraModule.last_image

from imutils.video import VideoStream
import datetime
import imutils
import time
import cv2
from hw.camera.stream.selector import VideoStreamSelector

video_stream = VideoStreamSelector.from_config()
logging.debug(video_stream)

class Camera:
    cap = None
    out = None

    @staticmethod
    def set_stream():
        try:
            if Camera.cap:
                logging.debug("CameraUsb busy")
                Camera.cap.stop()

            Camera.cap = VideoStream(usePiCamera=True).start()
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


class Camera:
    cap = None
    out = None

    @staticmethod
    def set_stream():
        try:
            if Camera.cap:
                logging.debug("CameraUsb busy")
                Camera.cap.stop()

            video_stream.start()
            Camera.cap = video_stream
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
            frame = Camera.cap.read()
            # frame = imutils.resize(frame, width=400)

            ret2, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return default


if __name__ == '__main__':
    # Streamer.start()
    # Streamer.start('module')
    Streamer.start('pi')

from flask import Flask, render_template, Response
import logging
import cv2
from multiprocessing import Process


class Streamer:
    app = Flask(__name__)  # , template_folder='templates')
    stream = None

    @staticmethod
    @app.route('/')
    def index():
        return render_template('streaming.html')

    @staticmethod
    def gen():
        while True:
            frame = Camara.get_frame()
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
    def start():
        Camara.set_stream()
        Streamer.stream = Process(target=Streamer.app.run, args=('0.0.0.0', 5000))
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


class Camara:
    cap = None
    out = None

    @staticmethod
    def set_stream():
        try:
            if Camara.cap:
                logging.debug("Camera busy")
                Camara.cap.release()
            Camara.cap = cv2.VideoCapture(0)
        except Exception as exception:
            logging.error("Error setting up camera: " + exception)

    @staticmethod
    def get_frame():
        ret1, frame = Camara.cap.read()
        ret2, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


if __name__ == '__main__':
    Streamer.start()

from flask import Flask, render_template, Response
from multiprocessing import Process


from cam0 import Camera as cam_orig
from cam1 import Camera as cam_imutils
from cam2 import Camera as cam_mine

# from dd.brain.settings import logging
from settings import logging


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
    def start(camera_type='pi'):
        if camera_type == 'pi':
            cam = cam_orig
            cam = cam_mine
            # cam = cam_here

        from hw.camera.stream.config import default_config
        config = default_config
        config.type = 'cv'
        config.type = 'pi'

        Streamer.camera = cam
        logging.info('call flask process')
        Streamer.stream = Process(
            target=Streamer.app.run,
            args=('0.0.0.0', 5000),
            # kwargs={'debug': False},  # imutils does not work with debug
        )
        logging.info('call set_stream')
        Streamer.camera.set_stream(config)

        logging.info('call stream start - starts the thread with update loop')
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



if __name__ == '__main__':
    # Streamer.start()
    # Streamer.start('module')
    Streamer.start('pi')

from flask import Flask, render_template, Response
from multiprocessing import Process


from cam0 import Camera as cam_orig
from cam1 import Camera as cam_imutils
from cam2 import Camera as cam_mine

# from dd.brain.settings import logging
from settings import logging
import arrow


class FlaskWeb:
    app = Flask(__name__)  # , template_folder='templates')
    stream = None
    camera = None

    @staticmethod
    @app.route('/')
    def index():
        return render_template('streaming.html')

    @staticmethod
    @app.route("/status", methods=['GET', 'POST'])
    def status():
        cam = FlaskWeb.camera
        tim = arrow.utcnow()
        dict_ = {
            'running': cam.running,
            'frame_count': cam.frame_count,
            'time': str(tim),
        }

        txt = str(dict_)
        return txt

    @staticmethod
    @app.route("/test", methods=['GET', 'POST'])
    def test():
        # return "You always saw the good in the world."
        cam = FlaskWeb.camera
        txt = str(cam.frame.size)
        return txt

    @staticmethod
    def gen():
        camera = FlaskWeb.camera
        while True:
            if camera.running:
                # print(camera.frame_count)
                camera._update_frame()
                # if camera.frame_count % 25 == 1:
                if True:
                    frame = camera.last_frame_bytes()
                    yield (
                        b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
                    )

    @staticmethod
    @app.route('/video_feed')
    def video_feed():
        return Response(
            FlaskWeb.gen(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )

    @staticmethod
    def start(camera_type='pi'):

        from hw.camera.stream.config import default_config
        config = default_config
        config.type = 'cv'
        config.type = 'pi'

        from hw.camera.stream.selector import VideoStreamSelector
        video_stream = VideoStreamSelector.from_config(config)

        FlaskWeb.camera = video_stream
        logging.info('call flask process')
        FlaskWeb.process = Process(
            target=FlaskWeb.app.run,
            args=('0.0.0.0', 5000),
            # kwargs={'debug': False},  # imutils does not work with debug
        )
        # logging.info('call set_stream')
        # FlaskWeb.camera.start_thread()

        logging.info('start flask process')
        FlaskWeb.process.start()

    @staticmethod
    def shutdown():
        if FlaskWeb.process:
            FlaskWeb.camera.release()

            FlaskWeb.process.terminate()
            FlaskWeb.process.join()
            FlaskWeb.process = None
            return True
        else:
            return False



if __name__ == '__main__':
    # FlaskWeb.start()
    # FlaskWeb.start('module')
    FlaskWeb.start('pi')

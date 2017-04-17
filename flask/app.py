#!/usr/bin/python
from flask import Flask, render_template, Response, request
import datetime
import time

from camera import Camera 
from nocache import nocache

import requests


try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


app = Flask(__name__)


GPIO.setmode(GPIO.BCM)


def gen(camera):
    while True:
        #time.sleep(0.1)
        frame = camera.get_frame()
        if frame is None:
            yield 'no-picture'
        else:
            yield (b'--frame\r\n'
                   b'Access-Control-Allow-Origin: *\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
@nocache
def video_feed():
    return Response(gen(Camera()), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_js')
def video_js():
    return render_template('video_js.html')


def get_time_str():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

def get_random_name():
    #chosen by a fair random choice from calendar
    return 'Peter'

@app.route('/')
def index():
    action = request.args.get('action')
    if action is None:
        action = ''
    if action=='snapshot':
        return Response(gen(Camera()), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    temp = {
        'title' : 'HELLO',
        'time': time_str,
        'name': 'SUCKER',
        'random_name' : 'your mum',
    }
    return render_template('index.html', **temp)



@app.route('/name/<name>')
def hello(name):
    temp = {
        'title' : 'HELLO',
        'time': get_time_str(),
        'name' : name,
        'random_name' : get_random_name(),
    }

    return render_template('index.html', **temp)


@app.route("/readPin/<pin>")
def readPin(pin):
    try:
        GPIO.setup(int(pin), GPIO.IN)
        if GPIO.input(int(pin)) == True:
            response = "Pin number " + pin + " is high!"
        else:
            response = "Pin number " + pin + " is low!"
    except:
        response = "There was an error reading pin " + pin + "."

    templateData = {
        'title' : 'Status of Pin' + pin,
        'response' : response
    }

    return render_template('pin.html', **templateData)  






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


# Note: This should only be run on the flask development server as it is
# not designed to be process safe.

import flask
import cv2
import serial
import time
import threading
import queue

serial_data_queue = queue.Queue()

def send_serial_data():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        while True:
            data: bytes = serial_data_queue.get()
            for b in data:
                ser.write(b.to_bytes(1, 'big'))
                time.sleep(0.02)
            serial_data_queue.task_done()
    except serial.SerialException as ex:
        print(ex)

send_serial_thread = threading.Thread(target=send_serial_data)
send_serial_thread.start()


app = flask.Flask(__name__)

# Resources used:
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# https://stackoverflow.com/questions/54786145/web-cam-in-a-webpage-using-flask-and-python

camera0 = cv2.VideoCapture(2)
camera0_lock = threading.Lock()
camera1 = cv2.VideoCapture(4)
camera1_lock = threading.Lock()

def computer_send_bytes(arr: bytes):
    print(arr)
    serial_data_queue.put(arr)


def generate_frames(camera: cv2.VideoCapture):
    while True:
        if not camera.isOpened():
            yield b''
        retval, frame = camera.read()
        b = b''
        if retval:
            retval, frame = cv2.imencode('.jpg', frame)
            if retval:
                b = frame.tobytes()
        yield b'--frame\r\nContent-type: image/jpeg\r\n\r\n' + b + b'\r\n\r\n'


@app.route('/camera0')
def camera0_stream():
    with camera0_lock:
        return flask.Response(generate_frames(camera0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera1')
def camera1_stream():
    with camera1_lock:
        return flask.Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset', methods=['POST'])
def reset_computer():
    computer_send_bytes(b'\x01')
    return flask.Response()

def send_file(arr: bytes):
    #computer_send_bytes(b'x\n')
    computer_send_bytes(arr.hex().encode())


def js_key_to_ascii(js_key):
    if len(js_key) == 1:
        return js_key
    match js_key:
        case b'Enter':
            return b'\n'
        case b'Escape':
            return b'\x1b'
        case b'Backspace':
            return b'\b'
        # Internal the 8-bit computer uses these codes for the arrows though
        # they are not official.
        case b'ArrowLeft':
            return b'\x11'
        case b'ArrowUp':
            return b'\x12'
        case b'ArrowRight':
            return b'\x13'
        case b'ArrowDown':
            return b'\x14'
        case _:
            return b'\x00'

@app.route('/key', methods=['POST'])
def key_entered():
    key = js_key_to_ascii(flask.request.get_data())
    if (key != '\x00'):
        computer_send_bytes(key)
    return flask.Response()

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if flask.request.method == 'POST':
        send_file(flask.request.files['file'].stream.read())
    return flask.render_template('home.html')


from flask import Flask, Response, render_template
from picamera2 import Picamera2
import cv2
from servos import AZIMUTH_PIN, ELEVATION_PIN, rotate, cleanup_servos, SPEED, DURATION

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (CAMERA_WIDTH, CAMERA_HEIGHT)}))
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')
        
@app.route('/')
def index():
    return render_template("./index.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move/<direction>', methods = ['GET'])
def move(direction: str):
    match direction:
        case "UP":
            rotate(pin=ELEVATION_PIN, speed=-SPEED, duration=DURATION)
        case "DOWN":
            rotate(pin=ELEVATION_PIN, speed=SPEED, duration=DURATION)
        case "LEFT":
            rotate(pin=AZIMUTH_PIN, speed=SPEED, duration=DURATION)
        case "RIGHT":
            rotate(pin=AZIMUTH_PIN, speed=-SPEED, duration=DURATION)

    return "Success!", 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=3000, debug=False)
    finally:
        cleanup_servos()

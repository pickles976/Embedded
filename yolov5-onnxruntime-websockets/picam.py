import asyncio
import websockets
import cv2
import time
from picamera import PiCamera
import numpy as np

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
SCALE = 0.7
FPS = 10.0
SIZE = (640, 480)

# create handler for each connection
async def handler(websocket, path):

    print("Initializing webcam...")
    with PiCamera() as camera:

        camera.resolution = SIZE
        camera.framerate = FPS
        time.sleep(2)
        print("Webcam initialized!")

        while True:

            # Capture the video frame
            frame = np.empty((SIZE[0] * SIZE[1] * 3,), dtype=np.uint8)
            camera.capture(frame, 'bgr', use_video_port=True)
            frame = frame.reshape((SIZE[1], SIZE[0], 3))

            # To bytes
            frameData = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()
        
            await websocket.send(frameData)

print("Starting server thread...")
start_server = websockets.serve(handler, "", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
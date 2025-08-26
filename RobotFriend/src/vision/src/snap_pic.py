from picamera import PiCamera
import time
from time import sleep

WIDTH, HEIGHT = 1280, 960

camera = PiCamera()
camera.resolution = (WIDTH, HEIGHT)
camera.rotation = 180
camera.start_preview()
sleep(1)
data= time.strftime("%Y-%b-%d_(%H%M%S)")
camera.capture('%s.jpg'%data, use_video_port=True)  
camera.stop_preview()
#!/usr/bin/python
from picamera import PiCamera
from time import sleep

WIDTH, HEIGHT = 1280, 960

camera = PiCamera()
camera.resolution = (WIDTH, HEIGHT)
camera.rotation = 180
camera.framerate = 60
camera.start_preview()
sleep(1)

for filename in camera.capture_continuous('img{counter:03d}.jpg',use_video_port=True):
    print('Captured %s' % filename)
    sleep(0.1) # wait 0.1s



#!/usr/bin/python
'''
  A Simple mjpg stream http server for the Raspberry Pi Camera
  inspired by https://gist.github.com/n3wtron/4624820
'''
import io
import time
import picamera
from picamera.array import PiRGBArray
# from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import rospy
import ros_numpy
import signal
import numpy as np
import cv2
# from PIL import Image

# (640, 480)
# (1280, 960)
WIDTH, HEIGHT = 1280, 960
camera=None
topic = 'camera/image/compressed'
node_name = 'camera'

def talker():

    print('Initializing node: {} with topic "{}"'.format(node_name, topic))
    pub = rospy.Publisher(topic, CompressedImage, queue_size=2)
    rospy.init_node(node_name, anonymous=True)
    rate = rospy.Rate(10) # 2 hz

    print("Starting camera...")
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    rawCapture = PiRGBArray(camera, size=(WIDTH, HEIGHT))
    camera.framerate = 60
    camera.rotation = 180
    
    time.sleep(2)

    print("Starting capture...")
    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):

        output = frame.array
        output = np.dot(output[...,:3], [0.299, 0.587, 0.114]) # convert to black and white
        output = output.astype(np.uint8)

        # message = ros_numpy.msgify(CompressedImage, output, encoding='mono8')
        message = CompressedImage()
        message.header.stamp = rospy.Time.now()
        message.format = "jpeg"
        message.data = np.array(cv2.imencode('.jpg', output)[1]).tostring()

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        print("Sending image...  (Press CTRL+C to exit)")
        pub.publish(message)
        rate.sleep()

def handler(signum, frame):
    print("CTRL+C pressed, exiting gracefully...")
    camera.close()


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, handler)
        talker()
    except rospy.ROSInterruptException:
        pass
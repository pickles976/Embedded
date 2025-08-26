#!/usr/bin/python
'''
  A Simple mjpg stream http server for the Raspberry Pi Camera
  inspired by https://gist.github.com/n3wtron/4624820
'''
import io
import time
import picamera
from sensor_msgs.msg import Image
import rospy
import numpy as np
import ros_numpy

camera=None

def talker():

    pub = rospy.Publisher('camera/image', Image, queue_size=10)
    rospy.init_node('camera', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    camera = picamera.PiCamera()
    camera.resolution = (1280, 960)
    camera.framerate = 10
    camera.rotation = 180

    while not rospy.is_shutdown():

        message = Image()

        output = np.empty((960, 1280, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')

        message = ros_numpy.msgify(Image, output, encoding='rgb8')

        # rospy.loginfo(message)
        pub.publish(message)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
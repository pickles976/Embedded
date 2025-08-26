#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import os
import pigpio
from time import sleep

# right center = 1540
# left center = 1530
RIGHT_TRIM = 40
LEFT_TRIM = 30

RIGHT_SERVO=12 # pin 32
LEFT_SERVO=13 # pin 33
MIN_WIDTH=1000
MAX_WIDTH=2000
STOP_WIDTH = 1500
RANGE_WIDTH = 500

def right_servo(speed):

    pulse = STOP_WIDTH + RIGHT_TRIM - (RANGE_WIDTH * speed)
    pi.set_servo_pulsewidth(RIGHT_SERVO, pulse)

def left_servo(speed):

    pulse = STOP_WIDTH + LEFT_TRIM + (RANGE_WIDTH * speed)
    pi.set_servo_pulsewidth(LEFT_SERVO, pulse)

def callback(data):

    print(data)

    x = data.linear.x / 6.0
    z = data.angular.z / 2.0 # turn less to make the camera less jittery

    right = 0
    left = 0

    right += x
    left += x

    if (abs(z) > 0.05):
        if (x > 0.01):
            if (z < 0):
                right *= (1-z)
            elif (z > 0):
                left *= (1-z)
        else:
            right = z
            left = -z

    right_servo(right)
    left_servo(left)
    
def listener():

    print("Starting node...")

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.Subscriber("velocity_controller/cmd_vel", Twist, callback)
    rospy.init_node('listener', anonymous=True)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':

    current_os = os.uname()
    print(current_os)

    pi = pigpio.pi()

    if not pi.connected:
        exit()

    print("Pigpio connected")
    print(pi)
    sleep(2)

    listener()
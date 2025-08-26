#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import os


current_os = os.uname()
print(current_os)


def callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    print(data)
    
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
    listener()
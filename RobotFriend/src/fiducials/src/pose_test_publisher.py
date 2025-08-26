#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped

def talker():

    print("Starting node!")
    rospy.init_node('pose_estimator', anonymous=True)
    pub = rospy.Publisher('pose', PoseStamped, queue_size=10)
    rate = rospy.Rate(5) # 5hz

    while not rospy.is_shutdown():

        p = PoseStamped()

        p.header.frame_id = "map"
        p.header.stamp = rospy.Time.now()

        p.pose.position.x = 5
        p.pose.position.y = 5
        p.pose.position.z = 0
        p.pose.orientation.x = 0
        p.pose.orientation.y = 0
        p.pose.orientation.z = 0
        p.pose.orientation.w = 0

        print("Publishing pose data!")
        
        pub.publish(p) # Send it when ready!
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
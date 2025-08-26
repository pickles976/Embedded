#! /usr/bin/env python
import rospy
from visualization_msgs.msg import Marker
import json
from scipy.spatial.transform import Rotation as R

# marker_json = "./src/fiducials/util/aruco_marker_layout.json"
marker_json = "/home/sebastian/catkin_ws/src/fiducials/util/aruco_marker_layout.json"

def generate_marker_messages(markers):

    msgs = []

    for key in markers:

        top_corner = markers[key]["translation"]
        print(top_corner)

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()

        # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
        marker.type = 1
        marker.id = int(key)

        # Set the scale of the marker
        marker.scale.x = 0.05
        marker.scale.y = 0.262
        marker.scale.z = 0.262

        # Set the color
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0

        # Set the pose of the marker
        marker.pose.position.x = top_corner[0]
        marker.pose.position.y = top_corner[1]
        marker.pose.position.z = top_corner[2]

        r = R.from_euler('xyz', markers[key]["rotation"], degrees=True)
        quat = R.as_quat(r)

        marker.pose.orientation.x = quat[0]
        marker.pose.orientation.y = quat[1]
        marker.pose.orientation.z = quat[2]
        marker.pose.orientation.w = quat[3]

        msgs.append(marker)

    return msgs

def init_node():

    marker_dict = {}

    with open(marker_json, 'r') as file:
        marker_dict = json.load(file)

    rospy.init_node('rviz_marker')
    marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size = 2)

    print("Publishing marker messages...")
    while not rospy.is_shutdown():

        msgs = generate_marker_messages(marker_dict)

        for msg in msgs:
            marker_pub.publish(msg)

        rospy.rostime.wallsleep(1.0)

if __name__ == '__main__':

    print("Initializing node...")
    init_node()
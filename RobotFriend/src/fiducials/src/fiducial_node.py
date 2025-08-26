#!/usr/bin/env python
import rospy
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped
import os
from aruco_tracker import ArucoTracker
import cv2
import numpy as np
np.float = float # monkey patch
import ros_numpy
from scipy.spatial.transform import Rotation as R
from kalman_filter import KalmanFilter

method = cv2.SOLVEPNP_IPPE
marker_dict = "/home/sebastian/catkin_ws/src/fiducials/src/aruco_markers.json"
camera_matrix = "/home/sebastian/catkin_ws/src/fiducials/src/camera_matrix.json"
tracker = None
pose_pub = None
KF = None
ROTATIONAL_OFFSET = 90

def callback(data):

    np_arr = np.fromstring(data.data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    # image = ros_numpy.numpify(data)

    success, pose = tracker.getPoseEstimatesFromImage(image, method)

    if not success:
        return

    trans_corrected = None

    trans = pose[:3,3]
    trans = list(map(lambda x: x / 304.80, trans))
    trans = np.array(trans, dtype=np.float32)
    print("Position:")
    print(trans)

    KF.predict()
    trans_corrected = KF.update(trans[0:2])
    trans_corrected = trans_corrected[0,0:].A1

    rot = pose[:3,:3]
    r = R.from_matrix(rot)

    # APPLY OFFSET 
    euler = R.as_euler(r, 'xyz', degrees=True)
    global ROTATIONAL_OFFSET
    euler[0] = 0
    euler[1] = 0
    euler[2] += ROTATIONAL_OFFSET
    r = R.from_euler('xyz',euler, degrees=True)

    quat = R.as_quat(r)
    print("Orientation:")
    print(quat)

    p = PoseStamped()

    p.header.frame_id = "map"
    p.header.stamp = data.header.stamp

    p.pose.position.x = trans_corrected[0]
    p.pose.position.y = trans_corrected[1]
    # p.pose.position.z = trans_corrected[2]
    p.pose.position.z = 0.21
    p.pose.orientation.x = quat[0]
    p.pose.orientation.y = quat[1]
    p.pose.orientation.z = quat[2]
    p.pose.orientation.w = quat[3]

    global pose_pub
    pose_pub.publish(p) # Send it when ready!

    
def init_node():

    print("Starting node...")

    rospy.init_node('fiducial_node', anonymous=True)

    rospy.Subscriber("camera/image/compressed", CompressedImage, callback)
    global pose_pub 
    pose_pub = rospy.Publisher('geometry_msgs/pose_fiducial', PoseStamped, queue_size = 10)

    rospy.spin()

if __name__ == '__main__':

    # load Aruco Tracker
    print("Initializing Tracker...")
    tracker = ArucoTracker(camera_matrix, marker_dict)

    #KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)
    KF = KalmanFilter(0.5, 1, 1, 1, 0.1,0.1)

    init_node()
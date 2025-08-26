# Robot Project

# How to use

## First time setup (laptop and robot)
1. clone repo
2. source opt/ros/kinetic/setup.bash
3. follow instructions for subsequent setup

## Robot setup
1. source initialize_pi.bash
2. sudo pigpiod
3. on Raspberry pi run "rosrun robot driver.py"

## Laptop setup
1. source initialize_master.bash
2. roslaunch main.launch

## Robot Scripts
1. roslaunch robot.launch

## Laptop Scripts
1. roscore
2. rosrun controller publisher.py
3. rviz
4. rosrun marker_node.py
5. rosrun pose_estimator.py

# Debugging hardware

Servo datasheet
https://docs.rs-online.com/0e85/0900766b8123f8d7.pdf

Servos need to be grounded to the RaspberryPi

Servos need 50hz w/ duty cycle of 5% to 10%
Duty cycle of 7.5% is stopped.

# Chassis Dimensions

robotv4.blend

Width = 7.931cm

Battery dims
L = 13.97cm
W = 6.731cm
H = 1.6256cm

Pi hole dims
4.9cm
5.8cm

robot hole dims
6.985cm x 6.985cm

wall thickness
4mm

# Vision

## Camera and Streaming on the Robot

There is one camera on the raspberry pi.

vision.py in the robot package takes video-accelerated images with the picamera and
streams them at the topic /camera/image

To view the stream on the laptop, run

rosrun image_view image_view image:=/camera/image

## Testing and utilities

snap_pic.py takes a picture, good for taking calibration images
websocket.py serves images at ip:8080, this can be hooked up to Yolo onnx or camera_viewer.html
camera_http_server.py serves images through html at ip:8000

# Fiducials and Localization

## Fiducial dictionary

The robot has a dictionary of 10 5x5 Aruco "Classic" fiducials, each 8cm wide.
The position and rotation of each can be found in src/pose_estimation/util/aruco_marker_layout.json

generate_marker_json.py turns this minimal json into a representation of all corners in 3D space.
The 3D coordinate system has Z as up, and is left-handed

The fiducials package has a folder called localization_images, these are images taken at specific coordinates width
fiducials in view. These images can be used for testing different pose estimation algorithms.

Localization is done from Perspective-n-Point:
https://en.wikipedia.org/wiki/Perspective-n-Point#:~:text=Perspective%2Dn%2DPoint%20is%20the,2D%20projections%20in%20the%20image.

## Camera calibration

The fiducials/util package has calibrate_camera.py which runs camera calibration on the images in the calibration_images folder.
The output goes into camera_matrix.json and can be loaded later.

The images in util/localization_images are used to test the veracity of the fiducials. Pictures can be taken manually and used to test the accuracy of certain pnp solver methods.



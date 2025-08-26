#!/bin/bash

rm -rf build
catkin_make -only-pkg-with-deps common_msgs robot

source ./devel/setup.bash
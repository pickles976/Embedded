from gettext import translation
import json
import os
from turtle import dot
import numpy as np
from math import sin, cos
from scipy.spatial.transform import Rotation   
import copy

WIDTH_MM = 80

path = "./src/fiducials/util/"
marker_file = "aruco_marker_layout.json"

aruco_markers = None

## TOP-LEFT OF MARKER IS ZERO POSITION
## BOTTOM LEFT, BOTTOM RIGHT, TOP RIGHT, TOP LEFT
corners = [
    [0, 0, 0],
    [0, WIDTH_MM, 0],
    [0, WIDTH_MM, -WIDTH_MM],
    [0, 0, -WIDTH_MM]
]

with open(os.path.join(path, marker_file), 'r') as f:

    dict = json.load(f)

    corner_dict = {}

    # Initialize corner dict with default corners
    for key in dict:
        corner_dict[key] = copy.deepcopy(corners)

    # rotate corners by rotation matrix
    for key in dict:

        angles = dict[key]["rotation"]
        r = Rotation.from_euler("xyz",angles,degrees=True)
        new_rotation_matrix = r.as_matrix()

        corners = corner_dict[key]
        
        for i in range(0, len(corners)):
            corner = np.array(corners[i], np.float32)
            corners[i] = corner.dot(new_rotation_matrix)

        corner_dict[key] = corners

    # add translations to corners
    for key in dict:
        trans = dict[key]["translation"]

        # convert to mm
        trans = list(map(lambda x: x * 304.80,trans))

        # convert to numpy array
        trans = np.array(trans, dtype=np.float32)

        # add to corners
        corners = corner_dict[key]

        for i in range(0, len(corners)):
            corners[i] = np.add(corners[i], trans).tolist()
            # corners[i] = corners[i].reshape(3,1).tolist() # need to do this for stupid solvepnp

        corner_dict[key] = corners

    # save to new dict
    aruco_markers = corner_dict

# Save to json
with open(os.path.join(path, "aruco_markers.json"), "w") as outfile:
    json_object = json.dumps(aruco_markers, indent=4)
    outfile.write(json_object)
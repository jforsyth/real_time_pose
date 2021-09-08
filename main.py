import cv2
import mediapipe as mp
import cv2
import time
import numpy as np

from pathlib import Path
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()

# create the background grids
gz = gl.GLGridItem()
gz.translate(0, 0, -1)
w.addItem(gz)

# Array of the 33 mapped points
body_point_array = np.ndarray((33, 3))

# Array of the 35 limbs (2 points for each limb)
limb_array = np.ndarray((70,3))

joint_scatter_plot = gl.GLScatterPlotItem(pos=body_point_array)
joint_scatter_plot.rotate(90, -1, 0, 0)

limb_line_plot = gl.GLLinePlotItem(pos=limb_array, mode="lines", width=2.0)
limb_line_plot.rotate(90, -1, 0, 0)

w.addItem(joint_scatter_plot)
w.addItem(limb_line_plot)


def update():
    joint_scatter_plot.setData()
    limb_line_plot.setData()


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)

mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5
_RGB_CHANNELS = 3
WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)

# For webcam input:
cap = cv2.VideoCapture(0)


def _normalize_color(color):
    return tuple(v / 255. for v in color)


with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        blaze_pose_global_coords = results.pose_world_landmarks
        connection_dict = {
            16:[14, 18, 20, 22],
            18:[20],
            14:[12],
            12:[11, 24],
            11:[23, 13],
            15:[13, 17, 19, 21],
            17:[19],
            24:[23],
            26:[24,28],
            25:[23,27],
            10:[9],
            8:[6],
            5:[6,4],
            0:[4,1],
            2:[1,3],
            3:[7],
            28:[32,30],
            27:[29, 31],
            32:[30],
            29:[31]
        }

        if blaze_pose_global_coords is not None:
            x = 0
            for landmark in blaze_pose_global_coords.landmark:
                body_point_array[x][0] = landmark.x
                body_point_array[x][1] = landmark.y
                body_point_array[x][2] = landmark.z
                x += 1

            # a = 24
            # limb_array[a][0] = blaze_pose_global_coords.landmark[a].x
            # limb_array[a][1] = blaze_pose_global_coords.landmark[a].y
            # limb_array[a][2] = blaze_pose_global_coords.landmark[a].z
            #
            # limb_array[a+1][0] = blaze_pose_global_coords.landmark[connection_dict[a]].x
            # limb_array[a+1][1] = blaze_pose_global_coords.landmark[connection_dict[a]].y
            # limb_array[a+1][2] = blaze_pose_global_coords.landmark[connection_dict[a]].z

            abc = 0
            for connection_index in range(0, 35):
                if connection_index in connection_dict:
                    for connection in range(0, len(connection_dict[connection_index])):

                        #print(f"Joint {connection_index} connected to joint {connection_dict[connection_index]}")

                        limb_array[abc][0] = blaze_pose_global_coords.landmark[connection_index].x;
                        limb_array[abc][1] = blaze_pose_global_coords.landmark[connection_index].y;
                        limb_array[abc][2] = blaze_pose_global_coords.landmark[connection_index].z;

                        limb_array[abc + 1][0] = blaze_pose_global_coords.landmark[connection_dict[connection_index][connection]].x;
                        limb_array[abc + 1][1] = blaze_pose_global_coords.landmark[connection_dict[connection_index][connection]].y;
                        limb_array[abc + 1][2] = blaze_pose_global_coords.landmark[connection_dict[connection_index][connection]].z;

                        abc += 2

            print("///")



        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

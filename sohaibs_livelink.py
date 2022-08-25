#! /usr/bin/env python3
import socket
import json
import sys
import numpy as np
from math import pi
import random
import time
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

TCP_PORT = 2000
BUFFER_SIZE = 1024

starting_height = 1 # starting height in meters
pos_scale = 100
rot_scale = 1
threshold = 0.0005
IPs = ["127.0.0.1"]

message = ""


def get_quaternion_from_euler(roll, pitch, yaw):
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qx, qy, qz, qw]


def t_publishPointsToLiveLink(cameraObj):

    print("AXIBO sending to" , IPs)
# for IP in IPs:  
#     MESSAGE = '{"MHTrack": [{"Type": "CameraSubject"}, {"FieldOfView": "true","AspectRatio": "true","FocalLength": "true","ProjectionMode": "false"}]}'
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect((IP, TCP_PORT))
#     s.send(MESSAGE.encode('utf-8'))
#     s.close() 
    

    while True:
        global g_landmarks
        l_landmarks = g_landmarks
        #print(l_landmarks)
        message = "A_Armature888=Root:(0.000000000,-0.000000000,-0.000000000,-0.000000000,0.000000000,-0.000000000,1.000000000)| "
        if((type(l_landmarks) != type(None)) and (l_landmarks != []) ):
            #print('ree', l_landmarks)
            landmks = l_landmarks.landmark
            for id, lmk in enumerate(landmks):   
                #print(id, lmk)
                coords = landmks[id]
                angles=get_quaternion_from_euler(0, 90, 180)
                message +=  mp_pose.PoseLandmark(id).name + ":(" + "{:.9f}".format(coords.x)+ "," + "{:.9f}".format(-coords.y) +  "," + "{:.9f}".format(-coords.z) +  "," + "{:.9f}".format(-angles[0]) +  "," + "{:.9f}".format(angles[1])+  "," + "{:.9f}".format(-angles[2])+ "," + "{:.9f}".format(angles[3])+ ")" + "|"
                print(message)
            
                for IP in IPs:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect((IP, TCP_PORT))
                    s.send(message.encode('utf-8'))
                    s.close()
        time.sleep(10)


    return




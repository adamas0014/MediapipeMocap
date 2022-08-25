#! /usr/bin/env python3
import io
import socket
import json
import sys
import numpy as np
from math import pi
import random
import time
import mediapipe as mp

liveLinkConfig = {
    "TCP_PORT": 2000, 
    "IPS": ["127.0.0.1"],
    "SOCKET": socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
    "MESSAGE_ENCODING": 'utf-8'
}

class LiveLink():
    def __init__(self, config):
        self._tcpPort = config["TCP_PORT"]
        self._ips = config["IPS"]
        self._socketObject = config["SOCKET"]
        self._messageEncoding = config["MESSAGE_ENCODING"]
        self._message = None

    def formatObjectString(self, pubObject):
        message = 'PythonArmature:= '

        for i, x in pubObject:
            message += str(list(pubObject[i])) + " += " + str(list((pubObject.values())[i])) + " | "
        
        return message
        
    def publish(self, pubObj):
        msg = self.formatObjectString(pubObj)
        for ip in self._ips:
            self._socketObject.connect((ip, self._tcpPort))
            self._socketObject.send(msg.encode(self._messageEncoding))
            self._socketObject.close() 
        
        time.sleep(1)

    










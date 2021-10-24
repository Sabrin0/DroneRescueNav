from threading import Thread
import airsim
import cv2 as cv
import os
import sys
import math
import time
import argparse
import numpy as np


class OANavigation:
    def __init__(self):
        # init client
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        start = time.time()
        print("arming the drone...")
        self.client.armDisarm(True)
        # drone take off
        print("taking off...")
        self.client.takeoffAsync().join()
        self.state = ('Go', 'Turn Left', 'Turn Right')

    def getData(self):
        regions = {
            'front': self.client.getDistanceSensorData(distance_sensor_name='DistanceFront').distance,
            'left': self.client.getDistanceSensorData(distance_sensor_name='DistanceLeft').distance,
            'right': self.client.getDistanceSensorData(distance_sensor_name='DistanceRight').distance
        }
        #print(regions)
        if regions['front'] > 3: #and regions['right'] > 3:
            return self.state[0]

        elif regions['front'] < 3 and regions['left'] > 6:
            return self.state[1]

        elif regions['front'] < 3 and regions['right'] > 6:
            return self.state[2]

        #if regions['front'] < 3 < regions['right'] and regions['left'] > 6:
        #    return self.state[1]

        #elif regions['front'] < 3 < regions['left'] and regions['right'] > 6:
        #    return self.state[2]

        #regions['front'] > 3 and regions['left'] > 3 and regions['right'] > 3:
        #return self.state[0]

    def moveForward(self):
        print('Go Ahead')
        self.client.moveByVelocityBodyFrameAsync(3, 0, 0, 0.1)
        #self.client.moveByVelocityAsync(3, 0, 0, 0.1)

    def turnLeft(self):
        print('Turn Left')
        self.client.rotateToYawAsync(90).join()

    def turnRight(self):
        print('Turn Right')
        self.client.rotateToYawAsync(-90).join()



if __name__ == '__main__':
    drone = OANavigation()
    while True:
        current_state = drone.getData()
        if current_state == 'Go':
            drone.moveForward()
        elif current_state == 'Turn Left':
            drone.turnLeft()
        elif current_state == 'Turn Right':
            drone.turnRight()


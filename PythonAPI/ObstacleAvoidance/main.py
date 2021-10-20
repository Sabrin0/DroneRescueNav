import airsim
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

    # test to set properly the LiDAR
    def setRotation(self, roll_rate, pitch_rate, yaw_rate):
        self.client.moveByAngleRatesThrottleAsync(roll_rate, pitch_rate, yaw_rate, throttle=0.5, duration=5)


if __name__ == '__main__':
    drone = OANavigation()

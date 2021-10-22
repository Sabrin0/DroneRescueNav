import airsim
import sys
import math
import numpy as np


class lidar:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def checkData(self):
        data = self.client.getLidarData()
        measurements = data.point_cloud
        return measurements


if __name__ == '__main__':
    sensor = lidar()
    while True:
        m = sensor.checkData()
        region = len(m)/4

        print(np.max(m))
        if np.max(m) < 4:
            print("---STOP---")
            sensor.client.hoverAsync()
        #if measurements.x_val > 3:
            #sensor.client.hoverAsync()

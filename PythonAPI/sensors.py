import airsim
import sys
import numpy as np


class SensorManager:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.duration = 0.4
        self.regions = {
            'front': None
        }
        print("taking off...")
        self.client.takeoffAsync().join()

    def get_data(self):
        self.regions['front'] = self.client.getDistanceSensorData(distance_sensor_name='DistanceFront').distance
        if self.regions['front'] < 5:
            self.client.simPrintLogMessage('Obstacle Detected')
            self.force_field(self.regions['front'])
            return True
        else:
            return False

    def force_field(self, amplitude):
        gain = 2
        base = 1.5
        force = gain * np.power(base, (-amplitude+5))
        self.client.cancelLastTask()
        self.client.moveByVelocityBodyFrameAsync(-force, 0.0, 0.0, self.duration)
        self.client.simPrintLogMessage('Move Away')

if __name__ =='__main__':
    test = SensorManager()
    while True:
        test.force_field(3)

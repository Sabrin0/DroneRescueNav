import airsim
import sys
import math
import numpy as np


class Lidar:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        #self.client.takeoffAsync().join()
        self.regions = ['E', 'NE', 'N', 'NO', 'O']
        self.regions_number = len(self.regions)
        self.j = [0, 1]
        self.obstacle = False
        self.threshold = 2.0

    def get_data(self):
        sensor_data = self.client.getLidarData()
        measurements = sensor_data.point_cloud
        '''
        print(type(measurements))
        dt = data.time_stamp
        segmentation = data.segmentation
        return measurements, dt, segmentation
        '''
        return measurements

    @staticmethod
    def reshape_point_cloud(point_cloud):
        # create a matrix where each row represent
        # the points [x, y, z] that were hit by the LiDAR
        points = np.array(point_cloud, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 3), 3))
        return points

    @staticmethod
    def euclidean_distance(points):
        # calculate Euclidean distance between the sensor frame
        # and the obstacle
        return np.linalg.norm(points)

    @staticmethod
    def unit_vector(vector):
        # calculate the distance unit vector
        return vector/np.linalg.norm(vector)

    @staticmethod
    def get_theta(v, u):
        # get the angle between the distance unit vector and the y-axis of the LiDAR
        return np.arccos(np.clip(np.dot(v, u), -1.0, 1.0))

    def get_obstacle(self, points):
        if points[3] < self.threshold:
            d = self.unit_vector([points[0], points[1]])
            theta = self.get_theta(d, self.j)
            idx = math.floor(theta / (np.pi / self.regions_number))
            return self.regions[self.check_idx(idx)]
        return None

    def check_idx(self, idx):
        if idx < 0 : return 0
        if idx > (self.regions_number - 1): return (self.regions_number- 1)
        return idx


    def check_obstacle(self, distance):
        if np.min(distance) < self.threshold:
            return True
        else:
            return False

    def manage_data(self):
        data = self.get_data()
        # avoid crash if the lidar laser does not hit anything
        if len(data) == 0:
            return False, None, None
        matrix = self.reshape_point_cloud(data)
        distance = np.array([np.apply_along_axis(self.euclidean_distance, axis=1, arr=matrix)])
        obstacle = self.check_obstacle(distance)
        if not obstacle:
            return obstacle, None, None
        matrix_d = np.append(matrix, distance.T, axis=1)
        region = np.array(np.apply_along_axis(self.get_obstacle, axis=1, arr=matrix_d))
        min_distance, min_region = self.find_closer(region, distance.flatten())

        print('-main- min distance: ', min_distance, '\n-main- min region: ', min_region)
        return obstacle, min_region, min_distance

    def find_closer(self, region, distance):
        min_dist_id = np.argmin(distance)
        return distance[min_dist_id], region[min_dist_id]
"""
if __name__ == '__main__':
    sensor = Lidar()
    while True:
        #m, dt, s = sensor.checkData()
        data = sensor.get_data()
        matrix = sensor.reshape_point_cloud(data)
        distance = np.array([np.apply_along_axis(sensor.euclidean_distance, axis=1, arr=matrix)])
        matrix_d = np.append(matrix, distance.T, axis=1)
        result = np.apply_along_axis(sensor.get_obstacle, axis=1, arr=matrix_d)

"""
        # print('points: ', len(m), '\n dt: ', dt, '\n s: ', len(s))
        # print(np.min(m))
        # if np.max(m) < 4:
        #    print("---STOP---")
        #    sensor.client.hoverAsync()
        # if measurements.x_val > 3:
        # sensor.client.hoverAsync()

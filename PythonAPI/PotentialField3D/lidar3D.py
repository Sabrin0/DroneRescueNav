import airsim
import sys
import math
import numpy as np


class Lidar:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        #self.client.moveToZAsync(-3., 1., timeout_sec=1.).join()
        self.j = [0, 1]
        self.obstacle = False
        self.threshold = 1
        self.range = 7

    def get_data(self):
        sensor_data = self.client.getLidarData()
        measurements = sensor_data.point_cloud
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

    def get_obstacle(self, points):
        if points[3] < self.threshold:
            d = self.unit_vector([points[0], points[1]])
            theta = self.get_theta(d, self.j)
            idx = math.floor(theta / (np.pi / self.regions_number))
            return self.regions[self.check_idx(idx)]
        return None

    def check_idx(self, idx):
        if idx < 0: return 0
        if idx > (self.regions_number - 1): return (self.regions_number - 1)
        return idx

    def check_obstacle(self, distance):
        if np.min(distance) < self.threshold:
            return True
        else:
            return False

    def manage_data(self):
        data = self.get_data()
        # avoid crash if the lidar laser does not hit anything
        try:
            matrix = self.reshape_point_cloud(data)
            distance = np.array([np.apply_along_axis(self.euclidean_distance, axis=1, arr=matrix)])
        except:

            print('No Lidar values')
            return False, None, self.range

        matrix_d = np.append(matrix, distance.T, axis=1)
        closest_obstacle = self.find_closer(matrix_d)

        if closest_obstacle[3] < self.threshold:
            return True, closest_obstacle[0:3], closest_obstacle[3]  # [0:3]

        else:
            return False, None, closest_obstacle[3]

    @staticmethod
    def find_closer(matrix):
        min_dist_id = np.argmin(matrix[:, 3])
        return matrix[min_dist_id]


class DebugLidarData(Lidar):

    def save_closer(self):
        data = super().get_data()

        try:
            matrix = super().reshape_point_cloud(data)
        except:
            print('No lidar value')
            pass

        distance = np.array([np.apply_along_axis(super().euclidean_distance, axis=1, arr=matrix)])
        matrix_d = np.append(matrix, distance.T, axis=1)
        closest_points = self.extract_row(matrix_d)

        if closest_points[3] < 5:
            # print('Distance:', closest_points[3])
            # print('points: ', distance[0:2])
            return closest_points[0:3]
        else:
            pass

    @staticmethod
    def extract_row(matrix):
        # extract closest point
        closest_point_idx = np.argmin(matrix[:, 3])
        return matrix[closest_point_idx]


"""    while True:
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

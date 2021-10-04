import airsim
from airsimTool import to_eularian_angles
import numpy as np


class Data:
    def __init__(self):
        # initialize client
        self.client = airsim.MultirotorClient()
        # init data
        self.time = np.zeros(0)
        self.dt_start = self.client.getMultirotorState().timestamp / 1e9 #np.array(self.client.getMultirotorState().timestamp)
        self.SP7_position = np.empty((0, 3), float)

        self.SP7_orientation = np.empty((0, 3), float)
        self.SP7_lin_vel = np.empty((0, 3), float)
        self.SP7_ang_vel = np.empty((0, 3), float)
        self.SP7_position_line = np.empty((0, 3), float)
        self.SP7_orientation_line = np.empty((0, 3), float)
        self.SP7_lin_vel_line = np.empty((0, 3), float)
        self.SP7_ang_vel_line = np.empty((0, 3), float)

        self.Rpos = np.array(
            [[1, 0, 0],
             [0, -1, 0],
             [0, 0, -1]])

        self.Ror = np.array([[1, 0, 0],
                             [0, -1, 0],
                             [0, 0, -1]])

    #    self.Rpos = np.matrix('1 0 0; 0 -1 0; 0 0 -1')
    #    self.Ror = np.matrix('1 0 0; 0 -1 0; 0 0 -1')

    def get_position(self):
        # self.SP7_position = self.Rpos * np.transpose(self.client.getMultirotorState(
        # ).kinematics_estimated.position.to_numpy_array()) self.SP7_position = self.client.getMultirotorState(
        # ).kinematics_estimated.position.to_numpy_array()*self.Rpos Update Transform
        self.SP7_position_line = np.matmul(
            self.client.getMultirotorState().kinematics_estimated.position.to_numpy_array(), self.Rpos)

        # Save current position
        self.SP7_position = np.append(self.SP7_position, [self.SP7_position_line], axis=0)

    def get_orientation(self):
        # from quaternion to Euler [Roll, Pitch, Yaw] in np array format
        self.SP7_orientation_line = np.array(
            to_eularian_angles(self.client.getMultirotorState().kinematics_estimated.orientation))
        # Update transform
        self.SP7_orientation_line = np.matmul(self.SP7_orientation_line, self.Ror)
        self.SP7_orientation = np.append(self.SP7_orientation, [self.SP7_orientation_line], axis=0)

    def get_velocities(self):

        self.SP7_lin_vel_line = np.matmul(
            self.client.getMultirotorState().kinematics_estimated.linear_velocity.to_numpy_array(), self.Rpos)
        self.SP7_lin_vel = np.append(self.SP7_lin_vel, [self.SP7_lin_vel_line], axis=0)

        self.SP7_ang_vel_line = np.matmul(
            self.client.getMultirotorState().kinematics_estimated.angular_velocity.to_numpy_array(), self.Ror)

        self.SP7_ang_vel = np.append(self.SP7_ang_vel, [self.SP7_ang_vel_line], axis=0)


if __name__ == "__main__":
    droneData = Data()
    while (droneData.client.getMultirotorState().timestamp / 1e9) - droneData.dt_start < 45:
        #print((droneData.client.getMultirotorState().timestamp / 1e9) - droneData.dt_start)
        #dt = np.append(dt, [droneData.dt_line], axis=0)
        droneData.time = np.append(droneData.time,
                                   [(droneData.client.getMultirotorState().timestamp / 1e9) - droneData.dt_start],
                                   axis=0)

        droneData.get_position()
        droneData.get_orientation()
        droneData.get_velocities()

        #if i > 100:
            # finalData = np.append(droneData.position, droneData.orientation, axis=1)
        np.savetxt('circular.txt', np.column_stack((droneData.time, droneData.SP7_position, droneData.SP7_orientation, droneData.SP7_lin_vel, droneData.SP7_ang_vel)), fmt='%.4f', delimiter=' ')
            # np.savetxt('prova.txt', droneData.position, fmt='%.s', delimiter=' ')
            #break
        # client = airsim.MultirotorClient()
        # position = client.getMultirotorState().kinematics_estimated.position


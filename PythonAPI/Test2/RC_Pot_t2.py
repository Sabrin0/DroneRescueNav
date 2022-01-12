import setup_path
import airsim
import sys
import time
import pygame
from scipy.spatial import distance
from PotentialField3D.lidar3D import Lidar
from PotentialField3D.force_field3D import GenerateForce

import numpy as np

# from scipy.spatial.transform import Rotation as ScipyRotation
from pygame.locals import *


class UAVController:
    def __init__(self):
        self.acceleration = 3.0
        self.max_speed = 10.0

        self.angular_velocity = 90.0
        self.duration = 0.4
        self.friction = 0.5
        self.desired_velocity = np.zeros(3, dtype=np.float32)

        # PyGame Initialization
        pygame.init()
        self.my_base = pygame.joystick.Joystick(1)
        self.my_controller = pygame.joystick.Joystick(2)
        self.my_throttle = pygame.joystick.Joystick(0)
        pygame.joystick.init()
        self.smooth = 0.7
        # self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.input_mapping = {
            'nose': 'altitude_motion',  # button t_axis -> old key
            'base': 'yaw_motion',
            'horizontal_axis': 'horizontal_motion',
            'vertical_axis': 'vertical_motion',
            't_axis': 'velocity_control',
            'red': 'restart',

        }

        #  Flag for obstacle avoidance
        self.obstacle = False

        #  initialize input as false
        self.active_command = {command: False for command in self.input_mapping.values()}
        # AirSim Client Connection

        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.takeoffAsync().join()
        # self.client.armDisarm(True)
        self.starting_pose = self.client.simGetVehiclePose()

    def input_manager(self):
        obstacle, points, self.current_distance = sensor.manage_data()
        if not obstacle:
            self.horizontal_axis = self.my_controller.get_axis(0)  # joystick vertical axis
            self.vertical_axis = self.my_controller.get_axis(1)  # joystick horizontal axis
            self.t_axis = self.my_throttle.get_axis(2)  # throttle axis
            self.base = self.my_base.get_axis(2)  # base platform
            self.nose = self.my_controller.get_hat(0)  # NOSE joystick
            self.restart = self.my_controller.get_button(0)  # restart button
            pygame.event.pump()

            if self.restart == 1:
                self.active_command[self.input_mapping['red']] = True
            else:
                self.active_command[self.input_mapping['red']] = False

            # --------------------- SET VELOCITY ---------------------

            if self.t_axis < 0.9:
                self.active_command[self.input_mapping['t_axis']] = True
            else:
                self.active_command[self.input_mapping['t_axis']] = False

            # --------------------- MOVE UP/DOWN ---------------------

            if self.nose[1] != 0:
                self.active_command[self.input_mapping['nose']] = True
            else:
                self.active_command[self.input_mapping['nose']] = False

            # --------------------- TURN LEFT/RIGHT ---------------------
            if np.abs(self.horizontal_axis) > 0.05:  # dead zone threshold
                self.active_command[self.input_mapping['horizontal_axis']] = True
            else:
                self.active_command[self.input_mapping['horizontal_axis']] = False

            # ------------------ MOVE FORWARD/BACKWARD ------------------
            if np.abs(self.vertical_axis) > 0.05:  # dead zone threshold
                self.active_command[self.input_mapping['vertical_axis']] = True
            else:
                self.active_command[self.input_mapping['vertical_axis']] = False

            # ----------------------- YAW CONTROL -----------------------
            if abs(self.base) > 0.05:
                self.active_command[self.input_mapping['base']] = True
            else:
                self.active_command[self.input_mapping['base']] = False

            self.move_by_joystick()
            time.sleep(self.duration / 2.5)  # 2.00
        else:
            FF.sigmoid(self.current_distance)
            vel = FF.get_vel(points[0:3])
            self.client.moveByVelocityBodyFrameAsync(
                -vel[0].item(), -vel[1].item(), -vel[2].item(),
                self.duration
            )
            self.send_flag()

    def send_flag(self):
        command = "ke FlyingPawn FlagMainSP7"
        self.client.simRunConsoleCommand(command)

    def input_scaling(self, input):
        current_vel = (input - 1) * self.max_speed / (-2)
        return current_vel

    def move_by_joystick(self):

        self.desired_velocity = np.zeros(3, dtype=np.float32)

        if self.active_command['restart']:
            self.client.simSetVehiclePose(self.starting_pose, ignore_collision=True)
            print('RESTART')

        if self.active_command['velocity_control']:
            current_vel = self.input_scaling(self.t_axis)
        else:
            current_vel = 0.0

        if self.active_command['altitude_motion']:
            self.desired_velocity[2] += current_vel * self.nose[1]
        else:
            self.desired_velocity[2] = 0.0

        if self.active_command['horizontal_motion']:
            self.desired_velocity[1] += current_vel * self.horizontal_axis
        else:
            self.desired_velocity[1] = 0.0

        if self.active_command['vertical_motion']:
            self.desired_velocity[0] += current_vel * self.vertical_axis
        else:
            self.desired_velocity[0] = 0.0

        if self.active_command['yaw_motion']:
            yaw_rate = self.angular_velocity * -self.base
        else:
            yaw_rate = 0.0

        self.move(self.desired_velocity, yaw_rate)

    def move(self, velocity, yaw_rate):

        self.client.moveByVelocityBodyFrameAsync(-velocity[0].item(), velocity[1].item(), -velocity[2].item(),
                                                 self.duration,
                                                 yaw_mode=airsim.YawMode(True, yaw_rate))


if __name__ == '__main__':
    sensor = Lidar()
    FF = GenerateForce()
    drone = UAVController()
    while True:
        drone.input_manager()

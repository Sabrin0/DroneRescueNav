import airsim
from keyboardControl import DroneController
from PotentialField3D.lidar3D import Lidar
from PotentialField3D.force_field3D import GenerateForce
import airsim
from pynput import keyboard
import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation
import time


class DroneController:
    """
    High level drone controller for manual drone navigation using a regular keyboard.
    """
    def __init__(self):
        self.drones_list = ['DummyDrone', 'MainDrone']
        self.acceleration = 3.0
        self.max_speed = 6.0
        self.min_speed = 1.0
        self.angular_velocity = 90.0
        self.duration = 0.4
        self.friction = 0.2
        self.max_distance = 7
        self.min_distance = 1.0
        self.current_distance = 0.0

        self.allowed_velocity = self.max_speed

        self.desired_velocity = np.zeros(3, dtype=np.float32)

        self._key_command_mapping = {
            keyboard.Key.up: "forward",
            keyboard.Key.down: "backward",
            keyboard.Key.left: "turn left",
            keyboard.Key.right: "turn right",
            keyboard.KeyCode.from_char("w"): "up",
            keyboard.KeyCode.from_char("s"): "down",
            keyboard.KeyCode.from_char("a"): "left",
            keyboard.KeyCode.from_char("d"): "right",
        }

        self._active_commands = {command: False for command in self._key_command_mapping.values()}

        self._client = airsim.MultirotorClient()

        # drone initialization
        self._client.simPause(True)
        self._client.confirmConnection()

        for name in self.drones_list:
            self._client.enableApiControl(True, vehicle_name=name)
            self._client.armDisarm(True, vehicle_name=name)
        self._client.simPause(False)

        self.init_overload()

        for name in self.drones_list:
            self._client.moveToZAsync(-4., 2., timeout_sec=2., vehicle_name=name).join()
            time.sleep(0.3)

        self.init_overload()
        #self._client.takeoffAsync()

    def init_overload(self):
        main_pose = self._client.simGetVehiclePose(vehicle_name='MainDrone')
        self._client.simSetVehiclePose(pose=main_pose, vehicle_name='DummyDrone', ignore_collision=True)
        self._client.hoverAsync(vehicle_name='DummyDrone').join()


    def fly_by_keyboard(self):
        """
        Begin to listen for keyboard input and send according control commands until `esc` is pressed.
        """
        print("Starting manual control mode...")
        # Start a listener instance that invokes callbacks when keys are pressed or released. When the listener stops,
        # it indicates that the whole execution should stop too.
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as keyboard_listener:
            keyboard_listener.wait()
            print("Ready, you can control the drone by keyboard now.")
            while keyboard_listener.running:
                self._handle_commands()
                time.sleep(self.duration / 2.0)
            keyboard_listener.join()
        print("Manual control mode was successfully deactivated.")

    def fly_by_keyboard_ff(self):
        """
        Begin to listen for keyboard input and send according control commands until `esc` is pressed.
        """

        print("Starting manual control mode...")
        # Start a listener instance that invokes callbacks when keys are pressed or released. When the listener stops,
        # it indicates that the whole execution should stop too.
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as keyboard_listener:
            keyboard_listener.wait()

            while keyboard_listener.running:
                obstacle, points, self.current_distance = sensor.manage_data()

                if not obstacle:
                    """
                    if d <= self.max_distance:
                        self.allowed_velocity = ((d - self.min_distance) / (self.max_distance - self.min_distance) * (
                                    self.max_speed - self.min_speed)) + self.min_speed
                    elif d > self.max_distance:
                        self.allowed_velocity = self.max_speed
                    """

                    self._handle_commands()

                    #current_vel = np.array(self._client.getMultirotorState().kinematics_estimated.linear_velocity)
                    #self._client.simPrintLogMessage('velocity: ', np.array2string(current_vel), severity=2)
                    #print(np.array2string(current_vel))
                    time.sleep(self.duration / 2.0)
                else:

                    FF.get_force(self.current_distance)
                    vel = FF.get_vel(points[0:3])
                    self._client.moveByVelocityBodyFrameAsync(
                            -vel[0].item(), -vel[1].item(), -vel[2].item(),
                            self.duration,
                            vehicle_name='DummyDrone'
                            )
                    #time.sleep(self.duration / 2.0)
            keyboard_listener.join()

        print("Manual control mode was successfully deactivated.")

    def move(self, velocity, yaw_rate):
        FF.save_velocities(np.transpose(velocity))
        self._client.moveByVelocityAsync(velocity[0].item(), velocity[1].item(), velocity[2].item(),
                                         self.duration,
                                         drivetrain=airsim.DrivetrainType.ForwardOnly,
                                         yaw_mode=airsim.YawMode(True, yaw_rate))

    def _on_press(self, key):
        if key in self._key_command_mapping.keys():
            self._active_commands[self._key_command_mapping[key]] = True
        elif key == keyboard.Key.esc:
            # Shutdown.
            return False

    def _on_release(self, key):
        if key in self._key_command_mapping.keys():
            self._active_commands[self._key_command_mapping[key]] = False

    def _handle_commands(self):
        drone_orientation = ScipyRotation.from_quat(self._client.simGetVehiclePose().orientation.to_numpy_array())
        yaw = drone_orientation.as_euler('zyx')[0]
        forward_direction = np.array([np.cos(yaw), np.sin(yaw), 0])
        left_direction = np.array([np.cos(yaw - np.deg2rad(90)), np.sin(yaw - np.deg2rad(90)), 0])

        if self._active_commands["forward"] or self._active_commands["backward"]:
            forward_increment = forward_direction * self.duration * self.acceleration
            if self._active_commands["forward"]:
                self.desired_velocity += forward_increment
            else:
                self.desired_velocity -= forward_increment
        else:
            forward_component = np.dot(self.desired_velocity, forward_direction) * forward_direction
            self.desired_velocity -= self.friction * forward_component

        if self._active_commands["up"] or self._active_commands["down"]:
            vertical_component = drone_orientation.apply(np.array([0.0, 0.0, -1.0]))
            vertical_component *= self.duration * self.acceleration
            if self._active_commands["up"]:
                self.desired_velocity += vertical_component
            else:
                self.desired_velocity -= vertical_component
        else:
            self.desired_velocity[2] *= self.friction

        if self._active_commands["left"] or self._active_commands["right"]:
            lateral_increment = left_direction * self.duration * self.acceleration
            if self._active_commands["left"]:
                self.desired_velocity += lateral_increment
            else:
                self.desired_velocity -= lateral_increment
        else:
            left_component = np.dot(self.desired_velocity, left_direction) * left_direction
            self.desired_velocity -= self.friction * left_component

        speed = np.linalg.norm(self.desired_velocity)
        if speed > self.allowed_velocity:
            self.desired_velocity = self.desired_velocity / speed * self.max_speed


        yaw_rate = 0.0

        if self._active_commands["turn left"]:
            yaw_rate = -self.angular_velocity
        elif self._active_commands["turn right"]:
            yaw_rate = self.angular_velocity

        self.move(self.desired_velocity*(self.current_distance/self.max_distance),
                  yaw_rate)


if __name__ == "__main__":
    controller = DroneController()
    sensor = Lidar()
    FF = GenerateForce()
    controller.fly_by_keyboard_ff()







import airsim
from PotentialField3D.lidar3D import Lidar
from PotentialField3D.force_field3D import GenerateForce
import time


class PathGenerator:
    def __init__(self):
        self._client = airsim.MultirotorClient()
        self._client.confirmConnection()
        self._client.enableApiControl(True)
        self._client.takeoffAsync(timeout_sec=3.0).join()
        self.initial_pose = self._client.getMultirotorState().kinematics_estimated.position
        self.duration = 0.4
        self.end_point = 10.0

    def go_pos(self):
        self._client.moveToPositionAsync(
            self.initial_pose.x_val + self.end_point,
            self.initial_pose.y_val,
            self.initial_pose.z_val,
            1
        )

    def go(self):
        self._client.moveByVelocityBodyFrameAsync(
            1.0,
            0,
            0,
            # self._client.simGetVehiclePose().position.z_val,
            self.duration
        )


if __name__ == '__main__':
    drone = PathGenerator()
    sensor = Lidar()
    ff = GenerateForce()
    dt = 0
    start = time.time()

    while dt < 13.0:
        drone.go()
        dt = time.time() - start
        print(dt)

    drone._client.landAsync().join()

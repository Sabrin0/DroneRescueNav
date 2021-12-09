import airsim
from scipy.spatial import distance
from PotentialField3D.lidar3D import Lidar
from PotentialField3D.force_field3D import GenerateForce
import time


class PathGenerator:
    def __init__(self):
        self._client = airsim.MultirotorClient()
        self._client.confirmConnection()
        self._client.enableApiControl(True)
        #self._client.takeoffAsync(timeout_sec=5.0).join()
        self._client.moveToZAsync(-3., 1., timeout_sec=3.).join()
        self.initial_pose = self._client.getMultirotorState().kinematics_estimated.position
        self.current_x = self.initial_pose
        self.duration = 0.4
        self.end_point = 15.0

    def go_pos(self, destination):
        self._client.moveToPositionAsync(
            self.initial_pose.x_val + self.end_point,
            self.initial_pose.y_val,
            self.initial_pose.z_val,
            1,
            timeout_sec=self.duration,
            drivetrain=airsim.DrivetrainType.ForwardOnly,
            yaw_mode=airsim.YawMode(False, 0)
        )

    def go(self):
        self._client.moveByVelocityBodyFrameAsync(
            1,
            0,
            0,
            # self._client.simGetVehiclePose().position.z_val,
            self.duration
        )

    def get_current_pos(self):
        self.current = self._client.getMultirotorState().kinematics_estimated.position

    def land(self):
        self._client.landAsync().join()

    def move_by_force(self, vector_f):
        self._client.moveByVelocityBodyFrameAsync(
            vector_f[0].item(),
            vector_f[1].item(),
            vector_f[2].item(),
            self.duration
        )
    @staticmethod
    def get_error(p2, p1):
        return abs(distance.euclidean(p2, p1))


if __name__ == '__main__':

    drone = PathGenerator()
    sensor = Lidar()
    ff = GenerateForce()

    dest = [drone.initial_pose.x_val + drone.end_point,
            drone.initial_pose.y_val,
            drone.initial_pose.z_val,
            ]

    e = drone.get_error(dest, airsim.Vector3r.to_numpy_array(drone.initial_pose))

    while e > 0.5:
        obstacle, points, obst_distance = sensor.manage_data()
        print(obst_distance)
        #obstacle = False
        if not obstacle:
            drone.go_pos(dest)
        else:
            ff.sigmoid(obst_distance)
            vel = ff.get_vel(points[0:3])
            drone.move_by_force(-vel)

        time.sleep(drone.duration/2.0)
        drone.get_current_pos()
        e = drone.get_error(dest, airsim.Vector3r.to_numpy_array(drone.current))

    drone.land()

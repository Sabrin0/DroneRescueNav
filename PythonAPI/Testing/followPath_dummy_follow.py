import airsim
from scipy.spatial import distance
from PotentialField3D.lidar3D import Lidar
from PotentialField3D.force_field3D import GenerateForce
import time


class PathGenerator:
    def __init__(self):
        self._client = airsim.MultirotorClient()
        self._client.confirmConnection()
        self.drones = ['DummyDrone', 'MainDrone']

        for name in self.drones:
            self._client.enableApiControl(True, name)
            self._client.armDisarm(True, name)
            self._client.takeoffAsync(vehicle_name=name).join()
            self._client.moveToZAsync(-3., 1., timeout_sec=3., vehicle_name=name).join()
            print('Init drone: ', name)


        # self._client.takeoffAsync(timeout_sec=5.0).join()
        self.main_kin = self._client.simGetGroundTruthKinematics(vehicle_name=self.drones[1])
        self._client.simSetKinematics(self.main_kin, ignore_collision=True, vehicle_name=self.drones[1])
        time.sleep(1)
        self._client.moveByVelocityBodyFrameAsync(-1.0, 0.0, 0.0, 1.0, vehicle_name=self.drones[0])

        self.initial_pose = self._client.getMultirotorState(vehicle_name='MainDrone').kinematics_estimated.position

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
            yaw_mode=airsim.YawMode(False, 0),
            vehicle_name='MainDrone'
        )

    def go(self):
        self._client.moveByVelocityBodyFrameAsync(
            1,
            0,
            0,
            # self._client.simGetVehiclePose().position.z_val,
            self.duration,
            vehicle_name='MainDrone'
        )

    def get_current_pos(self):
        self.current = self._client.getMultirotorState(vehicle_name='MainDrone').kinematics_estimated.position

    def get_main_pose(self):
        return self._client.simGetVehiclePose(vehicle_name='MainDrone')

    def land(self):
        self._client.landAsync(vehicle_name='MainDrone').join()

    def move_by_force(self, vector_f):
        self._client.moveByVelocityBodyFrameAsync(
            vector_f[0].item(),
            vector_f[1].item(),
            vector_f[2].item(),
            self.duration,
            vehicle_name='DummyDrone'
        )

    @staticmethod
    def get_error(p2, p1):
        return abs(distance.euclidean(p2, p1))

    def send_flag(self):
        self._client.simRunConsoleCommand('ce FlagSP7')

    def pause(self, is_paused):
        self._client.simPause(is_paused)

    def spawn_ghost(self):
        main_pose = self.get_main_pose()
        self._client.simAddVehicle(vehicle_name='DummyDrone', vehicle_type='simpleflight', pose=main_pose)

    def overload(self):
        main_pose = self.get_main_pose()
        self._client.simSetVehiclePose(pose=main_pose, vehicle_name='DummyDrone', ignore_collision=False)
        self._client.hoverAsync(vehicle_name='DummyDrone')
        # self._client.simDestroyObject(object_name='DummyDrone')

    def request_control(self):
        self._client.enableApiControl(True, 'DummyDrone')


if __name__ == '__main__':

    drone = PathGenerator()
    sensor = Lidar()
    ff = GenerateForce()

    dest = [drone.initial_pose.x_val + drone.end_point,
            drone.initial_pose.y_val,
            drone.initial_pose.z_val,
            ]

    e = drone.get_error(dest, airsim.Vector3r.to_numpy_array(drone.initial_pose))

    first = True

    while e > 0.5:
        obstacle, points, obst_distance = sensor.manage_data()
        # print(obst_distance)
        # obstacle = False
        # if not obstacle:

        drone.go_pos(dest)
        # if spawned and not obstacle:
        #  drone.overload()
        # else:

        if obstacle:
            if first:
                drone.overload()
                first = False
                start = time.time()

            # drone.send_flag()
            # drone.pause(is_paused=True)

            print('OBSTACLE')

            # if not spawned:
            #    spawned = True
            #    drone.spawn_ghost()
            #    drone.request_control()
            ff.sigmoid(obst_distance)
            # ff.get_force(obst_distance)
            vel = ff.get_vel(points[0:3])
            drone.move_by_force(-vel)

            dt = time.time() - start
            print(dt)
            if dt > 0.3:
                first = True
        else:
            first = True

        #time.sleep(drone.duration / 2)
        drone.get_current_pos()
        e = drone.get_error(dest, airsim.Vector3r.to_numpy_array(drone.current))

    # drone.land()

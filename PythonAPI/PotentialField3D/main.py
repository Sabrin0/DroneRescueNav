from PotentialField.lidar import DebugLidarData
from joystickControl import UAVController


if __name__ == '__main__':

    drone = UAVController()
    #sensor = DebugLidarData()

    while True:
        # move the drone
        drone.input_manager()
        #points = sensor.save_closer()



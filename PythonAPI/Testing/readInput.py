import setup_path
import airsim
import time
import numpy as np

if __name__ == '__main__':
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.moveToZAsync(z=-3, velocity=2.0, timeout_sec=2.0).join()
    input = np.loadtxt('RC_Data/input1.txt', dtype=float, delimiter=' ')
    duration = 0.4
    for command in input:
        if command[0] == 0:
            client.moveByVelocityBodyFrameAsync(
                command[1].item(),
                command[2].item(),
                command[3].item(),
                duration,
                yaw_mode=airsim.YawMode(True, command[4])
            )

        else:
            client.moveByVelocityBodyFrameAsync(
                command[1].item(),
                command[2].item(),
                command[3].item(),
                duration/1.7
            )
        time.sleep(duration / 1.3)





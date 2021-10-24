import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.moveToPositionAsync(100, 0, -3, 2).join()
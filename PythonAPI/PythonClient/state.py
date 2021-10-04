import airsim
import pprint

def print_state():
    print("===============================================================")
    state = client.getMultirotorState()
    print("state: %s" % pprint.pformat(state))
    return state

def print_position():
    position = client.getMultirotorState().kinematics_estimated.position
    print(position)



if __name__ == '__main__':
    client = airsim.MultirotorClient()
    state = print_state()

    while True:
        print_position()
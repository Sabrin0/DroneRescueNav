import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def mean_dt(data):
    dt = np.empty(data.shape)
    for rows in range(0, data.size-1):
        if rows > (data.size):
            break
        dt_line = data[rows+1] - data[rows]
        dt = np.append(dt, [dt_line], axis=0)

    print(np.mean(dt, axis=0))

if __name__ == '__main__':



    data = np.loadtxt("data/scaled_simple120.txt", dtype=float, delimiter=" ")
    #data = np.loadtxt("circular.txt", dtype=float, delimiter=" ")
    #data = np.loadtxt("UnrealCircularPath.txt", dtype=float, delimiter=" ")
    #data = np.loadtxt("x5y5.txt", dtype=float, delimiter=" ")
    #data = np.loadtxt("TakeOffandCircularPath.txt", dtype=float, delimiter=" ")
    #t = data[:,0]
    #print(t.size)
    #mean_dt(t)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(data[:, 1], data[:, 2], data[:, 3], label='Path')
    plt.show()
    # 0 t, 1 x, 2 y , 3 z, 4 roll, 5 pitch, 6 yaw, 7 vx, 8 vy, 9 vz, 10 wx, 11 wy, 12 wz
    ## velocities
    #fig, avs = plt.subplots(3,1)
    #fig.subtitle('Linear Velocity')
    #avs[0].plot(data[:, 0], data[:, 6])
    #avs[0].set_title(' Lin Vel among x [m/s]')
    #avs[0].axhline(y=np.amax(data[:, 6]), color='r')
    #axv[0].show()
    #avs[1].plot(data[:, 0], data[:, 7])
    #avs[1].set_title(' Lin Vel among y [m/s]')
    #avs[1].axhline(y=np.amax(data[:, 7]), color='r')
    #axv[1].show()
    #avs[2].plot(data[:, 0], data[:, 8])
    #avs[2].set_title(' Lin Vel among z [m/s]')
    #avs[2].axhline(y=np.amax(data[:, 8]), color='r')
    #axv[0].show()

    ## Linear Position
    plt.subplot(3, 1, 1)
    plt.plot(data[:, 0], data[:, 1])
    plt.title('Lin Position [m] over time')
    plt.axhline(y=np.amax(data[:, 1]), color='r', ls='--', label='max val %.2f [m]' % (np.amax(data[:, 1])))
    plt.axhline(y=np.amin(data[:, 1]), color='r', ls='--', label='min val %.2f [m]' % (np.amin(data[:, 1])))

    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(data[:, 0], data[:, 2])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 2]), color='r', ls='--', label='max val %.2f [m]' % (np.amax(data[:, 2])))
    plt.axhline(y=np.amin(data[:, 2]), color='r', ls='--', label='min val %.2f [m]' % (np.amin(data[:, 2])))
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data[:, 0], data[:, 3])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 3]), color='r', ls='--', label='max val %.2f [m]' % (np.amax(data[:, 3])))
    plt.axhline(y=np.amin(data[:, 3]), color='r', ls='--', label='min val %.2f [m]' % (np.amin(data[:, 3])))
    plt.legend()
    #plt.savefig('fig/linVel_circular.png', dpi=2000)
    plt.show()

    ## Angular position
    plt.subplot(3, 1, 1)
    plt.plot(data[:, 0], data[:, 4])
    plt.title('Angular position [rad] over time')
    plt.axhline(y=np.amax(data[:, 4]), color='r', ls='--', label='max val %.2f [rad]' % (np.amax(data[:, 4])))
    plt.axhline(y=np.amin(data[:, 4]), color='r', ls='--', label='min val %.2f [rad]' % (np.amin(data[:, 4])))

    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(data[:, 0], data[:, 5])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 5]), color='r', ls='--', label='max val %.2f [rad]' % (np.amax(data[:, 5])))
    plt.axhline(y=np.amin(data[:, 5]), color='r', ls='--', label='min val %.2f [rad]' % (np.amin(data[:, 5])))
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data[:, 0], data[:, 6])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 6]), color='r', ls='--', label='max val %.2f [rad]' % (np.amax(data[:, 6])))
    plt.axhline(y=np.amin(data[:, 6]), color='r', ls='--', label='min val %.2f [rad]' % (np.amin(data[:, 6])))
    plt.legend()
    #plt.savefig('fig/linVel_circular.png', dpi=2000)
    plt.show()

    ## Linear Velocities
    plt.subplot(3, 1, 1)
    plt.plot(data[:, 0], data[:, 7])
    plt.title('Lin Velocities [m/s] over time')
    plt.axhline(y=np.amax(data[:, 7]), color='r', ls='--', label='max val %.2f [m/s]' % (np.amax(data[:, 7])))
    plt.axhline(y=np.amin(data[:, 7]), color='r', ls='--', label='min val %.2f [m/s]' % (np.amin(data[:, 7])))

    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(data[:, 0], data[:, 8])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 8]), color='r', ls='--', label='max val %.2f [m/s]' % (np.amax(data[:, 8])))
    plt.axhline(y=np.amin(data[:, 8]), color='r', ls='--', label='min val %.2f [m/s]' % (np.amin(data[:, 8])))
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data[:, 0], data[:, 9])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 9]), color='r', ls='--', label='max val %.2f [m/s]' % (np.amax(data[:, 9])))
    plt.axhline(y=np.amin(data[:, 9]), color='r', ls='--', label='min val %.2f [m/s]' % (np.amin(data[:, 9])))
    plt.legend()
    #plt.savefig('fig/linVel_circular.png', dpi=2000)
    plt.show()

    ## Angular Velocities

    plt.subplot(3, 1, 1)
    plt.plot(data[:, 0], data[:, 10])
    plt.title('Ang Velocities [m/s] over time')
    plt.axhline(y=np.amax(data[:, 10]), color='r', ls='--', label='max val %.2f [rad/s]' % (np.amax(data[:, 10])))
    plt.axhline(y=np.amin(data[:, 10]), color='r', ls='--', label='min val %.2f [rad/s]' % (np.amin(data[:, 10])))

    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(data[:, 0], data[:, 11])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 11]), color='r', ls='--', label='max val %.2f [rad/s]' % (np.amax(data[:, 11])))
    plt.axhline(y=np.amin(data[:, 11]), color='r', ls='--', label='min val %.2f [rad/s]' % (np.amin(data[:, 11])))
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(data[:, 0], data[:, 12])
    #plt.title('Lin Vel among x [m/s] over time')
    plt.axhline(y=np.amax(data[:, 12]), color='r', ls='--', label='max val %.2f [rad/s]' % (np.amax(data[:, 12])))
    plt.axhline(y=np.amin(data[:, 12]), color='r', ls='--', label='min val %.2f [rad/s]' % (np.amin(data[:, 12])))
    plt.legend()
    #plt.savefig('fig/linVel_circular.png', dpi=2000)
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data= np.loadtxt('data/no_force.txt', dtype=float, delimiter=' ')
    fig = plt.figure()
    #ax = fig.gca(projection='3d')
    ax = plt.axes(projection='3d')
    ax.plot(data[:, 0], data[:, 1], data[:, 2], label='Path')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    # start
    ax.plot(0, 0, np.max(data[:, 2]), 'ro')
    ax.text(0, 0, np.max(data[:, 2])+0.05, 'start', color='red')
    # end
    ax.plot(np.max(data[:,0]), 0, data[np.argmax(data[:,0]), 2], 'ro')
    ax.text(np.max(data[:,0]), 0, data[np.argmax(data[:,0]), 2]+0.05, 'end', color='red')
    plt.show()

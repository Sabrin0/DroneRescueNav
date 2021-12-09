import numpy as np
import matplotlib.pyplot as plt




if __name__ == '__main__':

    data = np.loadtxt('data/no_force0.txt', dtype=float, delimiter=' ')
    data_f1 = np.loadtxt('data/force1.txt', dtype=float, delimiter=' ')
    data_f2 = np.loadtxt('data/force2.txt', dtype=float, delimiter=' ')
    data_f3 = np.loadtxt('data/force3.txt', dtype=float, delimiter=' ')
    data_f4 = np.loadtxt('data/force4.txt', dtype=float, delimiter=' ')
    data_f5 = np.loadtxt('data/force5.txt', dtype=float, delimiter=' ')

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    '''
    for i in range(1, 6, 1):
        print(i)
        data["test"+str(i)] = np.loadtxt('data/force'+str(i)+'.txt', dtype=float, delimiter=' ')
        #ax.plot(data['test'+str(i)])
    '''

    # ax = fig.gca(projection='3d')

    no_force_path, = ax.plot(data[:, 0], data[:, 1], data[:, 2], linestyle='--', color='green', label='no force path')

    force_path1, = ax.plot(data_f1[:, 0], data_f1[:, 1], data_f1[:, 2], label='force path 1', color=(0.1, 0.2, 0.3))
    force_path2, = ax.plot(data_f2[:, 0], data_f2[:, 1], data_f2[:, 2], label='force path 2', color=(0.2, 0.3, 0.4))
    force_path3, = ax.plot(data_f3[:, 0], data_f3[:, 1], data_f3[:, 2], label='force path 3', color=(0.3, 0.4, 0.5))
    force_path4, = ax.plot(data_f4[:, 0], data_f4[:, 1], data_f4[:, 2], label='force path 4', color=(0.4, 0.5, 0.6))
    force_path5, = ax.plot(data_f5[:, 0], data_f5[:, 1], data_f5[:, 2], label='force path 5', color=(0.5, 0.6, 0.7))
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    ax.set_ylim([-5, 5])
    ax.set_zlim([0, 3])
    # start
    ax.plot(0, 0, np.max(data[:, 2]), 'ro')
    ax.text(0, 0, np.max(data[:, 2]) + 0.05, 'start', color='red')
    # end
    '''ax.plot(np.max(data[:, 0]), 0, np.max(data[:, 2]), 'ro')
    ax.text(np.max(data[:, 0]), 0, np.max(data[:, 2]) + 0.05, 'end', color='red')
    ax.scatter(np.max(data[:, 0]), 0, np.max(data[:, 2]),
               s=300,
               facecolor='None',
               edgecolors='r',
               linestyle='--')
    '''
    # take off
    ax.plot(0, 0, 0, 'bo')
    ax.text(0, 0, 0.05, 'take off', color='blue')

    # land
    ax.plot(data[-1, 0], data[-1, 1], data[-1, 2], 'bo')
    ax.text(data[-1, 0], data[-1, 1], data[-1, 2], 'land', color='blue')

    plt.title('Test 1')
    plt.legend(handles=[no_force_path, force_path1, force_path2, force_path3, force_path4, force_path5])
    plt.show()

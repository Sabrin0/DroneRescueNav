import numpy as np
import time
import math
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt

class Test:
    def switch_region(self, region):
        return self.__getattribute__('case_'+ str(region))()

    def case_1(self):
        return [1,1,1]


class Sigmoid:
    def __init__(self):
        self.x = np.linspace(0, 10, 1000)
        self.y = np.empty(0)
        self.d_min = 0.5
        self.d_max = 3.0
        self.F_max = 5
        self.F_min = 0.0
        #self.y = 1/(1  + (math.exp(self.x+10)))

    def plot(self):
        plt.plot(self.x, self.y)
        plt.show()

    def sig_plot(self, d):

        if d >= self.d_max:
            self.y = 0
        elif d <= self.d_min:
            self.y = self.F_max
        else:
            cosarg = ((d - self.d_min) * np.pi) / (self.d_max - self.d_min)
            self.y = (self.F_max - self.F_min) * (0.5 * np.cos(cosarg) + 0.5) + self.F_min
        return self.y

if __name__ == '__main__':
    d = np.linspace(0, 10, 100)
    test = Sigmoid()
    #test.y = np.apply_along_axis(test.sig_plot, axis=0, arr=d)
    for i in range(0, len(d)):
        test.y = np.append(test.y, test.sig_plot(d[i]))
    plt.plot(d, test.y)
    plt.xlabel('Distance')
    plt.ylabel('Force')
    plt.vlines(test.d_min, 0, 5, colors='r', linestyles='--', label='d_min')
    plt.vlines(test.d_max, 0, 5, colors='r', linestyles='--', label='d_max')
    plt.show()

    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make the grid
    x, y, z = [0, 0, 0]

    # Make the direction data for the arrows
    u = [1, 0, 0]
    v = [0, 1, 0]
    w = [0, 0, 1]

    ax.quiver(x, y, z, u, v, w, length=0.2, normalize=True, color='r')

    plt.show()
    """


    #test.plot()
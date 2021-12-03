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
        self.x = np.linspace(-10, 10, 100)
        self.y = 1/(1  + (math.exp(self.x+10)))

    def plot(self):
        plt.plot(self.x, self.y)
        plt.show()

if __name__ == "__main__":
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
    test = Sigmoid()
    test.plot()
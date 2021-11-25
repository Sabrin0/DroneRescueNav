from PotentialField.lidar import DebugLidarData

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.text import Annotation
from matplotlib.patches import FancyArrowPatch
import matplotlib.animation as animation

"""
class plot(plt):
    def plot(self, fx, fy, fz):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(fx, fy, fz)
        plt.show(block=False)
        ax = fig.arrow()


force = plot()


    x = np.linspace(0, 10, 1000)
    ax.plot(x, x*i)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.show(block=False)
    plt.pause(0.01667)
    plt.cla()
    i = i + 1
    """


class Arrow3D(FancyArrowPatch):

    def __init__(self, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (0, 0, 0)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def _arrow3D(ax, dx, dy, dz, *args, **kwargs):
        arrow = Arrow3D(dx, dy, dz, *args, **kwargs)
        ax.add_artist(arrow)

    setattr(Axes3D, 'arrow3D', _arrow3D)


def plot_force(dx, dy, dz, ax):

    ax.arrow3D(
        dx, dy, dz,
        mutation_scale=20,
        arrowstyle="<|-",
        linestyle='dashed')

    ax.set_title('Force Vector')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.show(block=False)
    plt.pause(0.01667)
    plt.cla()



if __name__ == '__main__':
    sensor = DebugLidarData()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    while True:
        points = sensor.save_closer()
        plot_force(points[0], -points[1], -points[2], ax)


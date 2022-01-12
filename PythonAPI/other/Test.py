import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math


def mean_dt(data):
    dt = np.empty(data.shape)
    for rows in range(0, data.size - 1):

        if rows > (data.size):
            break

        dt_line = data[rows + 1] - data[rows]
        dt = np.append(dt, [dt_line])

    print(dt)
    print(np.average(dt))


def rescaling(dataOld, a, b, angle):
    new_data = np.empty(0)

    if not angle:
        for x in range(0, len(dataOld)):
            sx = (((dataOld[x] - np.amin(dataOld)) * (b - a)) / (np.amax(dataOld) - np.amin(dataOld)))
            new_data = np.append(new_data, [sx], axis=0)
        return new_data

    else:
        # fist conversion to radiant
        a *= math.pi / 180
        b *= math.pi / 180

        for x in range(0, len(data)):
            sx = a + (((dataOld[x] - np.amin(dataOld)) * (b - a)) / (np.amax(dataOld) - np.amin(dataOld)))
            new_data = np.append(new_data, [sx], axis=0)

    return new_data


if __name__ == '__main__':
    data = np.loadtxt("data/smooth_circular.txt", dtype=float, delimiter=" ")
    # data = np.loadtxt("TestFPS.txt", dtype=float, delimiter=" ")
    # data = np.loadtxt("UnrealCircularPath.txt", dtype=float, delimiter=" ")
    # data = np.loadtxt("x5y5.txt", dtype=float, delimiter=" ")
    # data = np.loadtxt("TakeOffandCircularPath.txt", dtype=float, delimiter=" ")

    sx = rescaling(data[:, 1], -0.05, 0.05, False)
    sy = rescaling(data[:, 2], -0.05, 0.05, False)
    sz = rescaling(data[:, 3], 0.396, 0.451, False)

    sroll = rescaling(data[:, 4], -5, 5, True)
    spitch = rescaling(data[:, 5], -5, 5, True)
    syaw = rescaling(data[:, 6], -180, 180, True)

    svx = rescaling(data[:, 7], -0.4, 0.4, False)
    svy = rescaling(data[:, 8], -0.325, 0.325, False)
    svz = rescaling(data[:, 9], 0.240, 0.225, False)

    swx = rescaling(data[:, 10], -30, 30, True)
    swy = rescaling(data[:, 11], -40, 40, True)
    swz = rescaling(data[:, 12], -50, 50, True)

    np.savetxt('data/scaled_smooth_circular.txt',
               np.column_stack((data[:, 0], sx, sy, sz, sroll, spitch, syaw, svx, svy, svz, swx, swy, swz)), fmt='%.4f',
               delimiter=' ')

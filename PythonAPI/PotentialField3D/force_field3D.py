import numpy as np
import sys

class GenerateForce:
    def __init__(self):
        self.gain = 5
        self.k = 2
        self.amplitude = 0.0
        self.max_force = 4.5 # 3
        self.min_force = 0.0
        self.min_distance = 0.0 # 0.2
        self.max_distance = 2.5

    def get_force(self, distance):
        self.force = self.gain * np.power(np.e, (-distance / self.k))

    def get_vel(self, points):
        return np.array(points[0:3]*self.force)

    def sigmoid(self, d):

        if d > self.max_distance:
            self.force = self.min_force
        elif d < self.min_distance:
            self.force = self.max_force
        else:
            cosarg = (d - self.min_distance) * np.pi / (self.max_distance - self.min_distance)
            self.force = (self.max_force - self.min_force) * (0.5 * np.cos(cosarg) + 0.5) + self.min_force

    def sigmoid_updated(self, d, max):
        max_force = max
        if d > self.max_distance:
            self.force = self.min_force
        elif d < self.min_distance:
            self.force = max_force
        else:
            cosarg = (d - self.min_distance) * np.pi / (self.max_distance - self.min_distance)
            self.force = (max_force - self.min_force) * (0.5 * np.cos(cosarg) + 0.5) + self.min_force

    @staticmethod
    def save_velocities(vel):
        with open('velocities.txt', 'ab') as f:
            f.write(b"\n")
            np.savetxt(f, vel, delimiter=' ', fmt='%.4f')
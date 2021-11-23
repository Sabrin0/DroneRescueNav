import numpy as np


class ForceField:
    def __init__(self):
        self.gain = 2
        self.base = 1.5
        self.duration = 0.4
        self.amplitude = 0.0

    def generate_amplitude(self, d):
        self.amplitude = self.gain * np.power(self.base, (-d + 5))
        print("Amplitude:", self.amplitude)

    def switch_region(self, region):
        return self.__getattribute__('force_'+str(region))()

    def force_E(self):
        print('Obstacle E')
        return np.array([0.0, -self.amplitude, 0.0])

    def force_NE(self):
        print('Obstacle NE')
        return np.array([-self.amplitude / 2, -self.amplitude / 2, 0.0])

    def force_N(self):
        print('Obstacle N')
        return np.array([-self.amplitude, 0.0, 0.0])

    def force_NO(self):
        print('Obstacle N0')
        return np.array([-self.amplitude / 2, self.amplitude / 2, 0.0])

    def force_O(self):
        print('Obstacle O')
        return np.array([0.0, self.amplitude / 2, 0.0])

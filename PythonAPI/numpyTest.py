import numpy as np
import time
import math

class Test:
    def switch_region(self, region):
        return self.__getattribute__('case_'+ str(region))()

    def case_1(self):
        return [1,1,1]



if __name__ == "__main__":

    a = [7, 1, 3, 4]
    b = [5, 6, 7, 8]

    min_id = np.argmin(a)
    lol = Test()
    v = lol.switch_region('1')

    print(v)
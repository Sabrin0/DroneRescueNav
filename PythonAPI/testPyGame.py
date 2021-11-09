import sys
import time

import numpy as np
import pygame
from pygame.locals import *


class joystickHandler:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Thrustmaster Control Test')
        self.screen = pygame.display.set_mode((500, 500), 0, 32)
        self.clock = pygame.time.Clock()
        self.max_vel = 100
        self.my_controller = pygame.joystick.Joystick(1)
        self.my_throttle = pygame.joystick.Joystick(0)
        self.my_base = pygame.joystick.Joystick(2)
        pygame.joystick.init()
        # joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        self.pointer = pygame.Rect(50, 50, 50, 50)
        self.pointer_color = 0
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.motion = [0, 0]
        self.mapping = {
            'hat': 'altitude',
        }

        self.active = {command: False for command in self.mapping.values()}

        # print('num axis: ', my_throttle.get_numaxes())
        # print('num hat: ', my_throttle.get_numhats())

        # print('num axis JOY: ', my_controller.get_numaxes())

    def feature_scaling(self, input):
        current_vel = (input - 1) * 100 / (-2)
        return current_vel

    def play(self):
        while True:

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, self.colors[self.pointer_color], self.pointer)
            # for idx, val in enumerate(motion):
            #    #print(idx, val)

            # if abs(motion[idx]) < 0.1:
            #    motion[idx] = 0

            # horizontal_axis = my_controller.get_axis(1)
            # vertical_axis = my_controller.get_axis(0)
            self.t_axis = self.my_throttle.get_axis(1)
            # print(my_throttle.get_numaxes())
            self.hat = self.my_controller.get_hat(0)
            self.restart = self.my_controller.get_button(0)
            self.base_control = self.my_base.get_axis(0)
            # pointer.x = hat[0]*10
            # pointer.y = hat[1]*10
            self.pointer.y = self.motion[1]
            #print('motion: ', self.motion[1])

            '''
            if abs(vertical_axis) > 0.05 and abs(horizontal_axis) > 0.05:
        
                print('H ', horizontal_axis)
                print('V ', my_controller.get_axis(0))
            
            '''
            #time.sleep(1)
            #print(self.t_axis)


            for event in pygame.event.get():
                #print(event)
                if event.type == JOYAXISMOTION:
                    print(event)
                if event.type == JOYHATMOTION:
                    print(event)

                if event.type == JOYBUTTONDOWN:  # and event.button == 0:
                    print(event)
                    print(event.button)
                    # pointer_color = (pointer_color + 1) % len(colors)
                # if event.type == JOYAXISMOTION and abs(event.value) > 0.04:
                # if np.abs(t_axis) > 0.04:
                # motion[1] = t_axis
                # print(event)
                # if event.axis < 2:
                #   motion[event.axis] = event.value
                # print('go')
                if event.type == JOYBUTTONUP:  # and event.button == 0:
                    print('stop')
                '''
                if event.type == JOYHATMOTION:
                    # motion[event.axis] = event.value
                    if event.value[1] == 1:
                        print('up')
                        motion = event.value
                    print(motion)
                    print('hat: ', event.hat)
                    print('value: ', event.value)
                '''

                if self.hat[1] != 0:
                    self.active[self.mapping['hat']] = True
                else:
                    self.active[self.mapping['hat']] = False

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if self.active['altitude']:
                self.motion[1] += 1
            else:
                self.motion[1] = 0
            if self.t_axis < 0.9:
                output = self.feature_scaling(self.t_axis)
            else:
                output = 0.0
            #print(self.restart)
            #print('current value: ', output)
            pygame.display.update()
            self.clock.tick(60)




if __name__ == '__main__':
    test = joystickHandler()
    test.play()

__author__ = 'Jack'

from math import *
import random

class SimulatedAnealing(object):
    def __init__(self):
        self.r = 0.9
        self.fun = 'sin(x)+x**0.5'
        self.boundary = [0, 10]
        self.T = [1000, 1]

    def main(self):
        x1 = random.random()*(self.boundary[1]-self.boundary[0])+self.boundary[0]
        temperature = self.T[0]
        while temperature>self.T[1]:
            derta = temperature*(self.boundary[1]-self.boundary[0])/self.T[0]
            if random.random()>0.5:
                x2 = x1+derta
            else:
                x2 = x1-derta
            if x2>self.boundary[1]:
                x2 = self.boundary[1]
            elif x2<self.boundary[0]:
                x2 = self.boundary[0]
            x = x1
            vx1 = eval(self.fun)
            x = x2
            vx2 = eval(self.fun)
            if vx2>vx1:
                x1 = x2
            else:
                p = exp((vx2-vx1)/0.0001*temperature)
                if p > random.random():
                    x1 = x2
            temperature = temperature*self.r
            print 'the temperature is ', temperature
            print 'the x value is ', x1

SA = SimulatedAnealing()
SA.main()
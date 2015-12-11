__author__ = 'Jack'

from random import *

class GeneticAlgorithm(object):
    def __init__(self):
        self.a = 5

    #start with number, dimension of vector, boundary of every interactive
    def start(self,Number,boundaries):
        boundary = [-100,100]
        generation = []
        individual = []
        for i in range(0,Number):
            for j in range(0,len(boundaries)):
                if boundaries[j][0]==0 and boundaries[j][1]==0:
                    individual[j] = uniform(boundary[0],boundary[1])
                else:
                    individual[j] = uniform(boundaries[j][0],boundaries[j][1])
            generation.append(individual)
        return generation

    #
    # def fitness(self,generation,functions):
    #     f = []
    #     for individual in generation:
    #
    #
    # def choosing(self,generation):
    #     for individual in generation:
    #
    #










boundaries = [[1,2],[3,4],[5,6]]
print len(boundaries[0])
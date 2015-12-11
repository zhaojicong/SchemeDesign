# -*- coding: utf-8 -*-

__author__ = 'Jack'
import wx
from math import *
import random

class GeneticAlgorithm(object):
    def __init__(self, functions, variableboundaries, algorithmInfo):
        self.functions = []
        self.variableboundaries = []
        self.algorithmInfo = []
        self.generation = []
        self.variables = []
        self.fitness = []
        self.process = 0
        for key in functions.keys():
            self.functions.append(functions.get(key))
        print self.functions
        for key in variableboundaries.keys():
            self.variableboundaries.append(variableboundaries.get(key))
        if algorithmInfo[0]=='Genetic Algorithm':
            try:
                self.groupSize = int(algorithmInfo[1][0])
                self.iteration = int(algorithmInfo[1][1])
                self.pcrossover = float(algorithmInfo[1][2])
                self.pmutation = float(algorithmInfo[1][3])
            except:
                wx.MessageBox('Genetic Algorithm is well set!', 'Error', wx.OK | wx.ICON_INFORMATION)
                return
        self.variableNumber = len(self.variableboundaries)
        self.objectiveNumber = len(self.functions)

    # output containning  tail
    def Initiate(self):
        for i in range(0, self.groupSize):
            individual = []
            for boundary in self.variableboundaries:
                individual.append(random.uniform(boundary[0], boundary[1]))
            self.generation.append(individual)
        self.Fitness()

    # let generation have tail
    def Fitness(self):
        try:
            self.fitness = []
            for x in self.generation:
                individualFitness = []
                for function in self.functions:
                    for i in range(1, self.variableNumber+1):
                        function = function.replace('x'+str(i), 'x['+str(i-1)+']')
                    individualFitness.append(eval(function))
                self.fitness.append(individualFitness)
            for i in range(0, self.groupSize):
                for j in range(0, self.objectiveNumber):
                    self.generation[i].append(self.fitness[i][j])
        except:
            print 'Calculating fitness error!'
            pass

    # input and output contain fitness tail, output individual number is limited
    def ChoosePareto(self):
        newgeneration = []
        for i in range(0, self.objectiveNumber):
            self.generation.sort(key=lambda x: x[self.variableNumber+i])
            for j in range(0, self.groupSize):
                if i == 0:
                    self.generation[j].append([j])
                else:
                    self.generation[j][self.variableNumber+self.objectiveNumber].append(j)
        for individual in self.generation:
            ranka = individual[self.variableNumber+self.objectiveNumber]
            for newindividual in self.generation:
                if individual == newindividual:
                    continue
                rankb = newindividual[self.variableNumber+self.objectiveNumber]
                # if all rankb<=ranka:
                for i in range(0, len(ranka)):
                    if ranka[i] < rankb[i]:
                        break
                else:
                    break
            else:
                newgeneration.append(individual)
        for individual2 in newgeneration:
            individual2.pop()
        return newgeneration

    def Choose(self):
        newgeneration = self.ChoosePareto()
        self.generation = newgeneration
        length = len(newgeneration)-1
        while len(self.generation) < self.groupSize:
            i = random.randint(0, length)
            self.generation.append(newgeneration[i])

    # input has tail but output without tail
    def CrossOver(self):
        random.shuffle(self.generation)
        newgeneration = []
        for i in range(0, self.groupSize, 2):
            oldindividual1 = self.generation[i]
            oldindividual2 = self.generation[i+1]
            newindividual1 = []
            newindividual2 = []
            p = random.random()
            if p < self.pcrossover:
                for j in range(0, self.variableNumber):
                    c = random.random()
                    newindividual1.append(c*oldindividual1[j]+(1-c)*oldindividual2[j])
                    newindividual2.append((1-c)*oldindividual1[j]+c*oldindividual2[j])
                newgeneration.append(newindividual1)
                newgeneration.append(newindividual2)
            else:
                newgeneration.append(oldindividual1[:self.variableNumber])
                newgeneration.append(oldindividual2[:self.variableNumber])
        self.generation = newgeneration

    # input and output without tail
    def Mutation(self):
        for individual in self.generation:
            p = random.random()
            if p < self.pmutation:
                individual = []
                for boundary in self.variableboundaries:
                    individual.append(random.uniform(boundary[0], boundary[1]))

    def Calculate(self):
        self.Initiate()
        for i in range(0,self.iteration):
            print 'Cycle: '+str(i+1)
            self.process = i+1
            self.Choose()
            self.CrossOver()
            self.Mutation()
            self.Fitness()

    def ShowResult(self):
        newgeneration = []
        for i in range(0, self.objectiveNumber):
            group = []
            self.generation.sort(key=lambda x: x[self.variableNumber+i], reverse=True)
            for individual in self.generation[:3]:
                group.append(individual)
            newgeneration.append(group)
        return newgeneration

    def GetIteration(self):
        return self.iteration

    def GetProcess(self):
        return self.process

# testing


# functions = {1: 'x1+x2+x3', 2: 'x1**2+x2-x3', 3: 'x1*x3-x2'}
# variableboundaries = {1: [0, 10], 2: [-2, 6], 3: [4, 10]}
# algorithmInfo = ['Genetic Algorithm', [300, 100]]
# GA = GeneticAlgorithm(functions, variableboundaries, algorithmInfo)
# GA.Calculate()
# GA.ShowResult()
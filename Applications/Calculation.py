# -*- coding: utf-8 -*-

__author__ = 'Jack'
import time
import wx
from GeneticAlgorithm import GeneticAlgorithm

class Calculation(object):
    def __init__(self, objectives, variables, algorithmInfo):
        self.object = None
        self.objectives = objectives
        self.variables = variables
        self.algorithmInfo = algorithmInfo
        if self.algorithmInfo[0] == 'Genetic Algorithm':
            self.object = GeneticAlgorithm(self.objectives, self.variables, self.algorithmInfo)

    def Calculate(self):
        if self.algorithmInfo[0] == 'Genetic Algorithm':
            self.object.Calculate()

    def ChoosePareto(self):
        if self.algorithmInfo[0] == 'Genetic Algorithm':
            return self.object.ChoosePareto()
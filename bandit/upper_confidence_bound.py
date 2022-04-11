from gambler import Gambler 
import numpy as np 
from math import sqrt

class UpperConfidenceBoundGambler(Gambler):

    def __init__(self, deg_of_exploration, num_levers, id, initial=0):
        self.deg_of_exploration = deg_of_exploration 
        self.num_levers = num_levers 
        self.id = id

        self.iterations = 0
        self.times_levers_pulled = [0] * num_levers
        self.value_estimates = [initial] * num_levers
        self.upper_bounds = [float("inf")] * num_levers

    def accept_reward(self, reward, choice):
        self.iterations += 1
        self.times_levers_pulled[choice] += 1
        self.value_estimates[choice] += (1 / self.times_levers_pulled[choice]) * (reward - self.value_estimates[choice])

        for i in range(self.num_levers):
            self.upper_bounds[i] = self.value_estimates[i] + self.deg_of_exploration * sqrt(np.log(self.iterations) / self.times_levers_pulled[i]) if self.times_levers_pulled[i] > 0 else float("inf")

    def pull_lever(self):
       
        choice = np.argmax(self.upper_bounds)

        return choice 
from gambler import Gambler 
import numpy as np 
import copy

"""
Gambler that balances exploitation and exploration, considering recent rewards more strongly.

"""
class UnbiasedRecency(Gambler):

    def __init__(self, epsilon, num_levers, id, stepsize=0.1):
        self.epsilon = epsilon 
        self.num_levers = num_levers 
        self.id = id
        self.const_stepsize = stepsize
        self.steptraces = [0] * num_levers

        self.times_levers_pulled = [0] * num_levers
        self.value_estimates = [0] * num_levers

    def accept_reward(self, reward, choice):
        self.times_levers_pulled[choice] += 1

        self.steptraces[choice] += self.const_stepsize * (1 - self.steptraces[choice])
        stepsize = self.const_stepsize / self.steptraces[choice]
        self.value_estimates[choice] += stepsize * (reward - self.value_estimates[choice])

    def pull_lever(self):
        p = np.random.uniform()
        greedy = (p > self.epsilon)
        
        if greedy:
            choice = np.argmax(self.value_estimates)
        else:
            choice = np.random.choice(self.num_levers)

        return choice 
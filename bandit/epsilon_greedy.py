from gambler import Gambler 
import numpy as np 

class EpsilonGreedy(Gambler):

    def __init__(self, epsilon, num_levers, id):
        self.epsilon = epsilon 
        self.num_levers = num_levers 
        self.id = id

        self.times_levers_pulled = [0] * num_levers
        self.value_estimates = [0] * num_levers

    def accept_reward(self, reward, choice):
        #print(reward)
        #print(choice)
        self.times_levers_pulled[choice] += 1
        self.value_estimates[choice] += (1 / self.times_levers_pulled[choice]) * (reward - self.value_estimates[choice])
        #print(self.value_estimates)

    def pull_lever(self):
        p = np.random.uniform()
        greedy = (p > self.epsilon)
        
        if greedy:
            choice = np.argmax(self.value_estimates)
        else:
            choice = np.random.choice(self.num_levers)

        return choice 
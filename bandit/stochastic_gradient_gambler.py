from gambler import Gambler 
import numpy as np 

class StochasticGradientGambler(Gambler):

    def __init__(self, preference_step_size, num_levers, id, stationary=True, expectation_step_size=0.1):
        self.preference_step_size = preference_step_size
        self.num_levers = num_levers 
        self.id = id
        self.stationary = stationary
        self.expectation_step_size = expectation_step_size

        self.iterations = 0
        self.expected_reward = 0
        self.preferences = [0] * num_levers
        self.probabilities = [1 / num_levers] * num_levers

    def accept_reward(self, reward, choice):
        self.iterations += 1
        if self.iterations == 1:
            self.average_reward = reward

        # Update lever preference in light of new reward
        for i in range(self.num_levers):
            if i == choice:
                self.preferences[i] += self.preference_step_size * (reward - self.average_reward) * (1 - self.probabilities[i])
            else:
                self.preferences[i] -= self.preference_step_size * (reward - self.average_reward) * self.probabilities[i]

        # Compute lever probabilities from preferences using a Boltzmann distribution
        exp_preferences = [np.exp(H) for H in self.preferences]
        exp_pref_sum = np.sum(exp_preferences)
        self.probabilities = [np.exp(self.preferences[i]) / exp_pref_sum for i in range(self.num_levers)]

        # Update expected reward
        if self.stationary:
            self.expected_reward += (1 / self.iterations) * (reward - self.expected_reward)
        else:
            self.expected_reward += self.expectation_step_size * (reward - self.expected_reward)

    def pull_lever(self):
       
        choice = np.random.choice(self.num_levers, p=self.probabilities)

        return choice 
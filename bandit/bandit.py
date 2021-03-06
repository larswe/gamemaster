from epsilon_greedy import EpsilonGreedy
from epsilon_recency import EpsilonRecency
from unbiased_recency import UnbiasedRecency
from upper_confidence_bound import UpperConfidenceBoundGambler
from stochastic_gradient_gambler import StochasticGradientGambler

import numpy as np 
import matplotlib.pyplot as plt
import copy

class Bandit:

    def __init__(self, num_levers):

        self.means = [None] * num_levers

        for i in range(num_levers):
            mean = np.random.normal(loc=0, scale=1)
            self.means[i] = mean
        
        self.best_lever = np.argmax(self.means)


    def get_reward(self, lever):
        return np.random.normal(loc=self.means[lever], scale=1)

"""
Run the k-armed bandit experiment.

:param num_levers: Number of levers.
:param num_iterations: Amount of times the gambler gets to pull a lever.
:param num_problems: Amount of times the experiment is repeated.
:param stationary: Whether the lever distributions stay constant during the bandit's lifetime.
"""
def main(num_levers=10, num_iterations=2000, num_problems=500, stationary=True):

    # Init gamblers
    greed = EpsilonGreedy(1/16, num_levers, 'e-greedy')
    greed_opt = EpsilonGreedy(1/16, num_levers, 'e-greedy optimist', initial=5)
    ucb = UpperConfidenceBoundGambler(0.75, num_levers, "UCB")
    sgd = StochasticGradientGambler(0.25, num_levers, 'SGD')
    # recent = EpsilonRecency(0.1, num_levers, 'e = 0.1, a = 0.1', stepsize=0.1)
    # stoc_recent = StochasticGradientGambler(0.1, num_levers, 'SGD, a = 0.1, recent', stationary=False)
    
    gambler_prototypes = copy.deepcopy([greed, greed_opt, ucb, sgd])

    # Prepare statistics
    total_reward = {}
    average_rewards = {}
    optimal_counts = {}
    for gambler in gambler_prototypes:
        total_reward[gambler.id] = 0
        average_rewards[gambler.id] = [0] * num_iterations
        optimal_counts[gambler.id] = [0] * num_iterations

    for problem in range(num_problems):

        # Init bandit 
        bandit = Bandit(num_levers)

        # Init gamblers for iteration
        gamblers = copy.deepcopy(gambler_prototypes)

        for step in range(num_iterations):
            # Pull levers
            for gambler in gamblers:
                lever = gambler.pull_lever()
                reward = bandit.get_reward(lever)
                gambler.accept_reward(reward, lever)

                # Update statistics
                total_reward[gambler.id] += reward
                average_rewards[gambler.id][step] += (1 / (problem + 1)) * (reward - average_rewards[gambler.id][step])
                if lever == bandit.best_lever:
                    optimal_counts[gambler.id][step] += 1
            
            # Update bandit
            if not stationary:
                for i in range(num_levers):
                    random_inc = np.random.normal(loc=0, scale=0.01)
                    bandit.means[i] += random_inc

    
    # Plot average reward
    for gambler_id in [g.id for g in gambler_prototypes]:
        plt.plot(range(1, num_iterations+1), average_rewards[gambler_id], label=gambler_id)
        print(f"Gambler {gambler_id} received an average reward of {total_reward[gambler_id] / (num_iterations*num_problems)} per step.")
    plt.title("Average gambler performance over time")
    plt.ylim(0, 2)
    plt.ylabel("Average reward")
    plt.xlim(1, num_iterations)
    plt.xlabel("Step")
    plt.legend()
    plt.show()

    print()

    # Plot optimal actions
    for gambler_id in [g.id for g in gambler_prototypes]:
        plt.plot(range(1, num_iterations+1), np.true_divide(optimal_counts[gambler_id], num_problems), label=gambler_id)
        print(f"Gambler {gambler_id} chose the optimal lever {np.sum(optimal_counts[gambler_id]) / (num_iterations * num_problems)} of the time.")
    plt.title("Gambler accuracy over time")
    plt.ylim(0, 1)
    plt.ylabel("Optimal action ratio")
    plt.xlim(1, num_iterations)
    plt.xlabel("Step")
    plt.legend()
    plt.show()
   

if __name__ == "__main__":
    main()

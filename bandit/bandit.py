from epsilon_greedy import EpsilonGreedy
import numpy as np 
import matplotlib.pyplot as plt
import copy

class Bandit:

    def __init__(self, num_levers):

        self.means = [None] * num_levers

        for i in range(num_levers):
            mean = np.random.normal(loc=0, scale=1)
            self.means[i] = mean


    def get_reward(self, lever):
        return np.random.normal(loc=self.means[lever], scale=1)

def main(num_levers=10, num_iterations=2000, num_problems=1000):

    # Init gamblers
    greed = EpsilonGreedy(0, num_levers, 'e = 0')
    hundredth = EpsilonGreedy(0.005, num_levers, 'e = 0.005')
    tenth = EpsilonGreedy(0.1, num_levers, 'e = 0.1')
    gambler_prototypes = copy.deepcopy([greed, hundredth, tenth])

    # Prepare statistics
    total_reward = {}
    average_rewards = {}
    for gambler in gambler_prototypes:
        total_reward[gambler.id] = 0
        average_rewards[gambler.id] = [0] * num_iterations

    for problem in range(num_problems):

        # Init bandit 
        bandit = Bandit(num_levers)

        # Init gamblers for iteration
        gamblers = copy.deepcopy(gambler_prototypes)

        for step in range(num_iterations):
            for gambler in gamblers:
                lever = gambler.pull_lever()
                reward = bandit.get_reward(lever)
                gambler.accept_reward(reward, lever)

                # Update statistics
                total_reward[gambler.id] += reward
                average_rewards[gambler.id][step] += (1 / (problem + 1)) * (reward - average_rewards[gambler.id][step])

        #print(f"You have received a total reward of {total_reward} over {num_iterations} iterations.")
        #print(f"That makes for an average reward of {total_reward / num_iterations}")

    
    # Plot results
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
   

if __name__ == "__main__":
    main()

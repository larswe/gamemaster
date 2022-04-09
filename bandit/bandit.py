from greedy import Greedy 
import numpy as np 

class Bandit:

    def __init__(self, num_levers):

        self.means = [None] * num_levers

        for i in range(num_levers):
            mean = np.random.normal(loc=0, scale=1)
            self.means[i] = mean


    def get_reward(self, lever):
        return np.random.normal(loc=self.means[lever], scale=1)

def main(num_levers=10, num_iterations=20):

    # Init bandit 
    bandit = Bandit(num_levers)

    # Init gambler 
    greed = Greedy(num_levers)

    # Prepare statistics
    total_reward = 0

    for _ in range(num_iterations):
        lever = greed.pull_lever()
        reward = bandit.get_reward(lever)
        greed.accept_reward(reward)
        print(reward)
        total_reward += reward

    print(f"You have received a total reward of {total_reward} over {num_iterations} iterations.")
   

if __name__ == "__main__":
    main()
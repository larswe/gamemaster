from gambler import Gambler 

class MyGambler(Gambler):

    def __init__(self, num_levers, id):
        self.num_levers = num_levers # TODO - Fill in, probably
        self.id = id

    """
    Process the reward received after pulling a lever.

    :param reward: Reward received on the previous iteration
    :param choice: Index of lever pulled on previous iteration
    """
    def accept_reward(self, reward, choice):
        pass # TODO - Fill in

    """
    Pull a lever.
    
    :returns: Index (0 <= i < self.num_levers) to pull next.
    """
    def pull_lever(self):
        return 0 # TODO - Fill in
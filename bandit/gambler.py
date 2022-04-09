from abc import ABC, abstractmethod

class Gambler(ABC):
    def __init__(self, num_levers):
        self.num_levers = num_levers

    @abstractmethod
    def accept_reward(self, R):
        pass

    @abstractmethod
    def pull_lever(self):
        pass 
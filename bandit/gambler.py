from abc import ABC, abstractmethod

class Gambler(ABC):

    @abstractmethod
    def accept_reward(self, R):
        pass

    @abstractmethod
    def pull_lever(self):
        pass    
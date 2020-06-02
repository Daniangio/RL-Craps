import numpy as np


class Dice:
    POSSIBLE_OUTCOMES = range(1, 7)

    def __init__(self):
        self.lastOutcome = 1

    def throw(self):
        self.lastOutcome = np.random.randint(Dice.POSSIBLE_OUTCOMES[0], Dice.POSSIBLE_OUTCOMES[-1])

    def getResult(self):
        return self.lastOutcome

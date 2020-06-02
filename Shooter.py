from typing import List

from Dice import Dice


class Shooter:
    DICES_NUMBER: int = 2

    def __init__(self, dices: List[Dice]) -> None:
        self.dices = dices

    def throwDices(self, manual: bool):
        for index, dice in enumerate(self.dices, start=1):
            if not manual:
                dice.throw()
            else:
                result = input("Dice {}: ".format(index))
                dice.lastOutcome = int(result)

from enum import Enum


class BetBase:

    def __init__(self, name, value: float):
        self.name = name
        self.value = value
        self.bettingOdds = 1.0

    def getName(self):
        return self.name

    def getWinningAmount(self):
        return self.value * self.bettingOdds

    def isWinning(self, model):
        pass

    def isLoosing(self, model):
        pass


class PassLine(BetBase):

    def __init__(self, value: float) -> None:
        super(PassLine, self).__init__(name=PossibleBets.PASS_LINE, value=value)
        self.bettingOdds = 2.0

    def isWinning(self, model):
        from Game.Model import BetResult
        return model.lastBetResult.__contains__(BetResult.NATURAL) or model.lastBetResult.__contains__(BetResult.SCORE)

    def isLoosing(self, model):
        from Game.Model import BetResult
        return model.lastBetResult.__contains__(BetResult.CRAPS) or model.lastBetResult.__contains__(
            BetResult.SEVEN_OUT)


class DontPassLine(BetBase):

    def __init__(self, value: float) -> None:
        super(DontPassLine, self).__init__(name=PossibleBets.DONT_PASS_LINE, value=value)
        self.bettingOdds = 2.0

    def isWinning(self, model):
        from Game.Model import BetResult
        if model.lastBetResult.__contains__(BetResult.PUSH):
            self.bettingOdds = 1.0
        return model.lastBetResult.__contains__(BetResult.CRAPS) or model.lastBetResult.__contains__(
            BetResult.SEVEN_OUT)

    def isLoosing(self, model):
        from Game.Model import BetResult
        return model.lastBetResult.__contains__(BetResult.NATURAL) or model.lastBetResult.__contains__(BetResult.SCORE)


class Field(BetBase):

    def __init__(self, value: float) -> None:
        super(Field, self).__init__(name=PossibleBets.FIELD, value=value)
        self.bettingOdds = 2.0

    def isWinning(self, model):
        from Game.Model import BetResult
        if model.lastBetResult.__contains__(BetResult.FIELD_DOUBLE):
            self.bettingOdds = 3.0
        elif model.lastBetResult.__contains__(BetResult.FIELD_TRIPLE):
            self.bettingOdds = 4.0
        return model.lastBetResult.__contains__(BetResult.FIELD)

    def isLoosing(self, model):
        return not self.isWinning(model)


class Bets:

    def __init__(self):
        self.bets = []

    def addBets(self, bets):
        self.bets.extend(bets)

    def removeBet(self, bet):
        self.bets.remove(bet)


class PossibleBets(Enum):
    STAY = 0
    PASS_LINE = 1
    DONT_PASS_LINE = 2
    FIELD = 4

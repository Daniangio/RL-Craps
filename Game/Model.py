from enum import Enum

from Bets import Bets
from Game.GameMVC import GamePhase
from Dice import Dice
from Player import Player
from Shooter import Shooter


class GameModel:

    def __init__(self, manual):
        self.view = None
        self.dices = [Dice() for _ in range(Shooter.DICES_NUMBER)]
        self.shooter = Shooter(self.dices)
        self.player = Player(manual, self)
        self.active_bets = Bets()
        self.previous_active_bets = self.active_bets.bets.copy()
        self.gamePhase = GamePhase.INITIAL_BET
        self.score = 0
        self.previous_score = 0
        self.lastBetResult = []

    def setView(self, view):
        self.view = view

    def getShooter(self):
        return self.shooter

    def getBets(self):
        return self.active_bets.bets

    def removeBet(self, bet):
        return self.active_bets.removeBet(bet)

    def addBets(self, bets):
        self.active_bets.addBets(bets)

    def clearWinningBets(self):
        self.lastBetResult.clear()

    def computeWinningBets(self):
        if self.gamePhase == GamePhase.COME_OUT:
            self.checkIfNatural()
            self.checkIfCraps()
        if self.gamePhase == GamePhase.MID_GAME:
            self.checkIfScore()
            self.checkIfSevenOut()
            self.checkIfField()

    def getDicesTotalResult(self):
        return sum(dice.getResult() for dice in self.dices)

    def getDicesListResult(self):
        results = []
        for dice in self.dices:
            results.append(dice.getResult())
        return results

    def checkIfNatural(self):
        if self.gamePhase != GamePhase.COME_OUT:
            raise Exception("Should not check if score is Natural during {} phase".format(self.gamePhase))
        result = self.getDicesTotalResult() in [7, 11]
        if result:
            self.lastBetResult.append(BetResult.NATURAL)
        return result

    def isNatural(self):
        if self.gamePhase != GamePhase.COME_OUT:
            return False
        return self.lastBetResult.__contains__(BetResult.NATURAL)

    def checkIfCraps(self):
        if self.gamePhase != GamePhase.COME_OUT:
            raise Exception("Should not check if score is Craps during {} phase".format(self.gamePhase))
        result = self.getDicesTotalResult() in [2, 3, 12]
        if result:
            self.lastBetResult.append(BetResult.CRAPS)
            if self.getDicesTotalResult() in [12]:
                self.lastBetResult.append(BetResult.PUSH)
        return result

    def isCraps(self):
        if self.gamePhase != GamePhase.COME_OUT:
            return False
        return self.lastBetResult.__contains__(BetResult.CRAPS)

    def checkIfSevenOut(self):
        if self.gamePhase != GamePhase.MID_GAME:
            raise Exception("Should not check if score is Seven Out during {} phase".format(self.gamePhase))
        result = self.getDicesTotalResult() == 7
        if result:
            self.lastBetResult.append(BetResult.SEVEN_OUT)
        return result

    def isSevenOut(self):
        if self.gamePhase != GamePhase.MID_GAME:
            return False
        return self.lastBetResult.__contains__(BetResult.SEVEN_OUT)

    def checkIfScore(self):
        if self.gamePhase != GamePhase.MID_GAME:
            raise Exception("Should not check for Score during {} phase".format(self.gamePhase))
        result = self.getDicesTotalResult() == self.score
        if result:
            self.lastBetResult.append(BetResult.SCORE)
        return result

    def isScore(self):
        if self.gamePhase != GamePhase.MID_GAME:
            return False
        return self.lastBetResult.__contains__(BetResult.SCORE)

    def checkIfField(self):
        if self.gamePhase != GamePhase.MID_GAME:
            raise Exception("Should not check for Field during {} phase".format(self.gamePhase))
        result = self.getDicesTotalResult() in [2, 3, 4, 9, 10, 11, 12]
        if result:
            self.lastBetResult.append(BetResult.FIELD)
            if self.getDicesTotalResult() in [2]:
                self.lastBetResult.append(BetResult.FIELD_DOUBLE)
            elif self.getDicesTotalResult() in [12]:
                self.lastBetResult.append(BetResult.FIELD_TRIPLE)
        return result


class BetResult(Enum):
    NATURAL = 1
    CRAPS = 2
    PUSH = 3
    SCORE = 4
    SEVEN_OUT = 5
    FIELD = 6
    FIELD_DOUBLE = 7
    FIELD_TRIPLE = 8

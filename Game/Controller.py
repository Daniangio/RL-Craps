from Game.GameMVC import GamePhase
from Game.Model import GameModel
from Game.View import GameView


class GameController:

    def __init__(self, model: GameModel, view: GameView, manual: bool):
        self.model = model
        self.view = view
        self.manual = manual

    def runTurn(self):
        self.runComeOut()
        while not self.endingTurnCriteriaAreMet():
            self.runMidGame()
        self.endTurn()

    def placeBets(self):
        self.model.player.makeBets(self.model.gamePhase, self.model.getBets())

    def runComeOut(self):
        self.model.gamePhase = GamePhase.INITIAL_BET
        self.runPhase()

    def runMidGame(self):
        self.model.gamePhase = GamePhase.MID_GAME_BET
        self.runPhase()

    def runPhase(self):
        self.placeBets()
        if self.model.gamePhase == GamePhase.INITIAL_BET:
            self.model.gamePhase = GamePhase.COME_OUT
        else:
            self.model.gamePhase = GamePhase.MID_GAME
        self.throwDices()
        self.setScore()
        self.model.previous_active_bets = self.model.getBets().copy()
        self.redistributeWinnings()
        if self.endingTurnCriteriaAreMet():
            self.model.previous_score = self.model.score
            self.model.score = 0
        self.model.player.update_knowledge(self.model.gamePhase, self.model.previous_active_bets)

    def setScore(self):
        self.model.previous_score = self.model.score
        if self.model.gamePhase == GamePhase.COME_OUT:
            dices_result = self.model.getDicesTotalResult()
            if dices_result in [2, 3, 4, 5, 6, 8, 9, 10]:
                self.model.score = dices_result
            else:
                self.model.score = 0

    def endTurn(self):
        self.view.trace("Player wallet: {}".format(self.model.player.cash))

    def endingTurnCriteriaAreMet(self):
        if self.model.gamePhase == GamePhase.COME_OUT:
            return self.model.isNatural() or self.model.isCraps()
        elif self.model.gamePhase == GamePhase.MID_GAME:
            return self.model.isSevenOut() or self.model.isScore()
        else:
            raise Exception("Game phase {} is not a valid phase for checking"
                            "the ending turn criteria".format(self.model.gamePhase.name))

    def redistributeWinnings(self):
        self.model.clearWinningBets()
        self.model.computeWinningBets()
        hit_bets = [x for x in self.model.getBets() if (x.isWinning(self.model) or x.isLoosing(self.model))]
        remaining_bets = [x for x in self.model.getBets() if not hit_bets.__contains__(x)]
        self.model.active_bets.bets = remaining_bets
        for bet in hit_bets:
            if bet.isWinning(self.model):
                self.view.trace("{}: won {}€".format(bet.getName(), bet.getWinningAmount()))
                self.model.player.addCash(bet.getWinningAmount())
            else:
                self.view.trace("{}: lost".format(bet.getName(), bet.getWinningAmount()))

    def throwDices(self):
        self.model.getShooter().throwDices(self.manual)
        self.view.showDicesResult()

from enum import Enum


class Game:

    def __init__(self, manual: bool = False):
        from Game.Model import GameModel
        from Game.View import GameView
        from Game.Controller import GameController
        self.model = GameModel(manual)
        self.view = GameView(self.model)
        self.model.setView(self.view)
        self.controller = GameController(self.model, self.view, manual)

    def getMVC(self):
        return self.model, self.view, self.controller


class GamePhase(Enum):
    INITIAL_BET = 1
    COME_OUT = 2
    MID_GAME_BET = 3
    MID_GAME = 4

from Game.Model import GameModel


class GameView:

    def __init__(self, model: GameModel):
        self.model = model

    def showDicesResult(self):
        pass
        # print('Throw results: {}, {} -> {}'.format(*self.model.getDicesListResult(), self.model.getDicesTotalResult()))

    @staticmethod
    def trace(message: str):
        pass
        # print(message)

from Behaviours.ActionSelector import ActionSelector


class Player:

    def __init__(self, manual: bool, model):
        self.manual = manual
        self.actionSelector = ActionSelector(model)
        self.cash = 1000
        self.last_reward = 0

    def makeBets(self, game_phase, active_bets):
        if not self.manual:
            i = 0
            self.last_reward = 0
            while self.actionSelector.bet(game_phase, active_bets, i):
                active_bets_names = map(lambda x: x.name, active_bets)
                next_bet = self.actionSelector.getNextBet()
                self.last_reward = 0
                if next_bet.name not in active_bets_names:
                    self.last_reward = -self.actionSelector.getNextBet().value
                    self.cash += self.last_reward
                    active_bets.append(next_bet)
                i += 1

    def update_knowledge(self, game_phase, previous_active_bets):
        self.actionSelector.update_knowledge(game_phase, previous_active_bets, self.last_reward)

    def addCash(self, value):
        self.last_reward += value
        self.cash += value

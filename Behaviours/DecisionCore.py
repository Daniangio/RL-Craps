from Bets import *


class ComeOutDecisionCore:

    def __init__(self, model):
        from DP import DynamicProgramming
        self.model = model
        self.possible_bets = [PossibleBets.STAY, PossibleBets.PASS_LINE, PossibleBets.DONT_PASS_LINE, PossibleBets.FIELD]
        self.dp = DynamicProgramming(model, self.possible_bets)
        self.state_value = {}
        self.last_action = PossibleBets.STAY
        self.current_state = 0

    def go(self, active_bets):
        self.current_state = self.dp.get_state_index((self.model.gamePhase, self.model.score, active_bets))
        self.last_action = self.dp.choose_action(self.current_state)
        return self.last_action

    def update_knowledge(self, previous_active_bets, last_reward):
        previous_state = self.dp.get_state_index((self.model.gamePhase, self.model.previous_score, previous_active_bets))
        next_state = self.dp.get_state_index((self.model.gamePhase, self.model.score, self.model.getBets()))
        self.dp.update_occurrence(previous_state, next_state, self.last_action)
        self.dp.update_rewards(previous_state, next_state, last_reward)
        self.dp.update_policy(previous_state)

    def getNextBet(self, active_bets):
        action = self.go(active_bets)
        if action == 0: return None
        if action == 1: return PassLine(1)
        if action == 2: return DontPassLine(1)
        if action == 3: return Field(1)


class MidGameDecisionCore:

    def __init__(self):
        pass

    def getNextBet(self, active_bets):
        if len(active_bets) > 1:
            return None
        return Field(5)

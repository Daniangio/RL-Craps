from Behaviours.DecisionCore import ComeOutDecisionCore, MidGameDecisionCore


class ActionSelector:

    def __init__(self, model):
        self.nextBet = None
        self.comeOutDecisionCore = ComeOutDecisionCore(model)
        # self.midGameDecisionCore = MidGameDecisionCore()

    def bet(self, game_phase, active_bets, number_of_bets_made_this_round):
        from Game.GameMVC import GamePhase
        if number_of_bets_made_this_round > 0:
            return False
        if game_phase == GamePhase.INITIAL_BET:
            bet = self.comeOutDecisionCore.getNextBet(active_bets)
            self.nextBet = bet
            if bet is None:
                return False
        elif game_phase == GamePhase.MID_GAME_BET:
            bet = self.comeOutDecisionCore.getNextBet(active_bets)
            self.nextBet = bet
            if bet is None:
                return False
        else:
            raise Exception("Should not make bets during {} phase".format(game_phase))
        return True

    def update_knowledge(self, game_phase, previous_active_bets, last_reward):
        from Game.GameMVC import GamePhase
        if game_phase == GamePhase.COME_OUT:
            self.comeOutDecisionCore.update_knowledge(previous_active_bets, last_reward)
        elif game_phase == GamePhase.MID_GAME:
            self.comeOutDecisionCore.update_knowledge(previous_active_bets, last_reward)

    def getNextBet(self):
        return self.nextBet

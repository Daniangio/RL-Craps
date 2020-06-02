from Game.GameMVC import GamePhase
from Game.Model import GameModel
import numpy as np
import itertools

from Game.View import GameView


def map_state_x_to_index(game_phase):
    if game_phase == GamePhase.INITIAL_BET or game_phase == GamePhase.COME_OUT:
        return 0
    if game_phase == GamePhase.MID_GAME_BET or game_phase == GamePhase.MID_GAME:
        return 1
    raise Exception("Game phase {} is not mapped".format(game_phase))


def map_state_y_to_index(score):
    if score == 0: return 0
    if score == 2: return 1
    if score == 3: return 2
    if score == 4: return 3
    if score == 5: return 4
    if score == 6: return 5
    if score == 8: return 6
    if score == 9: return 7
    if score == 10: return 8
    raise Exception("Score {} is not mapped".format(score))


def map_state_z_to_index(bets):
    if len(bets) == 0:
        return 0
    index = 0
    for bet in bets:
        index += bet.name.value
    return index


class DynamicProgramming:

    def __init__(self, model: GameModel, possible_bets):
        self.model = model
        self.possible_bets = possible_bets
        self.state_x = [GamePhase.INITIAL_BET, GamePhase.MID_GAME_BET]  # Game phase
        self.state_y = [0, 2, 3, 4, 5, 6, 8, 9, 10]  # Score
        self.state_z = list(range(2 ** len(self.possible_bets)))  # Active bets
        self.number_of_states = len(self.state_x) * len(self.state_y) * len(self.state_z)
        self.reward_map = self.create_reward_map()
        self.occurrence_map = self.create_occurrence_map()
        self.policy = self.create_policy()
        self.epsilon = 0.2

    def save_on_file(self):
        np.savetxt("reward_map.csv", np.asarray(self.reward_map).reshape((self.number_of_states, self.number_of_states)), delimiter=';', fmt='%i')
        np.savetxt("occurrence_map.csv", np.asarray(self.occurrence_map).reshape((-1, len(self.possible_bets))), delimiter=';', fmt='%i')
        np.savetxt("policy.csv", np.asarray(self.policy).reshape((self.number_of_states, len(self.possible_bets))), delimiter=';', fmt='%d')

    def choose_action(self, state):
        row = self.policy[state,]
        max_index = np.where(row == np.max(row))[0]
        if max_index.shape[0] > 1:
            max_index = int(np.random.choice(max_index, size=1))
        else:
            max_index = int(max_index)
        if np.random.random() < self.epsilon:
            epsilon_row = [x for i, x in enumerate(row) if i != max_index]
            max_index = int(np.random.choice(epsilon_row, size=1))
        GameView.trace('Action: {}'.format(max_index))
        return max_index

    def get_policy(self):
        return self.policy

    def create_reward_map(self):
        try:
            reward_map = np.loadtxt("reward_map.csv", delimiter=';')
        except:
            reward_map = np.zeros([self.number_of_states, self.number_of_states])
            for i, j in itertools.product(range(self.number_of_states), range(self.number_of_states)):
                reward_map[i, j] = -1
        return reward_map

    def update_rewards(self, state, state_prime, reward):
        self.reward_map[state, state_prime] = reward
        # GameView.trace("REWARD: {} STATE: {} STATE_PRIME: {} REWARDS: {}".format(reward, state, state_prime, self.reward_map[(self.reward_map > -1)]))

    def create_occurrence_map(self):
        try:
            occurrence_map = np.loadtxt("occurrence_map.csv", delimiter=';')
            occurrence_map = np.reshape(occurrence_map, (self.number_of_states, self.number_of_states, len(self.possible_bets)))
        except:
            occurrence_map = np.zeros([self.number_of_states, self.number_of_states, len(self.possible_bets)])
        return occurrence_map

    def get_probability_from_occurrence_map(self, state, state_prime, action):
        total_occurrences = sum(self.occurrence_map[state, :, action])
        if total_occurrences == 0:
            return 0
        return self.occurrence_map[state, state_prime, action] / total_occurrences

    def update_occurrence(self, state, state_prime, action):
        self.occurrence_map[state, state_prime, action] += 1

    def create_policy(self):
        try:
            policy = np.loadtxt("policy.csv", delimiter=';')
        except:
            policy = np.empty([self.number_of_states, len(self.possible_bets)])
            for i, j in itertools.product(range(self.number_of_states), range(len(self.possible_bets))):
                policy[i, j] = 1 / len(self.possible_bets)
        return policy

    def update_policy(self, previous_state):
        for action in range(len(self.possible_bets)):
            total_next_state_occurrence = sum(self.occurrence_map[previous_state, :, action])
            action_value: float = 0.0
            for next_state in range(self.number_of_states):
                if self.occurrence_map[previous_state, next_state, action] == 0:
                    continue
                action_value += self.occurrence_map[previous_state, next_state, action] / total_next_state_occurrence * \
                                self.reward_map[previous_state, next_state]
            self.policy[previous_state, action] = action_value

    def get_state_index(self, state):
        x = map_state_x_to_index(state[0])
        y = map_state_y_to_index(state[1])
        z = map_state_z_to_index(state[2])
        # print("x: {} - {} y: {} - {} z: {} - {}".format(state[0], x, state[1], y, state[2], z))
        return x + len(self.state_x) * (y + len(self.state_y) * z)

    def iterative_policy_evaluation(self, policy, action, theta=0.1, discount_rate=0.5):
        V_s = {i: 0 for i in range(self.number_of_states)}

        delta = 100

        while not delta < theta:
            delta = 0
            for state in range(self.number_of_states):
                v = V_s[state]

                action_total = 0
                for state_prime in range(self.number_of_states):
                    action_total += self.get_probability_from_occurrence_map(state, state_prime, action) * (
                            self.reward_map[(state, state_prime)] + discount_rate * V_s[state_prime])

                total = policy[state, action] * action_total

                V_s[state] = round(total, 1)
                delta = max(delta, abs(v - V_s[state]))
        return V_s

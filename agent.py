import torch
import random
import numpy as np
from collections import deque
from game import TicTacToeAI

from config import *

class Player:
    def __init__(self, symbol):
        self.symbol = symbol


class Human(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def get_action(self, game):
        while True:
            action = input(f"{self.symbol}, Enter a number from 0 to 8: ")
            if action.isdigit():
                action = int(action)
                if 0 <= action <= 8:
                    row, column = game.getIndeces(action)
                    if game.isValidMove(row, column):
                        return action
            print("Invalid move. Try again.")

class Computer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)

        self.previous_state = None
        self.previous_action = None
        self.reward = None
        self.next_state = None

    def get_state(self, game):
        state = np.array(game.board).reshape(1, 9)
        return state

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        if self.previous_state = None:
            self.previous_state = state

        else:
            self.next_state = state
            self.remember(self.previous_state, self.previous_action, self.reward, self.next_state, False)

        pass
            
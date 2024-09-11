import torch
import random
import numpy as np
from collections import deque
from game import TicTacToeAI
from model import Linear_QNet, QTrainer

from config import *

class Player:
    def __init__(self, symbol):
        self.symbol = symbol


class Human(Player):
    def __init__(self, symbol):
        super().__init__(symbol)

    def make_move(self, game):
        valid_moves = game.get_valid_moves()
        print("Valid moves: ", valid_moves)
        index = int(input(f"{self.symbol}, Enter a number from 0 to 8: "))
        while index not in valid_moves:
            print("Invalid move. Try again.")
            index = int(input(f"{self.symbol}, Enter a number from 0 to 8: "))
        game.play_step(index, self.symbol)

        

class Computer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.score = 0
        self.frame = 0
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(9, 256, 9)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        self.previous_state = None
        self.previous_action = None
        self.reward = None
        self.next_state = None
        self.next_action = None

    def get_state(self, game):
        state = np.array(game.board).reshape(1, 9)
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)


    def train_short_memory(self):
        state, action, reward, next_state, done = self.memory[-1]
        self.trainer.train_step(state, action, reward, next_state, done)

    def make_move(self, game):
        #first move
        if self.frame == 0:
            self.previous_state = game.get_state()
            valid_moves = game.get_valid_moves()
            self.previous_action = self.get_action(self.previous_state, valid_moves)
            reward, game_over, score = game.play_step(self.previous_action, self.symbol)
            self.reward = reward
        #all other moves
        else:
            #get next state, action, reward and update previous SARSA tuple
            self.next_state = game.get_state()
            valid_moves = game.get_valid_moves()
            action = self.get_action(self.next_state, valid_moves)
            reward, game_over, score = game.play_step(action, self.symbol)
            self.reward = reward

            self.remember(self.previous_state, self.previous_action, self.reward, self.next_state, game_over)
        
            self.train_short_memory()

            self.previous_state = self.next_state
            self.previous_action = action
        
        self.score += score
        self.frame += 1

        if game_over:
            game.drawBoard()
            if game.is_draw():
                print("Game over! It's a draw.")
            else:
                print(f"Game over! {self.symbol} wins!")
            self.train_long_memory()
            self.n_games += 1
            self.frame = 0
            game.reset()
            print("Game reset")

        return game_over
             

    def get_action(self, state, valid_moves):
        index = -1
        while index not in valid_moves:
            self.epsilon = 80 - self.n_games
            final_move = [0,0,0,0,0,0,0,0,0]
            if random.randint(0, 200) < self.epsilon:
                move = random.randint(0, 8)
                final_move[move] = 1
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)
                move = torch.argmax(prediction).item()
                final_move[move] = 1

            index = np.where(np.array(final_move) == 1)[0][0]

        return index
    

def main():
    game = TicTacToeAI()
    game_over = False
    player1 = Computer('X')
    player2 = Computer('O')
    print("Starting game...")
    for x in range(50):
        print("Starting game", x)
        while not game_over:
            game_over = player1.make_move(game)
            game_over = player2.make_move(game)
        game_over = False

    player1 = Human('X')
    for x in range(3):
        while not game_over:
            game.drawBoard()
            game_over = player1.make_move(game)
            game.drawBoard()
            print("AI making move...")
            game_over = player2.make_move(game)
    
main()
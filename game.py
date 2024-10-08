import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np

class TicTacToeAI:
    def __init__(self):
        # Initialize the 3x3 board, represented as a list of lists
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def reset(self):
        # Reset the board to empty
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.frame_iteration = 0

    def play_step(self, action : list, symbol) -> tuple:
        """
        Take an action and update the game state.
        Returns reward, game_over, and current score.
        """
        row, column = self.getIndeces(action)
        if self.isValidMove(row, column):
            self.board[row][column] = symbol
            if self.check_winner(symbol):
                return 1, True, 1
            if self.is_draw():
                return 0, True, 0
            return 0, False, 0  # No reward for continuing
        
        return 0, False, 0  # No reward for continuing
    
    def getIndeces(self, action):
        return action // 3, action % 3
    
    def isValidMove(self, row, column):
        if self.board[row][column] == ' ':
            return True
        return False

    def check_winner(self, player):
        return self.checkRows() or self.checkColumns() or self.checkDiagonals()

    def checkRows(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return True
        return False
    
    def checkColumns(self):
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return True
        return False
    
    def checkDiagonals(self):
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def is_draw(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True
    
    def drawBoard(self):
        for x in range(3):
            row = self.board[x] 
            line = ""
            for cell in row:
                line += cell + " | "
            print(line[:-2])
            if x < 2:
                print("-" * 10)

    def get_state(self):
        board = []
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    board.append(0)
                elif cell == 'X':
                    board.append(1)
                else:
                    board.append(-1)
        board = np.array(board)
        return board
    
    def get_valid_moves(self):
        valid_moves = []
        for i in range(9):
            row, col = self.getIndeces(i)
            if self.isValidMove(row, col):
                valid_moves.append(i)
        return valid_moves
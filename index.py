from game import TicTacToeAI
from agent import Computer, Human

def main():
    # Initialize the game
    game = TicTacToeAI()
    game_over = False
    game.reset()
    
    # Initialize the players
    player1 = Human('X')
    player2 = Human('O')
    
    # Main game loop
    while not game_over:
        # Player 1's turn
        game.drawBoard()
        action = player1.get_action(game)
        reward, game_over, score = game.play_step(action, player1.symbol)
        if game_over:
            print("Player 1 wins!")
        
        # Player 2's turn
        game.drawBoard()
        action = player2.get_action(game)
        reward, game_over, score = game.play_step(action, player2.symbol)
        if game_over:
            print("Player 2 wins!")


if __name__ == "__main__":
    main()
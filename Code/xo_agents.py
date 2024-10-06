import numpy as np
import random
import matplotlib.pyplot as plt

class Strategy:
    """
    Base class for users to set a strategy
    Just change the select_move function
    """
    def __init__(self) -> None:
        pass

    def select_move(self,board):
        available_moves = [i for i, cell in enumerate(board) if cell == ' ']
        return random.choice(available_moves)



class TicTacToe:
    def __init__(self,player1:str = 'Player 1',player2:str = 'Player 2',player1_strat:Strategy = Strategy(),player2_strat:Strategy = Strategy()):
        # Create a 3x3 board, initialized with empty cells
        self.board = [' '] * 9
        self.current_player = 'X'
        self.player1 = player1 #This is the player  that will play the X
        self.player2 = player2
        self.player1_strat = player1_strat
        self.player2_strat = player2_strat
        self.game_trace = ''

    def __setattr__(self, name, value):
        if name in ['player1_strat','player2_strat'] and not isinstance(value, Strategy):
            raise TypeError(f"Expected instance of Strategy class, got {type(value).__name__}")
        super().__setattr__(name, value)

    def display_board(self,first=False):
        # Display the current state of the board

        if not first:
            trace = f'{self.player1 if self.current_player == 'X' else self.player2} played :'
            self.game_trace+=trace+'\n'
            print(trace)
        for i in range(0, 9, 3):
            trace = f'|   {self.board[i]}   |   {self.board[i+1]}   |   {self.board[i+2]}   |'
            self.game_trace+=trace+'\n'
            print(trace)
            if i < 6:
                trace = '-----+----+-----'
                print(trace)
                self.game_trace+=trace+'\n'
        trace = "___________________________________"
        self.game_trace+=trace+'\n'
        print(trace)

    def reset(self):
        # Reset the board for a new game
        self.board = [' '] * 9
        self.current_player = 'X'

    def is_winner(self):
        # Check all win conditions for the player
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
                        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
                        (0, 4, 8), (2, 4, 6)]             # Diagonals
        return any(self.board[i] == self.board[j] == self.board[k] == self.current_player for i, j, k in win_conditions)
    
    def is_draw(self):
        # Check if the game is a draw (no empty cells left)
        return ' ' not in self.board
    
    def make_move(self, position):
        # Place the player's marker on the board if the move is valid
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        print("This position if full")
        return False
    
    def switch_player(self):
        # Alternate between players
        self.current_player = 'O' if self.current_player == 'X' else 'X'


    def play_game(self):
        self.display_board(first=True)

        while True:
            #Player 1's move
            move1 = self.player1_strat.select_move(self.board)
            self.make_move(move1)
            self.display_board()

            if self.is_winner():
                trace = f'{self.player1} wins!'
                print(trace)
                self.game_trace+=trace
                break
            if self.is_draw():
                print('It\'s a draw!')
                break
            self.switch_player()


            #Player 2's move
            move2 = self.player2_strat.select_move(self.board)
            self.make_move(move2)
            self.display_board()

            if self.is_winner():
                trace = f'{self.player2} wins!'
                print(trace)
                self.game_trace+=trace
                break
            if self.is_draw():
                trace = "It's a draw!"
                print(trace)
                self.game_trace+=trace
                break
            self.switch_player()


    def evaluate_strategies(self, num_games=1000,plot=False):
        results = {self.player1: 0, self.player2: 0, "draws": 0}

        for _ in range(num_games):
            game = TicTacToe()
            while True:
                # Player 1 move
                move1 = self.player1_strat.select_move(game.board)
                game.make_move(move1)
                if game.is_winner():
                    results[self.player1] += 1
                    break
                if game.is_draw():
                    results["draws"] += 1
                    break
                
                # Player 2 move
                move2 = self.player1_strat.select_move(game.board)
                game.make_move(move2)
                if game.is_winner():
                    results[self.player2] += 1
                    break
                if game.is_draw():
                    results["draws"] += 1
                    break

        if plot:
            # Extract the keys and values from the dictionary
            labels = [self.player1,self.player2,'draw']
            values = list(results.values())

            # Create a bar chart
            plt.bar(labels, values, color=['blue', 'green', 'orange'])

            # Add titles and labels
            plt.title('Game Results')
            plt.xlabel('Player name')
            plt.ylabel('Count')

            # Display the plot
            plt.show()

        return results
    

if __name__=='__main__':

    game = TicTacToe()
    game.evaluate_strategies(plot=True,num_games=500)


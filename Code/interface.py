import gradio as gr
import numpy as np
import random
import matplotlib.pyplot as plt
import tempfile
import os
from xo_agents import TicTacToe,Strategy

def create_strategy(code):
    # Create a Strategy subclass with the provided select_move function
    class CustomStrategy(Strategy):
        def __init__(self):
            super().__init__()
        
        exec(code)  # This will define the select_move method

    return CustomStrategy()

def play_game(strategy1_code, strategy2_code):
    strategy1 = create_strategy(strategy1_code)
    strategy2 = create_strategy(strategy2_code)

    game = TicTacToe(player1_strat=strategy1, player2_strat=strategy2)
    game.play_game()

    return game.game_trace

def evaluate_strategies(strategy1_code, strategy2_code, num_games):
    strategy1 = create_strategy(strategy1_code)
    strategy2 = create_strategy(strategy2_code)

    game = TicTacToe(player1_strat=strategy1, player2_strat=strategy2)
    results = game.evaluate_strategies(num_games=num_games, plot=True)

    plt.close()  # Close the plot to free up memory

    return f"Results: {results}"

if __name__ == "__main__":
    # Create the Gradio interface
    with gr.Blocks() as demo:
        gr.Markdown("# Tic-Tac-Toe Strategy Tester")
        
        default_strategy = '''
"""
Your strategy should be implemented in the select_move function.
The 'board' parameter is a list of 9 elements, each being ' ', 'X', or 'O', for example = ['O',' ','O',' ','X','X',' ','O',' ']
The function should return an integer from 0-8, representing the chosen move.

Example implementation:
"""
def select_move(self,board):
    available_moves = [index for index, c in enumerate(board) if c == ' ']
    return random.choice(available_moves)
'''

        with gr.Tab("Play Game"):
            strategy1_input = gr.Code(label="Player 1 Strategy (select_move function)", 
                                      language="python", 
                                      value=default_strategy)
            strategy2_input = gr.Code(label="Player 2 Strategy (select_move function)", 
                                      language="python", 
                                      value=default_strategy)
            play_button = gr.Button("Play Game")
            game_output = gr.Textbox(label="Game Result")
        
        with gr.Tab("Evaluate Strategies"):
            strategy1_eval = gr.Code(label="Player 1 Strategy (select_move function)", 
                                     language="python", 
                                     value=default_strategy)
            strategy2_eval = gr.Code(label="Player 2 Strategy (select_move function)", 
                                     language="python", 
                                     value=default_strategy)
            num_games = gr.Slider(minimum=100, maximum=10000, step=100, label="Number of Games", value=1000)
            evaluate_button = gr.Button("Evaluate Strategies")
            eval_output = gr.Textbox(label="Evaluation Result")
        
        play_button.click(play_game, inputs=[strategy1_input, strategy2_input], outputs=game_output)
        evaluate_button.click(evaluate_strategies, inputs=[strategy1_eval, strategy2_eval, num_games], outputs=eval_output)

    demo.launch()
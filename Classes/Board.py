import numpy as np


class Board:
    def __init__(self, size):
        self.board = np.zeros([size, size])

    def make_move(self, current_location, new_location):
        # Not sure if these are the smartest parameters. I was
        # thinking if you provide for example (1,0) and (2,0)
        # it moves the piece on 1,0 -> 2,0
        pass

    def evaluate_board(self):
        # Evaluate whether or not the game is finished, and if so
        # who won
        pass

    def get_possible_moves(self):
        # Check whose turn it is, and which moves this player can make
        # using the current state of the board and the piece.possible_next_locations
        # funtion. It should not be possible to make a move to a location containing
        # another piece of the same color. Also, you should not be able to make a move
        # which puts your own king in check
        pass

    def choose_next_move(self, strategy):
        # Select a next move for a player based on their strategy and the output
        # of self.get_possible_moves
        pass

    def __str__(self):
        # Create function to nicely print state of board
        pass

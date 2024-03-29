import numpy as np
from Classes.Piece import Piece
from math import inf


class Board:
    def __init__(self, size=5, q4=False):  # Default value set to 5
        # If we're answering Q4, the pawn can move 2 spaces at the beginning

        # Declaration of the array with object as data type.
        self.board = np.ndarray((size, size), dtype=object)
        self.size = size
        self.q4 = q4

        # Initialise all values with "False" as default.
        for i in range(size):
            for j in range(size):
                self.board[i][j] = False

        self.init_figures()

    def place_figure_on_board(self, row, column, player, piece_type, limit):
        """
                Places one piece on the board.

                :param row: int             The row where the piece should be 
                                            placed.

                :param column: int          The column where the piece should
                                            be placed.

                :param player: bool         The owner of the piece (black or 
                                            white)

                :param piece_type: string   The type of the piece 
                                            (rook, king,....)

                :param piece_type: limit    Set the limit (described in the
                                            class Piece)
        """

        self.board[row][column] = Piece(player, piece_type, limit)

    def init_figures(self):
        """
                Initialises the game board according to the specification
                of mini chess for a 5x5 board
        """

        # Check if the board is indeed 5x5
        if len(self.board) != 5 or len(self.board[0]) != 5:
            print("Error: this function is only for a 5x5 board")
            return False

        # Initialise Pawns
        for i in range(5):
            self.place_figure_on_board(3, i, 1, "P", 1)
            self.place_figure_on_board(1, i, 0, "P", self.q4 + 1)

        # Initialise Rooks
        self.place_figure_on_board(4, 4, 1, "R", inf)
        self.place_figure_on_board(0, 0, 0, "R", inf)

        # Initialise Knights
        self.place_figure_on_board(4, 3, 1, "N", 1)
        self.place_figure_on_board(0, 1, 0, "N", 1)

        # Initialise Bishops
        self.place_figure_on_board(4, 2, 1, "B", inf)
        self.place_figure_on_board(0, 2, 0, "B", inf)

        # Initialise Queens
        self.place_figure_on_board(4, 1, 1, "Q", inf)
        self.place_figure_on_board(0, 3, 0, "Q", inf)

        # Initialise Kings
        self.place_figure_on_board(4, 0, 1, "K", 1)
        self.place_figure_on_board(0, 4, 0, "K", 1)

        return True

    def make_move(self, current_location, new_location):
        """
        Move a piece from current_location to new_location.
        Also update the numbers of column switches allowed for 
        the moved piece if necessary

        :param current_location: tuple of form (row, col)
        :param new_location: tuple of form (row, col)
        """
        # Check what piece we're moving
        piece_to_move = self.board[current_location]

        # Reduce the number of column switches still allowed
        # there has been a column switch
        if current_location[1] is not new_location[1]:
            piece_to_move.switches_left -= 1

        # If pawn and limit == 2 -> this was it's first move in Q4
        # so reset limit to 1
        if piece_to_move.type == "P":
            piece_to_move.limit = 1

        # Remove piece from current location
        self.board[current_location] = False

        # Place piece at new location
        self.board[new_location] = piece_to_move

        # check for pawn promotion
        if piece_to_move.type == "P":
            if new_location[0] == 0 or new_location[0] == 4:
                self.place_figure_on_board(
                    new_location[0], new_location[1], piece_to_move.player,
                    "Q", inf)
                return True

        return False

    def copy(self):  # Create a copy of the current board
        c = Board()
        c.board = self.board.copy()
        return c

    def __str__(self):
        """
            Function that returns a string which is a plotting of 
            the board.
        """

        # The colours may appear different depending on light or dark mode.
        fig_dict = {
            "0P": "♟", "1P": "♙",
            "0R": "♜", "1R": "♖",
            "0N": "♞", "1N": "♘",
            "0B": "♝", "1B": "♗",
            "0Q": "♛", "1Q": "♕",
            "0K": "♚", "1K": "♔"
        }

        # Possibility to flip the board:
        # self.board = np.flip(self.board, 0)

        ret_str = "            white\n"
        ret_str += " +-------------------------+\n"

        for i in range(len(self.board)):
            # change this to "str(4-i)" if the board is flipped"
            ret_str += str(i) + "|"
            for j in range(len(self.board)):
                if self.board[i][j]:
                    ret_str += "  "
                    ret_str += fig_dict[str(self.board[i]
                                        [j].player) + self.board[i][j].type]
                    ret_str += "  "
                else:
                    ret_str += "  ⋅  "
            ret_str += "|\n"

        ret_str += " +-------------------------+\n"
        ret_str += "            black"

        # undo the flipping if done previously.
        # self.board = np.flip(self.board, 0)

        return ret_str

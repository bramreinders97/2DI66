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
        # a little function in order to place one individual figure on the board
        self.board[row][column] = Piece(player, piece_type, limit)

    def init_figures(self):
        # Initialises the game board according to the specification of mini chess for a 5x5 board
        # Convention:
        # White     =>      rows 0 and 1
        # Black     =>      rows 3 and 4

        # Check if the board is indeed 5x5
        if len(self.board) != 5 or len(self.board[0]) != 5:
            print("Error: this function is only for a 5x5 board")
            return False

        # Initialise Pawns
        for i in range(5):
            self.place_figure_on_board(3, i, 1, "P", self.q4 + 1)
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

        # Remove piece from current location
        self.board[current_location] = False

        # Place piece at new location
        self.board[new_location] = piece_to_move

    def copy(self):  # Create a copy of the current board
        c = Board()
        c.board = self.board.copy()
        return c

    def detect_check(self, _board, player):
        """
        Move a piece from current_location to new_location.
        Also update the numbers of column switches allowed for 
        the moved piece if necessary

        :param current_location: tuple of form (row, col)
        :param new_location: tuple of form (row, col)
        """
        # if needed, flip the board
        if player == 1:
            board = list(reversed(_board))  # invert _board
        else:
            board = _board.copy()

        # find location for our king:
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].type == "K":
                    k_loc = (i, j)

        # go through enemy piece types and areas they can be in
        # pawn
        locs = [[-1, -1], [1, -1]]
        for loc in locs:
            try:
                piece = board[k_loc[0] + loc[0]][k_loc[1] + loc[1]]
                if type(piece) == Piece:
                    if piece.type == "P" and piece.player != player:
                        return True
            except IndexError:
                pass
            # except AttributeError:
            #     pass
                # ignore if we get the error that the type of the empty squares has no attribute player

        # knight
        locs = [[-1, -2], [1, -2], [-2, -1], [2, -1]]
        for loc in locs:
            try:
                piece = board[k_loc[0] + loc[0]][k_loc[1] + loc[1]]
                if type(piece) == Piece:
                    if piece.type == "N" and piece.player != player:
                        return True
            except IndexError:
                pass
            # except AttributeError:
            #     pass
                # ignore if we get the error that the type of the empty squares has no attribute player

        # bishop/queen:
        loclines = [[(-i, -i) for i in range(1, 6)], [(i, -i)
                                                      for i in range(1, 6)]]
        for line in loclines:
            for loc in line:
                try:
                    piece = board[k_loc[0] + loc[0]][k_loc[1] + loc[1]]
                    if type(piece) == Piece:
                        if piece.type in ["Q", "B"] and piece.player != player:
                            return True
                        else:
                            break
                except IndexError:
                    pass
                except AttributeError:
                    pass
                    # ignore if we get the error that the type of the empty squares has no attribute player

        # rook/queen
        loclines = [[(0, -i) for i in range(1, 6)], [(i, 0)
                                                     for i in range(1, 6)], [(-i, 0) for i in range(1, 6)]]
        for line in loclines:
            for loc in line:
                try:
                    piece = board[k_loc[0] + loc[0]][k_loc[1] + loc[1]]
                    if type(piece) == Piece:
                        if piece.type in ["Q", "R"] and piece.player != player:
                            return True
                        else:
                            break
                except IndexError:
                    pass
                except AttributeError:
                    pass
                    # ignore if we get the error that the type of the empty squares has no attribute player

        # king
        locs = [[-1, -1], [0, -1], [1, -1], [1, 0], [-1, 0]]
        for loc in locs:
            try:
                piece = board[k_loc[0] + loc[0]][k_loc[1] + loc[1]]
                if type(piece) == Piece:
                    if piece.type == "K" and piece.player != player:
                        return True
            except IndexError:
                pass
            # except AttributeError:
            #     pass
            # ignore if we get the error that the type of the empty squares has no attribute player

        # if we didn't find anything, we return false
        return False

    def __str__(self):

        # The colours may appear different depending on light or dark mode.
        fig_dict = {
            "0P": "♟", "1P": "♙",
            "0R": "♜", "1R": "♖",
            "0N": "♞", "1N": "♘",
            "0B": "♝", "1B": "♗",
            "0Q": "♛", "1Q": "♕",
            "0K": "♚", "1K": "♔"
        }

        # Flip the board in order to get a more natural looking image with white at the bottom.
        self.board = np.flip(self.board, 0)

        ret_str = "            black\n"
        ret_str += " +-------------------------+\n"

        for i in range(len(self.board)):
            ret_str += str(4-i) + "|"
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
        ret_str += "            white"

        # undo the flipping
        self.board = np.flip(self.board, 0)

        return ret_str

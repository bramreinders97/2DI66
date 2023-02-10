import numpy as np
from Classes.Piece import Piece


class Board:
    def __init__(self, size=5):  # Default value set to 5

        # Declaration of the array with object as data type.
        self.board = np.ndarray((size, size), dtype=object)
        self.size = size

        # Initialise all values with "False" as default.
        for i in range(size):
            for j in range(size):
                self.board[i][j] = False



    def place_figure_on_board(self, row, column, player, piece_type):
        # a little function in order to place one individual figure on the board
        self.board[row][column] = Piece(player, piece_type)

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
            self.place_figure_on_board(3, i, "B", "P")
            self.place_figure_on_board(1, i, "W", "P")

        # Initialise Rooks
        self.place_figure_on_board(4, 4, "B", "R")
        self.place_figure_on_board(0, 0, "W", "R")

        # Initialise Knights
        self.place_figure_on_board(4, 3, "B", "N")
        self.place_figure_on_board(0, 1, "W", "N")

        # Initialise Bishops
        self.place_figure_on_board(4, 2, "B", "B")
        self.place_figure_on_board(0, 2, "W", "B")

        # Initialise Queens
        self.place_figure_on_board(4, 1, "B", "Q")
        self.place_figure_on_board(0, 3, "W", "Q")

        # Initialise Kings
        self.place_figure_on_board(4, 0, "B", "K")
        self.place_figure_on_board(0, 4, "W", "K")

        return True

    def make_move(self, current_location, new_location):
        # Not sure if these are the smartest parameters. I was
        # thinking if you provide for example (1,0) and (2,0)
        # it moves the piece on 1,0 -> 2,0
        pass

    def evaluate_board(self):
        # Evaluate whether or not the game is finished, and if so
        # who won
        pass

    def get_possible_moves(self, player):
        # Check whose turn it is, and which moves this player can make
        # using the current state of the board and the piece.possible_next_locations
        # funtion. It should not be possible to make a move to a location containing
        # another piece of the same color. Also, you should not be able to make a move
        # which puts your own king in check
        pass

    def choose_next_move(self, player):
        # Select a next move for a player based on their strategy and the output
        # of self.get_possible_moves
        moves = self.get_possible_moves(self, player)
        self.make_move(np.random.choice(moves))
        return

    def detect_check(self, _board, player):
        """
        Check whether the current player is in check. Return true if they are.

        :param player: the current player
        :return: bool
        """
        # if needed, flip the board
        if player == 1:
            board = list(reversed(_board))#invert _board
        else:
            board = _board.copy()

        # find location for our king:
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j].type == "K":
                    k_loc = (i, j)


        # go through enemy piece types and areas they can be in
        ## pawn
        locs = [[-1,-1], [1,-1]]
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

        ## knight
        locs = [[-1,-2], [1,-2], [-2,-1],[2,-1]]
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

        ## bishop/queen:
        loclines = [[(-i,-i) for i in range(1,6)], [(i,-i) for i in range(1,6)]]
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

        ## rook/queen
        loclines = [[(0,-i) for i in range(1,6)], [(i,0) for i in range(1,6)], [(-i,0) for i in range(1,6)]]
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

        ## king
        locs = [[-1,-1], [0,-1], [1,-1], [1,0], [-1,0]]
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
            "WP": "♟", "BP": "♙",
            "WR": "♜", "BR": "♖",
            "WN": "♞", "BN": "♘",
            "WB": "♝", "BB": "♗",
            "WQ": "♛", "BQ": "♕",
            "WK": "♚", "BK": "♔"
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
                    ret_str += fig_dict[self.board[i]
                                        [j].player + self.board[i][j].type]
                    ret_str += "  "
                else:
                    ret_str += "  ⋅  "
            ret_str += "|\n"

        ret_str += " +-------------------------+\n"
        ret_str += "            white"

        # undo the flipping
        self.board = np.flip(self.board, 0)

        return ret_str

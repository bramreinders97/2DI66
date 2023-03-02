from math import inf
from Classes.Piece import Piece
from Classes.Board import Board
import random


class NextMovesGenerator:
    def __init__(self, board, player):
        self.board = board  # The boards current state

        self.player = player  # the player whose turn it is
        # 0 for white, 1 for black

        # List to keep track of all possible moves
        self.possible_moves = []

    def horizontal_or_vertical_limit(self, one_dimensional_direction,
                                     current_loc):
        """
        Check how far we can move to the left/right or top/bottom.

        :param one_dimensional_direction: int specifying the direction accross
                                     either the horizontal or vertical axis
        :param current_loc: int specifying the current row/column a piece is at
        """
        if one_dimensional_direction > 0:
            return (self.board.size - 1) - current_loc
        elif one_dimensional_direction < 0:
            return current_loc
        else:
            return inf

    def check_possible_moves(self, start_location, direction_obj):
        """
        Check all possible moves for a specific piece in a specific direction

        :param start_location: array of the form [row, col]
        :param direction_obj: Direction object specifying the direction to
                              check moves in
        :param player: 0 if white's turn, 1 if blacks turn
        """
        # Specifies how far along the board we're travelling
        distance = 1

        #[vertical_direction, horizontal_direction]
        direction = direction_obj.direction

        # Check how far we will be able to go across the board.
        # This value is decided by taking the minimum of the inherent limit of
        # a piece, the space a piece has along the horizontal axis and the
        # space a piece has along the vertical axis
        limit = min(direction_obj.limit,
                    self.horizontal_or_vertical_limit(
                        direction[0], start_location[0]),
                    self.horizontal_or_vertical_limit(
                        direction[1], start_location[1]))

        while distance <= limit:
            # location this move would move us to
            move_loc = start_location + distance*direction
            try:
                piece_at_new_loc = self.board.board[move_loc[0], move_loc[1]]
            except IndexError:
                # the horizontal_or_vertical_limit function is written without
                # the movements of knights in mind
                # This try-except saves knights trying to get outside of the
                # board
                break

            # check if there is already a piece at the new location
            if piece_at_new_loc:
                # can't go there is one of our own pieces is already there
                if piece_at_new_loc.player == self.player:
                    break
                # there is an opponents piece at the new location
                else:
                    # if we are not a pawn going straight, we're allowed to
                    # hit the opponent -> check if doing this is safe and
                    # we're not putting ourselvesin check
                    if direction_obj.can_hit:
                        self.check_if_move_allowed(start_location, move_loc)
                        break
                    else:  # If pawn wants to go forward but there is a piece
                        # in the way
                        break

            elif direction_obj.must_hit:  # for the case that a pawn wants to
                # move sideways but there is no opponent there
                break
            else:  # location is free
                self.check_if_move_allowed(start_location, move_loc)
                distance += 1

    def check_if_move_allowed(self, start_loc, move_loc):
        """
        Check if making a move leaves you in check. If it is okay to do the
        move, append the move to self.possible_moves

        :pararm start_loc: [row,col] = the location where the piece is being
                                       removed
        :param move_loc: [row,col] = the location where the piece is being 
                                     moved to
        """
        copy_board = self.board.copy()
        copy_board.make_move(
            (start_loc[0], start_loc[1]), (move_loc[0], move_loc[1]))
        if not self.detect_check(copy_board.board, self.player):
            self.possible_moves.append(
                [(start_loc[0], start_loc[1]), (move_loc[0], move_loc[1])])

    def choose_next_move(self):
        """
        For all pieces belonging to the current player, check the possible 
        moves.As soon as all possible moves are found, chose a random move.

        :returns: The randomly chosen move if available, False if there are 
                  no possible moves
        """
        # for all pieces of current player, check the possible moves
        for i in range(self.board.size):
            for j in range(self.board.size):
                piece_at_loc = self.board.board[i][j]

                if piece_at_loc and piece_at_loc.player == self.player:

                    # check possible moves for this piece in each direction
                    # separately
                    for direction in piece_at_loc.directions():
                        self.check_possible_moves(
                            [i, j], direction)

        if len(self.possible_moves):
            # Return a randomly chosen move
            return random.choice(self.possible_moves)
        else:
            return False

    def detect_check(self, _board, player):
        """
        Check whether the current player is in check. Return true if they are.
        :param player: the current player
        :return: bool
        """
        # if needed, flip the board
        if player == 0:
            board = list(reversed(_board))  # invert _board
        else:
            board = _board.copy()

        # BBoard = Board(self.board.size, self.board.q4)
        # BBoard.board = board
        # print(BBoard)

        # find location for our king:
        for i in range(len(_board)):
            for j in range(len(_board)):
                try:
                    if board[i][j].type == "K" and \
                            board[i][j].player == player:
                        k_loc = (i, j)
                        # print(f'k_loc: {i}, {j}')
                except AttributeError:
                    continue

        # print(k_loc)
        # go through enemy piece types and areas they can be in
        # pawn
        locs = [[-1, 1], [-1, -1]]
        for loc in locs:
            try:
                x = k_loc[0] + loc[0]
                y = k_loc[1] + loc[1]
                if x < 0 or y < 0:
                    continue
                    # skip locations under 0
                piece = board[x][y]
                if type(piece) == Piece:
                    # print(piece.player, player, loc, piece, [
                    #       k_loc[0] + loc[0], k_loc[1] + loc[1]])
                    if piece.type == "P" and piece.player != player:
                        if (loc[1] != 0 and piece.switches_left > 0) or \
                                loc[1] == 0:
                            return True
                        # print("P")
            except IndexError:
                pass
                # ignore if we get the error that the type of the empty
                # squares has no attribute player

        # knight
        locs = [[-1, -2], [-1, 2], [-2, -1], [-2, 1]]
        for loc in locs:
            try:
                x = k_loc[0] + loc[0]
                y = k_loc[1] + loc[1]
                if x < 0 or y < 0:
                    continue
                    # skip locations under 0
                piece = board[x][y]
                if type(piece) == Piece:
                    if piece.type == "N" and piece.player != player:
                        if (loc[1] != 0 and piece.switches_left > 0) or \
                                loc[1] == 0:
                            return True
                        # print("N")

            except IndexError:
                pass
            # except AttributeError:
            #     pass
                # ignore if we get the error that the type of the empty
                # squares has no attribute player

        # bishop/queen:
        loclines = [[(-i, -i) for i in range(1, 6)], [(-i, i)
                                                      for i in range(1, 6)]]
        for line in loclines:
            for loc in line:
                try:
                    x = k_loc[0] + loc[0]
                    y = k_loc[1] + loc[1]
                    if x < 0 or y < 0:
                        continue
                        # skip locations under 0
                    piece = board[x][y]
                    if type(piece) == Piece:
                        if piece.type in ["Q", "B"] and piece.player != player:
                            if (loc[1] != 0 and piece.switches_left > 0) or \
                                    loc[1] == 0:
                                return True
                            # print("QB")

                        else:
                            break
                except IndexError:
                    pass
                except AttributeError:
                    pass
                    # ignore if we get the error that the type of the empty
                    # squares has no attribute player

        # rook/queen
        loclines = [[(0, -i) for i in range(1, 6)], [(-i, 0)
                    for i in range(1, 6)], [(0, i) for i in range(1, 6)]]
        for line in loclines:
            for loc in line:
                try:
                    x = k_loc[0] + loc[0]
                    y = k_loc[1] + loc[1]
                    if x < 0 or y < 0:
                        continue
                        # skip locations under 0
                    piece = board[x][y]
                    if type(piece) == Piece:
                        if piece.type in ["Q", "R"] and piece.player != player:
                            if (loc[1] != 0 and piece.switches_left > 0) or \
                                    loc[1] == 0:
                                return True
                            # print("QR")

                        else:
                            break
                except IndexError:
                    pass
                except AttributeError:
                    pass
                    # ignore if we get the error that the type of the empty
                    # squares has no attribute player

        # king
        locs = [[-1, -1], [0, -1], [-1, 1], [-1, 0], [0, 1]]
        for loc in locs:
            try:
                x = k_loc[0] + loc[0]
                y = k_loc[1] + loc[1]
                if x < 0 or y < 0:
                    continue
                    # skip locations under 0
                piece = board[x][y]
                if type(piece) == Piece:
                    if piece.type == "K" and piece.player != player:
                        # print("K")
                        if (loc[1] != 0 and piece.switches_left > 0) or \
                                loc[1] == 0:
                            return True
            except IndexError:
                pass
            # except AttributeError:
            #     pass
            # ignore if we get the error that the type of the empty squares
            #  has no attribute player

        # if we didn't find anything, we return false
        return False

from math import inf
from Classes.Piece import Piece
from Classes.Board import Board


class NextMovesGenerator:
    def __init__(self, board, player):
        self.board = board  # The boards current state

        self.player = player  # the player whose turn it is
        # 0 for white, 1 for black

        # List to keep track of all possible moves
        self.possible_moves = []

    def horizontal_or_vertical_limit(self, one_dimensional_direction, current_loc):
        """
        Check how far we can move to the left/right or top/bottom.

        :param one_dimensional_direction: int specifying the direction accross 
                                     either the horizontal or vertical axis
        :param current_loc: int specifying the current column a piece is at
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
        :param direction_obj: Direction object specifying the direction to check moves in
        :param player: 0 if white's turn, 1 if blacks turn
        """
        # Specifies how far along the board we're travelling
        distance = 1

        #[vertical_direction, horizontal_direction]
        direction = direction_obj.direction

        # Check how far we will be able to go across the board
        limit = min(direction_obj.limit,
                    self.horizontal_or_vertical_limit(
                        direction[0], start_location[0]),
                    self.horizontal_or_vertical_limit(
                        direction[1], start_location[1]))

        while distance <= limit:
            move_loc = start_location + distance*direction
            try:
                piece_at_new_loc = self.board.board[move_loc[0], move_loc[1]]
            except IndexError:
                # the horizontal_or_vertical_limit function is written without
                # the movements of knights in mind
                # This try-except saves knights trying to get outside of the board
                break

            if piece_at_new_loc:
                if piece_at_new_loc.player == self.player:
                    break
                else:  # there is an opponents piece at move_loc
                    if direction_obj.can_hit:
                        self.check_if_move_allowed(start_location, move_loc)
                        break
                    else:  # If pawn wants to go forward but there is a piece in the way
                        break

            elif direction_obj.must_hit:  # for the case that a pawn wants to move sideways
                # but there is no opponent there
                break
            else:  # location is free
                self.check_if_move_allowed(start_location, move_loc)
                distance += 1

    def check_if_move_allowed(self, start_loc, move_loc):
        copy_board = self.board.copy()
        copy_board.make_move(
            (start_loc[0], start_loc[1]), (move_loc[0], move_loc[1]))
        # if not self.detect_check(copy_board.board, self.player):
        # print('result of detect_check: ', self.detect_check(
        #     copy_board.board, 1))
        self.possible_moves.append(
            [(start_loc[0], start_loc[1]), (move_loc[0], move_loc[1])])

    def choose_next_move(self):
        pass

    def detect_check(self, _board, player):
        """
        Check whether the current player is in check. Return true if they are.
        :param player: the current player
        :return: bool
        """
        # if needed, flip the board
        if player == 1:
            board = list(reversed(_board))  # invert _board
        else:
            board = _board.copy()

        BBoard = Board(5, q4=True)
        BBoard.board = board
        print(BBoard)

        # find location for our king:
        for i in range(len(_board)):
            for j in range(len(_board)):
                try:
                    if board[i][j].type == "K":
                        k_loc = (i, j)
                except AttributeError:
                    continue

        print(k_loc)
        # go through enemy piece types and areas they can be in
        # pawn
        locs = [[-1, -1], [1, -1]]
        for loc in locs:
            try:
                x = k_loc[0] + loc[0]
                y = k_loc[1] + loc[1]
                if x < 0 or y < 0:
                    continue
                    #skip locations under 0
                piece = board[x][y]
                if type(piece) == Piece:
                    print(piece.player, player, loc, piece, [k_loc[0] + loc[0], k_loc[1] + loc[1]])
                    if piece.type == "P" and piece.player != player:
                        print("P")
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
                x = k_loc[0] + loc[0]
                y = k_loc[1] + loc[1]
                if x < 0 or y < 0:
                    continue
                    # skip locations under 0
                piece = board[x][y]
                if type(piece) == Piece:
                    if piece.type == "N" and piece.player != player:
                        print("N")
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
                    x = k_loc[0] + loc[0]
                    y = k_loc[1] + loc[1]
                    if x < 0 or y < 0:
                        continue
                        # skip locations under 0
                    piece = board[x][y]
                    if type(piece) == Piece:
                        if piece.type in ["Q", "B"] and piece.player != player:
                            print("QB")
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
                    x = k_loc[0] + loc[0]
                    y = k_loc[1] + loc[1]
                    if x < 0 or y < 0:
                        continue
                        # skip locations under 0
                    piece = board[x][y]
                    if type(piece) == Piece:
                        if piece.type in ["Q", "R"] and piece.player != player:
                            print("QR")
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
                x = k_loc[0] + loc[0]
                y = k_loc[1] + loc[1]
                if x < 0 or y < 0:
                    continue
                    # skip locations under 0
                piece = board[x][y]
                if type(piece) == Piece:
                    if piece.type == "K" and piece.player != player:
                        print("K")
                        return True
            except IndexError:
                pass
            # except AttributeError:
            #     pass
            # ignore if we get the error that the type of the empty squares has no attribute player

        # if we didn't find anything, we return false
        return False

from math import inf
from Classes.Direction import Direction
from numpy import array


class Piece:
    # This class is to be extended for all possible type of pieces.
    # Each of these extensions will have their own possible_next_locations
    # function

    def __init__(self, player, piece_type, limit):

        # White     =>  0   (type: int)
        # Black     =>  1   (type: int)
        self.player = player

        self.switches_left = 5  # Number of allowed column switches left

        # Naming convention for type:
        # Pawn      =>  P    (type: string)
        # Rook      =>  R    (type: string)
        # Knight    =>  N    (type: string)
        # Bishop    =>  B    (type: string)
        # Queen     =>  Q    (type: string)
        # King      =>  K    (type: string)
        self.type = piece_type

        # 1 if king or knight or pawn & we're not answering q4
        # 2 if pawn & we are answering q4
        # inf otherwise
        self.limit = limit

    def directions(self):
        """
        Function that returns a list of all the possible directions a piece
        can move in.
        """
        # white pieces should go in inverted directions compared to black
        # pieces
        directions_factor = 1 if not self.player else -1

        # Return the possible directions this piece can move in
        if self.type == "P":
            directions = [
                Direction(directions_factor*array([1, 0]),
                          self.limit, can_hit=False)]

            # col switches are only possible if we have switches left
            if self.switches_left > 0:
                directions.extend(
                    [
                        Direction(directions_factor *
                                  array([1, 1]), 1, must_hit=True),
                        Direction(directions_factor *
                                  array([1, -1]), 1, must_hit=True)
                    ]
                )
            return directions

        elif self.type == "R":
            directions = [
                Direction(directions_factor*array([1, 0]), self.limit)]

            # col switches are only possible if we have switches left
            if self.switches_left > 0:
                directions.extend([
                    Direction(directions_factor*array([0, 1]), self.limit),
                    Direction(directions_factor*array([0, -1]), self.limit)
                ])

            return directions

        elif self.type == "N":
            # col switches are only possible if we have switches left
            if self.switches_left > 0:
                return [
                    Direction(directions_factor*array([1, -2]), self.limit),
                    Direction(directions_factor*array([1, 2]), self.limit),
                    Direction(directions_factor*array([2, -1]), self.limit),
                    Direction(directions_factor*array([2, 1]), self.limit)
                ]
            else:
                return []

        elif self.type == "B":
            # col switches are only possible if we have switches left
            if self.switches_left > 0:
                return [
                    Direction(directions_factor*array([1, 1]), self.limit),
                    Direction(directions_factor*array([1, -1]), self.limit)
                ]
            else:
                return []

        elif self.type == "Q":
            directions = [Direction(directions_factor*array([1, 0]),
                                    self.limit),
                          Direction(directions_factor*array([1, 0]),
                                    self.limit)]

            # col switches are only possible if we have switches left
            if self.switches_left > 0:
                directions.extend([
                    Direction(directions_factor*array([0, 1]), self.limit),
                    Direction(directions_factor*array([0, -1]), self.limit),
                    Direction(directions_factor*array([1, 1]), self.limit),
                    Direction(directions_factor*array([1, -1]), self.limit)
                ])

            return directions

        else:  # King
            directions = [
                Direction(directions_factor*array([1, 0]), self.limit)]

            # col switches are only possible if we have switches left
            if self.switches_left > 0:
                directions.extend([
                    Direction(directions_factor*array([0, 1]), self.limit),
                    Direction(directions_factor*array([1, 1]), self.limit),
                    Direction(directions_factor*array([1, -1]), self.limit),
                    Direction(directions_factor*array([0, -1]), self.limit)
                ])

            return directions

    def __str__(self):
        return f"{self.player} - {self.type} - {self.switches_left}"

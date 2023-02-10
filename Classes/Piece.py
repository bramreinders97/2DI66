from math import inf
from Classes.Direction import Direction
from numpy import array


class Piece:
    # This class is to be extended for all possible type of pieces. Each of these extensions
    # will have their own possible_next_locations function

    def __init__(self, player, piece_type, limit):

        # Naming convention for type: (I would choose it like this since it is short and unambiguous)
        # White     =>  W   (type: string)
        # Black     =>  B   (type: string)
        if player == "W":
            self.player = 0
        elif player == "B":
            self.player = 1
        else:
            self.player = player

        self.switches_left = 5  # Number of allowed column switches left
        # I'm not really sure if this should be stored her or in the Game/Board class

        # Naming convention for type:
        # Pawn      =>  P    (type: string)
        # Rook      =>  R    (type: string)
        # Knight    =>  N    (type: string)
        # Bishop    =>  B    (type: string)
        # Queen     =>  Q    (type: string)
        # King      =>  K    (type: string)
        self.type = piece_type  # rook, knight, etc

        # 1 if king or knight or pawn & we're not answering q4
        # 2 if pawn & we are answering q4
        # inf otherwise
        self.limit = limit

    def directions(self):
        # white pieces should go in inverted directions compared to black pieces
        directions_factor = 1 if not self.player else -1

        # Return the possible directions this piece can move in
        if self.type == "P":
            return [
                Direction(directions_factor *
                          array([1, 0]), self.limit, can_hit=False),
                Direction(directions_factor*array([1, 1]), 1, must_hit=True),
                Direction(directions_factor*array([1, -1]), 1, must_hit=True)
            ]
        elif self.type == "R":
            return [
                Direction(directions_factor*array([1, 0]), self.limit),
                Direction(directions_factor*array([0, 1]), self.limit),
                Direction(directions_factor*array([0, -1]), self.limit)
            ]
        elif self.type == "N":
            return [
                Direction(directions_factor*array([1, -2]), self.limit),
                Direction(directions_factor*array([1, 2]), self.limit),
                Direction(directions_factor*array([2, -1]), self.limit),
                Direction(directions_factor*array([2, 1]), self.limit)
            ]
        elif self.type == "B":
            return [
                Direction(directions_factor*array([1, 1]), self.limit),
                Direction(directions_factor*array([1, -1]), self.limit)
            ]
        elif self.type == "Q":
            return [
                Direction(directions_factor*array([1, 0]), self.limit),
                Direction(directions_factor*array([0, 1]), self.limit),
                Direction(directions_factor*array([0, -1]), self.limit),
                Direction(directions_factor*array([1, 1]), self.limit),
                Direction(directions_factor*array([1, -1]), self.limit)
            ]
        else:  # King
            return [
                Direction(directions_factor*array([1, 0]), self.limit),
                Direction(directions_factor*array([0, 1]), self.limit),
                Direction(directions_factor*array([1, 1]), self.limit),
                Direction(directions_factor*array([1, -1]), self.limit),
                Direction(directions_factor*array([0, -1]), self.limit)
            ]

    def __str__(self):
        # return coloured letter of this piece
        return f"{self.player} - {self.type}"

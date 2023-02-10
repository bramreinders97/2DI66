class Piece:
    # This class is to be extended for all possible type of pieces. Each of these extensions
    # will have their own possible_next_locations function

    def __init__(self, player, piece_type):

        # Naming convention for type: (I would choose it like this since it is short and unambiguous)
        # White     =>  0   (type: int)
        # Black     =>  1   (type: int)
        self.player = player  # White or Black, or 1/2 not sure what is more useful

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

    def possible_next_locations(self, row, col):
        # Based on the current location and player, return an array of indices where
        # this piece can go. E.g. if a pawn is now at 1,0 and self.player == black, this
        # function returns [(2,0)]
        pass

    def __str__(self):
        #return coloured letter of this piece
        pass

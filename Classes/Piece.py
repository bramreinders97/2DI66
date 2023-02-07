class Piece:
    # This class is to be extended for all possible type of pieces. Each of these extensions
    # will have their own possible_next_locations function

    def __init__(self, player):
        self.player = player  # White or Black, or 1/2 not sure what is more useful
        self.switches_left = 5  # Number of allowed column switches left
        # I'm not really sure if this should be stored her or in the Game/Board class

    def possible_next_locations(self, row, col):
        # Based on the current location and player, return an array of indices where
        # this piece can go. E.g. if a pawn is now at 1,0 and self.player == black, this
        # function returns [(2,0)]
        pass

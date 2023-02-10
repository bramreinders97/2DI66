class Direction:
    def __init__(self, direction, limit, must_hit=False, can_hit=True):
        """
        Class that stores info about a specific direction a piece can move in.

        :param direction: array of form [row-direction, col-direction]
        :param limit: int specifying how many times the direction can be multiplied. To illustrate,
                      for the direction (1,1), limit = 1 for a pawn but inf for a queen
        :param must_hit: bool. True for a pawn in the (1,1) direction as a pawn can only 
                               move sideways if it hits something
        :param can_hit: bool. False for a pawn in the direction (1,0). Done to prevent a pawn 
                              hitting a piece from the opponent without going sideways
        """
        self.direction = direction
        self.limit = limit
        self.must_hit = must_hit
        self.can_hit = can_hit

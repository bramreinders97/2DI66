class playSingleGame:
    # This class simulates a single game

    def __init__(self, board, strategyPlayer1, strategyPlayer2):
        self.board = board
        self.strategyPlayer1 = strategyPlayer1
        self.strategyPlayer2 = strategyPlayer2
        self.moves_made = 0

    def simulate_game(self):
        # Simulate game and return:
        # - the winner (White/Black/Draw)
        # - Boolean specifying whether black promoted a pawn to a queen
        # - Boolean specifying whether white promoted a pawn to a queen (not completely sure
        #   right now whether we need a separate var for both players)
        # moves until end of game
        pass

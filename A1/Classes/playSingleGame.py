from Classes.Board import Board
from Classes.NextMovesGenerator import NextMovesGenerator


class playSingleGame:
    # This class simulates a single game

    def __init__(self, q4=False):
        self.moves_made = 0
        self.board = Board(q4=q4)

    def simulate_game(self):
        # Simulate game and return:
        # - the winner (White/Black/Draw)
        # - Boolean specifying whether black promoted a pawn to a queen
        # - Boolean specifying whether white promoted a pawn to a queen
        # - moves until end of game

        white_queen = False
        black_queen = False

        while True:
            next_moves_gen = NextMovesGenerator(
                self.board, self.moves_made % 2)

            next_move = next_moves_gen.choose_next_move()

            if next_move:
                pawn_promoted = self.board.make_move(
                    next_move[0], next_move[1])
                if pawn_promoted:

                    if self.moves_made % 2:
                        black_queen = True
                    else:
                        white_queen = True

                self.moves_made += 1

            else:
                # check other player
                if next_moves_gen.detect_check(self.board.board,
                                               (self.moves_made % 2)):
                    winner = not (self.moves_made % 2)
                else:
                    winner = -1

                return winner, white_queen, black_queen, self.moves_made

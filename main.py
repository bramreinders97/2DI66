# Import the Simulator class and answer questions

from Classes.Board import Board
from Classes.NextMovesGenerator import NextMovesGenerator

board = Board(5, q4=True)

board.make_move((4, 3), (2, 0))

print(board)

# Check possible moves
loc_piece = [0, 1]
piece = board.board[loc_piece[0], loc_piece[1]]

# pawn at 1,0
next_moves_gen = NextMovesGenerator(board, piece.player)
directions = piece.directions()

for direction in directions:
    moves = next_moves_gen.check_possible_moves(loc_piece, direction)
    print(direction.direction, next_moves_gen.possible_moves)

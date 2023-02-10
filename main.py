# Import the Simulator class and answer questions

from Classes.Board import Board
from Classes.NextMovesGenerator import NextMovesGenerator

board = Board(5, q4=True)
piece = board.board[0,4]
next_moves_gen = NextMovesGenerator(board, piece.player)
print(next_moves_gen.detect_check(board.board, 0))

# board.make_move((0, 3), (3, 4))
# board.make_move((1, 4), (2, 0))
#
# print(board)
#
# # Check possible moves
# loc_piece = [0, 4]
# piece = board.board[loc_piece[0], loc_piece[1]]
#
# # pawn at 1,0
# next_moves_gen = NextMovesGenerator(board, piece.player)
# directions = piece.directions()
#
# for direction in directions:
#     moves = next_moves_gen.check_possible_moves_others(loc_piece, direction)
#     print(direction.direction, next_moves_gen.possible_moves)

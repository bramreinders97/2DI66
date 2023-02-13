import numpy as np
from Classes.Board import Board
from Classes.NextMovesGenerator import NextMovesGenerator

board = Board(5, q4=True)

print(board)

################ How to use my (Bram) part ################

next_player = 0  # 0 if it is white's turn, 1 if it is blacks turn

# create new NextMovesGenerator object
next_moves_gen = NextMovesGenerator(board, next_player)

# Randomly choose a next move
next_move = next_moves_gen.choose_next_move()
print(next_move)

# check all possible moves
print(next_moves_gen.possible_moves)

################ What I did to get incorrect detect_check_value ################

# This should return False, however it returns True
print(f"result detect check: {next_moves_gen.detect_check(board.board, 1)}")
print(f"result detect check: {next_moves_gen.detect_check(board.board, 0)}")

# now lets put the king in check and se if it works
board.make_move((0,4), (2,2))
print(board)
print(f"result detect check: {next_moves_gen.detect_check(board.board, 0)}")
print(f"result detect check: {next_moves_gen.detect_check(board.board, 1)}")

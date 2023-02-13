import numpy as np
from Classes.Board import Board
from Classes.NextMovesGenerator import NextMovesGenerator
from Classes.playSingleGame import playSingleGame

board = Board(5, q4=True)

print(board)

################ How to use my (Bram) part ################

n_games = 10000

black_won = 0
white_won = 0
stalemate = 0

for i in range(n_games):
    game = playSingleGame()
    winner, white_queen, black_queen, moves_made = game.simulate_game()

    if winner == -1:
        stalemate += 1
    elif winner:
        black_won += 1
    else:
        white_won += 1

print(f'White won: {white_won / n_games}')
print(f'Black won: {black_won / n_games}')
print(f'No winner: {stalemate / n_games}')


# next_player = 0  # 0 if it is white's turn, 1 if it is blacks turn

# # create new NextMovesGenerator object
# next_moves_gen = NextMovesGenerator(board, next_player)

# # Randomly choose a next move
# next_move = next_moves_gen.choose_next_move()
# print(next_move)

# # check all possible moves
# print(next_moves_gen.possible_moves)

# ################ What I did to get incorrect detect_check_value ################

# # This should return False, however it returns True
# print(f"result detect check: {next_moves_gen.detect_check(board.board, 1)}")
# print(f"result detect check: {next_moves_gen.detect_check(board.board, 0)}")

# # now lets put the king in check and se if it works
# board.make_move((0,4), (2,2))
# print(board)
# print(f"result detect check: {next_moves_gen.detect_check(board.board, 0)}")
# print(f"result detect check: {next_moves_gen.detect_check(board.board, 1)}")

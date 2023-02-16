from Classes.Board import Board
from Classes.playSingleGame import playSingleGame

import numpy as np

class Simulator:
    # class that simulates n games

    def __init__(self):
        pass

    def simulate_n_games(self, n):
        # Simulate n games and store results
        pass

    def question_1(self, n):
        # do calculations that answer Q1
        # maybe also make visualisation?
        pass

    def question_2(self, n):
        # do calculations that answer Q2
        # maybe also make visualisation?
        pass

    def question_3(self, pawn_advancing=False):

        """
        The Code to answer question 3.

        :param pawn_advancing: bool Controls whether white can advance two
                                    squares along the same column on its first move.
        """

        # In order to get a confidence interval, we need to simulate some games.
        print("Question 3: average number of games.")

        n_moves_list = []
        n_games = 2000

        for i in range(n_games):
            game = playSingleGame()

            # Turn on pawn advancing for white if wanted.
            if pawn_advancing:
                game.board.q4 = True

            tmp = game.simulate_game()
            n_moves_list.append(tmp[3])
            if i % 100 == 0:
                print("\r Game: " + str(i) + "/" + str(n_games), end="")

        print()
        print()

        half_width = 1.96 * np.sqrt(np.var(n_moves_list) / n_games)
        print("The average number of steps for " + str(n_games) + " played games is "
              + str(np.round(np.average(n_moves_list), 1)) + " games")
        print("Half width for " + str(n_games) + " games: " + str(np.round(half_width, 6)))

        # Since the want a half width of 0.01 we need to simulate more games.
        # To compute how much more we will compute n using the variance obtained above.
        # To compute the number of games needed we just transform the formular
        # used for calculating the confidence interval.
        # Since the resulting number is quite large, we will not simulate this many games.

        n_games_needed = 1 / (((0.01 / 1.96) ** 2) / np.var(n_moves_list))
        print("In order to achieve a half-width of 0.01 approximately " + str(
            np.round(n_games_needed, 1)) + " games are needed")

        print()
        print("--------------------------")
        print("Question 3: average number of games if white wins.")

        # To get the average number of games with given that white wins can be achieved by only some small adaptions.
        # The trick is to simply only append to the array if white won the game.

        n_games = 2000  # Actually it is the number of games where white won.
        n_moves_list = []

        i = 0
        while i < n_games:
            game = playSingleGame()

            # Turn on pawn advancing for white if wanted.
            if pawn_advancing:
                game.board.q4 = True

            tmp = game.simulate_game()
            if not tmp[0]:
                n_moves_list.append(tmp[3])
                i += 1
                if i % 100 == 0:
                    print("\r Game: " + str(i) + "/" + str(n_games), end="")

        print()
        print()

        half_width = 1.96 * np.sqrt(np.var(n_moves_list) / n_games)
        print("The average number of steps for " + str(n_games) + " played games is " + str(
            np.round(np.average(n_moves_list), 1)) + " games")
        print("Half width for " + str(n_games) + " games: " + str(np.round(half_width, 6)))

        # Again, we are using the same approach as above to calculate  the number of needed games
        # to achieve a half-width of 0.01.

        n_games_needed = 1 / (((0.01 / 1.96) ** 2) / np.var(n_moves_list))
        print("In order to achieve a halfWidth of 0.01 approximately " + str(
            np.round(n_games_needed, 1)) + " games are needed")

        pass

    def question_4(self, n):
        # do calculations that answer Q4
        # maybe also make visualisation?
        pass

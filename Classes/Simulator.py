from Classes.Board import Board
from Classes.playSingleGame import playSingleGame
from itertools import combinations
import numpy as np
import multiprocessing
from joblib import Parallel, delayed


class Simulator:
    # class that simulates n games

    def __init__(self, q4=False):
        self.q4 = q4

    def calc_probability_and_ci(self, sim_results, winner):
        """
        Calculate and return the probability and confidence interval
        of a certain winner

        :param sim_results: np.array Array with the winners of the 
                                     games
        :param winner: bool/int The winner to check statistics for
        """
        n = len(sim_results)
        games_won = (sim_results == winner)
        prob = np.mean(games_won)
        sigma = np.std(games_won)
        half_width = 1.96 * sigma/np.sqrt(n)

        ci = (prob - half_width, prob + half_width)

        return prob, ci

    def check_overlap_in_cis(self, cis_to_check):
        """
        Checks if two CI's overlap. Returns True is this is 
        the case and False if not

        :param cis_to_check: list List of CIs the form [(low,high),(low,high),..]
        """
        for cis_to_check in combinations(cis_to_check, 2):
            ci1 = cis_to_check[0]
            ci2 = cis_to_check[1]

            # If there is an overlap return True
            if ci1[1] >= ci2[0] and ci2[1] >= ci1[0]:
                return True

        # If we surivive the loop -> no overlap
        return False

    def get_winner_single_game(self):
        """
        Simulate a single game and return the winner
        """
        game = playSingleGame(q4=self.q4)
        winner = game.simulate_game()[0]
        return winner

    def sim_games_in_parallel(self, n_games):
        """
        Function that simulates n games in parallel. This
        significantly speeds up the simualtion process

        :param n_games: int number of games to simulate
        """
        num_cores = multiprocessing.cpu_count()

        sim_results = Parallel(n_jobs=num_cores)(delayed(self.get_winner_single_game)()
                                                 for _ in range(n_games))

        return np.array(sim_results)

    def question_1_4(self, nRuns):
        """
        The Code to answer questions 1 and 4.

        :param nRuns: int number of games to simulate
        """
        print()
        print(f"Doing {nRuns} runs to answer Q{4 if self.q4 else 1}!")
        print()

        # Get results from games
        sim_results = self.sim_games_in_parallel(nRuns)

        # Calculate statistics of interest
        prob_white, ci_white = self.calc_probability_and_ci(sim_results, False)
        prob_black, ci_black = self.calc_probability_and_ci(sim_results, True)
        prob_draw, ci_draw = self.calc_probability_and_ci(sim_results, -1)

        print(f"Prob White wins: {prob_white}, {ci_white}")
        print(f"Prob Black wins: {prob_black}, {ci_black}")
        print(f"Prob Draw wins: {prob_draw}, {ci_draw}")

        print()

        # Check for significance
        if self.check_overlap_in_cis([ci_white, ci_black, ci_draw]):
            print("Results not significant, there is an overlap in the CI's")
        else:
            print('Results are significant!')

        print()

    def get_promotion_single_game(self):
        """
        Play a single game and return wheter anyone got a promotion
        :return: bool
        """
        game = playSingleGame()
        output = game.simulate_game()
        promotion = output[1] or output[2]
        return promotion


    def question_2(self, nRuns):
        """
        Code to answer question 2
        :param n: number of runs to be ran for the test
        :return:
        """
        print()
        print(f"Doing {nRuns} runs to answer Q2!")
        print()

        # Initialize results array
        sim_results = np.zeros(nRuns)

        # Get results from games
        sim_results = self.sim_games_in_parallel(nRuns)

        #get the promotion from each game
        num_cores = multiprocessing.cpu_count()

        sim_results = Parallel(n_jobs=num_cores)(delayed(self.get_promotion_single_game())()
                                                 for _ in range(nRuns))

        promotions = np.array(sim_results)
        prob_promo, ci_promo = self.calc_probability_and_ci(promotions, True)

        print(f"Probability of promotion: {prob_promo}, CI: {ci_promo}")

    def question_3(self):
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

            tmp = game.simulate_game()
            n_moves_list.append(tmp[3])
            if i % 100 == 0:
                print("\r Game: " + str(i) + "/" + str(n_games), end="")

        print()
        print()

        half_width = 1.96 * np.sqrt(np.var(n_moves_list) / n_games)
        print("The average number of steps for " + str(n_games) + " played games is "
              + str(np.round(np.average(n_moves_list), 1)) + " games")
        print("Half width for " + str(n_games) +
              " games: " + str(np.round(half_width, 6)))

        # Since the want a half width of 0.01 we need to simulate more games.
        # To compute how much more we will compute n using the variance obtained above.
        # To compute the number of games needed we just transform the formular
        # used for calculating the confidence interval.
        # Since the resulting number is quite large, we will not simulate this many games.

        n_games_needed = np.var(n_moves_list) / ((0.01 / 1.96) ** 2)
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
        print("Half width for " + str(n_games) +
              " games: " + str(np.round(half_width, 6)))

        # Again, we are using the same approach as above to calculate  the number of needed games
        # to achieve a half-width of 0.01.

        n_games_needed = np.var(n_moves_list) / ((0.01 / 1.96) ** 2)
        print("In order to achieve a halfWidth of 0.01 approximately " + str(
            np.round(n_games_needed, 1)) + " games are needed")

        pass

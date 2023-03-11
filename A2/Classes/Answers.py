from A2.Classes.Simulation import Simulation

import numpy as np
import math
from time import time


class Answers:

    """
    A small class in order to structure the code needed to answer the questions of the assignment.
    """

    def Q1(self):

        def sd(my_list, mean):
            return math.sqrt(sum([(i - mean) ** 2 for i in my_list]) / len(my_list))

        start = time()
        for lam in range(1, 5):
            EW_list = []
            ES_list = []
            EN_list = []
            ESg_list = []
            group_count_list = []
            EW_sd_list = []
            ES_sd_list = []
            EN_sd_list = []
            ESg_sd_list = []

            for i in range(100):
                # create and run simulation
                simulator = Simulation(queue_speeds=[1, 1, 1], lam=lam / 60)
                results = simulator.simulate()
                # add desired values to all summary lists
                # E[W] waiting time (over all cashiers): getMeanQueueTime()
                EW_list.append(results.getMeanQueueTime())
                EW_sd_list.append(results.getStDevQueueTime())
                # E[S]: getMeanSojournTime()
                ES_list.append(results.getMeanSojournTime())
                ES_sd_list.append(results.getStDevSojournTime())
                # E[n people inside]: getExpectedNPeopleInCanteen()
                EN_list.append(results.getExpectedNPeopleInCanteen())
                EN_sd_list.append(results.getStDevNPeopleInCanteen())
                # E[S_g]: getMeanSojournGroup()
                ESg_list.append(results.getMeanSojournGroup())
                ESg_sd_list.append(results.getStDevSojournGroup())
                # nr of groups in total
                group_count_list.append(results.group_count)

            # calculate standard deviations and means of the lists
            EW_mean = sum(EW_list) / len(EW_list)
            ES_mean = sum(ES_list) / len(ES_list)
            EN_mean = sum(EN_list) / len(EN_list)
            ESg_mean = sum(ESg_list) / len(ESg_list)
            groups_mean = sum(group_count_list) / len(group_count_list)
            # mean of individual run standard deviations
            EW_sd_mean = sum(EW_sd_list) / len(EW_sd_list)
            ES_sd_mean = sum(ES_sd_list) / len(ES_sd_list)
            EN_sd_mean = sum(EN_sd_list) / len(EN_sd_list)
            ESg_sd_mean = sum(ESg_sd_list) / len(ESg_sd_list)

            EW_sd = sd(EW_list, EW_mean)
            ES_sd = sd(ES_list, ES_mean)
            EN_sd = sd(EN_list, EN_mean)
            ESg_sd = sd(ESg_list, ESg_mean)
            groups_sd = sd(group_count_list, groups_mean)

            print(f"""

            lambda = {lam}
            Average nr of groups per simulation: {groups_mean:.2f} (sd: {groups_sd:.2f})
            E [Waiting]: {EW_mean:.2f}, sd[E[Waiting]] {EW_sd:.2f}, E[sd[Waiting]] {EW_sd_mean:.2f}
            E Sojourn: {ES_mean:.2f}, sd[E] {ES_sd:.2f}, E[sd[Sojourn] {ES_sd_mean:.2f}
            E Nr of people: {EN_mean:.2f}, sd[E] {EN_sd:.2f}, E[sd[nr]] {EN_sd_mean:.2f}
            E Sojourn groups: {ESg_mean:.2f}, sd[E] {ESg_sd:.2f}, E[sd[S group]] {ESg_sd_mean:.2f}
            runtime: {time() - start:.2f}


                    """)

    def Extension_1(self, n_simulations=2000):

        """
        The code to answer the question for the model extension 1.

        :param n_simulations:   int.  The number of simulations performed.
        """

        def sim_1(n, lam=1):

            Mean_Queue_time_Fast = []
            SD_Queue_time_Fast = []

            Mean_Queue_time_Slow = []
            SD_Queue_time_Slow = []

            for i in range(n):
                simulation = Simulation([1, 1.25, 1], 0.15, True, lam / 60)
                sim = simulation.simulate()

                Mean_Queue_time_Fast.append(sim.getMeanQueueTime())
                SD_Queue_time_Fast.append(sim.getStDevQueueTime())

                Mean_Queue_time_Slow.append(sim.getMeanQueueTimeSlow())
                SD_Queue_time_Slow.append(sim.getStDevQueueTimeSlow())

                if i % 1000 == 0:
                    print("\r Simulation: " + str(i) + "/" + str(n), end="")

            print()
            print("lambda: " + str(lam))
            mean_fast = np.mean(Mean_Queue_time_Fast)
            sd_fast = np.mean(SD_Queue_time_Fast)
            hw_fast = 1.96 * np.sqrt((sd_fast ** 2) / n)
            print("Fast: mean: " + str(np.round(mean_fast, 3)) + " sd: " + str(np.round(sd_fast, 3)) + " hw:  " + str(
                np.round(hw_fast, 3)))

            mean_slow = np.mean(Mean_Queue_time_Slow)
            sd_slow = np.mean(SD_Queue_time_Slow)
            hw_slow = 1.96 * np.sqrt((sd_slow ** 2) / n)
            print("Slow: mean: " + str(np.round(mean_slow, 3)) + " sd: " + str(np.round(sd_slow, 3)) + " hw:  " + str(
                np.round(hw_slow, 3)))

            print("Difference in percent: " + str(np.round(mean_slow / mean_fast, 3)))
            print()

        sim_1(n_simulations, 1)
        sim_1(n_simulations, 2)
        sim_1(n_simulations, 3)
        sim_1(n_simulations, 4)
        sim_1(n_simulations, 10)

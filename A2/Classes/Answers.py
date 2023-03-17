from A2.Classes.Simulation import Simulation

import numpy as np
import math
from time import time


class Answers:

    """
    A small class in order to structure the code needed to answer the questions of the assignment.
    """

    def Q1(self, n_simulations):

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

            for i in range(n_simulations):
                # create and run simulation
                simulator = Simulation(queue_speeds=[1, 1, 1], lam=lam /60)
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

            lambda = {lam}, nr of runs {n_simulations}
            Average nr of groups per simulation: {groups_mean:.2f} (sd: {groups_sd:.2f})
            E [Waiting]: {EW_mean:.2f}, sd[E[Waiting]] {EW_sd:.2f}, E[sd[Waiting]] {EW_sd_mean:.2f}
            E Sojourn: {ES_mean:.2f}, sd[E] {ES_sd:.2f}, E[sd[Sojourn] {ES_sd_mean:.2f}
            E Nr of people: {EN_mean:.2f}, sd[E] {EN_sd:.2f}, E[sd[nr]] {EN_sd_mean:.2f}
            E Sojourn groups: {ESg_mean:.2f}, sd[E] {ESg_sd:.2f}, E[sd[S group]] {ESg_sd_mean:.2f}
            runtime: {time() - start:.2f}


                    """)

    def extension_1(self, n_simulations=2000):

        """
        The code to answer the question for the model extension 1.

        :param n_simulations:   int.  The number of simulations performed.
        """

        def sim_1(n, lam=1):

            mean_queue_time_fast = []
            sd_queue_time_fast = []

            mean_queue_time_slow = []
            sd_queue_time_slow = []

            for i in range(n):
                simulation = Simulation([1, 1.25, 1], 0, True, lam / 60)
                sim = simulation.simulate()

                mean_queue_time_fast.append(sim.getMeanQueueTime())
                sd_queue_time_fast.append(sim.getStDevQueueTime())

                mean_queue_time_slow.append(sim.getMeanQueueTimeSlow())
                sd_queue_time_slow.append(sim.getStDevQueueTimeSlow())

                # A small counter to know how far the simulation already is.
                if i % 1000 == 0:
                    print("\r Simulation: " + str(i) + "/" + str(n), end="")

            print()
            print("lambda: " + str(lam))
            mean_fast = np.mean(mean_queue_time_fast)
            sd_fast = np.mean(sd_queue_time_fast)
            hw_fast = 1.96 * np.sqrt((sd_fast ** 2) / n)
            print("Fast: mean: " + str(np.round(mean_fast, 3)) + " sd: " + str(np.round(sd_fast, 3)) + " hw:  " + str(
                np.round(hw_fast, 3)))

            mean_slow = np.mean(mean_queue_time_slow)
            sd_slow = np.mean(sd_queue_time_slow)
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

    def extension_2(self, n_simulations=2000):

        """
        The code to answer the question for the model extension 2.

        :param n_simulations:   int.  The number of simulations performed.
        """

        def sim_2(n, lam=1):

            mean_queue_time_0 = []
            sd_queue_time_0 = []
            mean_queue_time_15 = []
            sd_queue_time_15 = []

            mean_sojourn_time_0 = []
            sd_sojourn_time_0 = []
            mean_sojourn_time_15 = []
            sd_sojourn_time_15 = []

            for i in range(n):

                # Simulate without chance that a group chooses the mobile food stand
                simulation = Simulation([1, 1, 1], 0, True, lam / 60)
                sim = simulation.simulate()
                mean_queue_time_0.append(sim.getMeanQueueTime())
                sd_queue_time_0.append(sim.getStDevQueueTime())
                mean_sojourn_time_0.append(sim.getMeanSojournTime())
                sd_sojourn_time_0.append(sim.getStDevSojournTime())

                # Simulate with a 15% chance that a group chooses the mobile food stand
                simulation = Simulation([1, 1, 1], 0.15, True, lam / 60)
                sim = simulation.simulate()
                mean_queue_time_15.append(sim.getMeanQueueTime())
                sd_queue_time_15.append(sim.getStDevQueueTime())
                mean_sojourn_time_15.append(sim.getMeanSojournTime())
                sd_sojourn_time_15.append(sim.getStDevSojournTime())

                # A small counter to know how far the simulation already is.
                if i % 1000 == 0:
                    print("\r Simulation: " + str(i) + "/" + str(n), end="")

            print()
            print("--------------------------------------")
            print("lambda: " + str(lam))
            print("waiting time")
            mean_0 = np.mean(mean_queue_time_0)
            sd_0 = np.mean(sd_queue_time_0)
            hw_0 = 1.96 * np.sqrt((sd_0 ** 2) / n)
            print("0: mean: " + str(np.round(mean_0, 3)) + " sd: " + str(np.round(sd_0, 3)) + " hw:  " + str(
                np.round(hw_0, 3)))

            mean_15 = np.mean(mean_queue_time_15)
            sd_15 = np.mean(sd_queue_time_15)
            hw_15 = 1.96 * np.sqrt((sd_15 ** 2) / n)
            print("0.15: mean: " + str(np.round(mean_15, 3)) + " sd: " + str(np.round(sd_15, 3)) + " hw:  " + str(
                np.round(hw_15, 3)))

            print("Difference in percent: " + str(np.round(mean_15 / mean_0, 3)))
            print()

            print("sojourn time")
            mean_0 = np.mean(mean_sojourn_time_0)
            sd_0 = np.mean(sd_sojourn_time_0)
            hw_0 = 1.96 * np.sqrt((sd_0 ** 2) / n)
            print("0: mean: " + str(np.round(mean_0, 3)) + " sd: " + str(np.round(sd_0, 3)) + " hw:  " + str(
                np.round(hw_0, 3)))

            mean_15 = np.mean(mean_sojourn_time_15)
            sd_15 = np.mean(sd_sojourn_time_15)
            hw_15 = 1.96 * np.sqrt((sd_15 ** 2) / n)
            print("0.15: mean: " + str(np.round(mean_15, 3)) + " sd: " + str(np.round(sd_15, 3)) + " hw:  " + str(
                np.round(hw_15, 3)))

            print("Difference in percent: " + str(np.round(mean_15 / mean_0, 3)))
            print("--------------------------------------")

        sim_2(n_simulations, 1)
        sim_2(n_simulations, 2)
        sim_2(n_simulations, 3)
        sim_2(n_simulations, 4)
    def extension_3(self, n_simulations):
        """
        Gets the mean sojourn and waiting time using card only mode
        :return:
        """
        start = time()
        for lam in range(1, 5):
            mean_waiting_list = []
            mean_sojourn_list = []
            for i in range(n_simulations):
                simulator = Simulation(queue_speeds=[1, 1, 1], lam=lam / 60, card_only=True)
                results = simulator.simulate()

                mean_waiting_list.append(results.getMeanQueueTime())
                mean_sojourn_list.append(results.getMeanSojournTime())
            print(f"""
                    lambda: {lam}, nr of runs: {n_simulations}
                    Mean waiting time: {sum(mean_waiting_list)/len(mean_waiting_list):.2f}
                    Mean sojourn time: {sum(mean_sojourn_list)/len(mean_sojourn_list):.2f}
                    runtime: {time() - start:.2f}
                    """)


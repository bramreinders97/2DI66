from A3.Classes.Simulation import Simulation

import numpy as np


class Answer:

    """
    Class to answer the questions of the assignments.
    """

    def question_1(self):
        pass

    def question_2(self):
        pass

    def question_3(self, n_runs=10000, sim_time=8*60, elevators=[1, 2, 3, 4, 5], n_floors=5):

        """
        Method to answer question 3.

        :param n_runs:      The number of simulations
        :param sim_time:    The time each simulation runs.
        :param elevators:   List of values for the total number of elevators the system has.
        :param n_floors:    The number of floors of the system. (always 5 in our case)
        """

        prob_not_to_enter = np.zeros((len(elevators), n_floors, n_runs))

        # Iterate over the number of runs.
        for i in range(n_runs):

            # Display how far the simulation is.
            if i % 100 == 0:
                print("\r Game: " + str(i) + "/" + str(n_runs), end="")
            print()

            # Iterate over different numbers of elevators
            for j in range(len(elevators)):
                # Execute simulation and make calculations.
                simulation = Simulation(sim_time, elevators[j])
                results = simulation.simulate()
                results.make_calculations()

                for m in range(n_floors):
                    prob_not_to_enter[j][m][i] = results.prob_not_to_enter[m]

        # Calculate the mean, standard deviation and half width.
        mean_per_elevator_and_floor = np.zeros((len(elevators), n_floors))
        sd_per_elevator_and_floor = np.zeros((len(elevators), n_floors))
        hw_per_elevator_and_floor = np.zeros((len(elevators), n_floors))
        for i in range(len(elevators)):
            for j in range(n_floors):
                mean_per_elevator_and_floor[i][j] = np.mean(prob_not_to_enter[i][j])
                sd_per_elevator_and_floor[i][j] = np.std(prob_not_to_enter[i][j])
                hw_per_elevator_and_floor[i][j] = 1.96 * np.sqrt(sd_per_elevator_and_floor[i][j] ** 2 / n_runs)

        # print the results
        print("probabilities matrix")
        print(mean_per_elevator_and_floor)
        print()
        print("half widths matrix")
        print(hw_per_elevator_and_floor)

    def question_4(self):
        pass

    def question_5(self):
        pass

    def question_6(self, n_runs=10000, sim_time=8*60, elevators=[1, 2, 3, 4, 5]):

        """
        Method to answer question 6.

        :param n_runs:      The number of simulations
        :param sim_time:    The time each simulation runs.
        :param elevators:   List of values for the total number of elevators the system has.
        """

        # mean and sd of waiting times over all runs
        mean_waiting_times = np.zeros((len(elevators), n_runs))
        sd_waiting_times = np.zeros((len(elevators), n_runs))
        # mean and sd of waiting times over all runs including people who left the system due to impatience.
        mean_waiting_times_2 = np.zeros((len(elevators), n_runs))
        sd_waiting_times_2 = np.zeros((len(elevators), n_runs))

        # Iterate over the number of runs.
        for i in range(n_runs):

            # Display how far the simulation is.
            if i % 100 == 0:
                print("\r Game: " + str(i) + "/" + str(n_runs), end="")

            # Iterate over different numbers of elevators
            for j in range(len(elevators)):

                # Execute simulation and make calculations.
                simulation = Simulation(sim_time, elevators[j])
                results = simulation.simulate(True)
                results.make_calculations()

                # sum up the results.
                mean_waiting_times[j][i] = results.overall_mean_waiting_time
                mean_waiting_times_2[j][i] = results.overall_mean_waiting_time_2
                sd_waiting_times[j][i] = results.overall_sd_waiting_time
                sd_waiting_times_2[j][i] = results.overall_sd_waiting_time_2

        # Calculate mean waiting times.
        mean_waiting_time = np.mean(mean_waiting_times, 1)
        mean_waiting_time_2 = np.mean(mean_waiting_times_2, 1)

        # Calculate mean standard deviations.
        sd_waiting_time = np.mean(sd_waiting_times, 1)
        sd_waiting_time_2 = np.mean(sd_waiting_times_2, 1)

        # Calculate half widths.
        half_width = 1.96 * np.sqrt(sd_waiting_time**2 / n_runs)
        half_width_2 = 1.96 * np.sqrt(sd_waiting_time_2**2 / n_runs)

        # print the results.
        print("results for question 6")
        print("elevators: " + str(elevators))
        print("#################################")
        print("mean waiting time: " + str(mean_waiting_time))
        print("standard deviation: " + str(sd_waiting_time))
        print("half width: " + str(half_width))
        print("---------------------------------")
        print("mean waiting time 2: " + str(mean_waiting_time_2))
        print("standard deviation: " + str(sd_waiting_time_2))
        print("half width: " + str(half_width_2))
        print("#################################")







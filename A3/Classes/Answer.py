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

    def question_3(self, n_runs=10000, sim_time=8*60, elevators=[1, 2, 3, 4, 5]):

        # Iterate over the number of runs.
        for i in range(n_runs):

            # Display how far the simulation is.
            if i % 100 == 0:
                print("\r Game: " + str(i) + "/" + str(n_runs), end="")

            # Iterate over different numbers of elevators
            for j in range(len(elevators)):
                # Execute simulation and make calculations.
                simulation = Simulation(sim_time, elevators[j])
                results = simulation.simulate()
                results.make_calculations()

    def question_4(self):
        pass

    def question_5(self):
        pass

    def question_6(self, n_runs=10000, sim_time=8*60, elevators=[1, 2, 3, 4, 5]):

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







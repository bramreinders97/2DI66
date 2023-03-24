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

    def question_3(self):
        pass

    def question_4(self):
        pass

    def question_5(self):
        pass

    def question_6(self, n_runs=10, sim_time=8*60, elevators=[1, 2, 3, 4, 5]):

        # Total mean waiting times over all runs
        mean_waiting_times = np.zeros((len(elevators), n_runs))
        # total mean waiting times over all runs including people who left the system due to impatience.
        mean_waiting_times_2 = np.zeros((len(elevators), n_runs))

        # Iterate over the number of runs.
        for i in range(n_runs):
            # Iterate over different numbers of elevators
            for j in range(len(elevators)):

                # Execute simulation and make calculations.
                simulation = Simulation(sim_time, elevators[j])
                results = simulation.simulate(True)
                results.make_calculations()

                # sum up the results.
                mean_waiting_times[j][i] = results.overall_mean_waiting_time
                mean_waiting_times_2[j][i] = results.overall_mean_waiting_time_2

        # Calculate mean waiting times.
        mean_waiting_time = np.mean(mean_waiting_times, 1)
        mean_waiting_time_2 = np.mean(mean_waiting_times_2, 1)

        # Calculate mean standard diviatins.






from A3.Classes.Simulation import Simulation
from math import inf
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
from joblib import Parallel, delayed


class Answer:

    """
    Class to answer the questions of the assignments.
    """

    def warm_up_cut_off(self, n_elevators, T=8*60*60, n_runs=10000, modulo_for_printing=100):
        """
        Method to plot mean waiting for people. This is necessary to find the cut-off point
        for the warm-up period. 

        :param n_elevators: int. The number of elevators in the system.
        :param T:           int. The time the simulation runs, in seconds.
        :param n_runs:      int. The number of simulations to run.
        :param modulo_for_printing: int. The number of simulations to run before printing the progress.
        """

        # Create a helper function to run a single simulation
        # do it in here so it knows many of the local variables present in this function
        def get_wait_times_single_sim(T, n_elevators, ith_run):
            """
            Helper function, which runs a single simulation and returns the results.
            In the form of a dictionary containing the list of waiting times for each person,
            and the number of people.

            :param T:           int. The time the simulation runs, in seconds.
            :param n_elevators: int. The number of elevators in the system.
            :param ith_run:     int. The number specifying which simulation run this is.
            """
            if ith_run % modulo_for_printing == 0:
                print("\r Simulation: " + str(ith_run) +
                      "/" + str(n_runs), end="")
                print()

            # Simualte a game and calculate the results
            simulation = Simulation(T=T, nr_elevators=n_elevators)
            results = simulation.simulate()
            results.make_calculations()

            # Return the results
            return {
                'all_wait_times': results.one_dim_list_of_waiting_times,
                'n_people': len(results.one_dim_list_of_waiting_times)
            }

        # Check nr of cores for parallelization
        num_cores = multiprocessing.cpu_count()

        # Simulate n_runs in parallel
        sim_results = Parallel(n_jobs=num_cores)(delayed(get_wait_times_single_sim)(T, n_elevators, i)
                                                 for i in range(n_runs))

        # Get the value of the minimum number of people over all runs
        # This is the number of people that we can compare the waiting times for
        # using all the runs
        min_nr_people = min([sim_result['n_people']
                            for sim_result in sim_results])

        # Get all wait times for each simulation for the first `min_nr_people`
        all_wait_times = [sim_result['all_wait_times'][0:min_nr_people]
                          for sim_result in sim_results]

        # Get cumulative waiting times
        cumulative_wait_times = np.sum(all_wait_times, axis=0)

        # calculate mean waiting times
        mean_waiting_times = cumulative_wait_times / n_runs

        # Create plot of results
        x_axis = np.arange(1, min_nr_people+1)

        plt.plot(x_axis, mean_waiting_times)
        plt.title(
            'Mean waiting time for $i^{th}$ customer, '+str(n_runs)+' runs, '+str(n_elevators)+' elevator(s)')

        # Add horizontal line at mean waiting time
        plt.axhline(y=np.mean(mean_waiting_times), color='red')

        # Add dashed vertical line at x-location corresponding to y >= mean waiting time for the first time
        x_pos_1 = np.argmax(mean_waiting_times >= np.mean(mean_waiting_times))

        # Add dashed vertical line that stops at the horizontal line
        mean_waiting_times_after_x_pos_1 = mean_waiting_times[x_pos_1:]
        x_pos_2 = x_pos_1 + \
            np.argmax(mean_waiting_times_after_x_pos_1 <=
                      np.mean(mean_waiting_times))
        y_pos_2 = mean_waiting_times[x_pos_1 + np.argmax(
            mean_waiting_times_after_x_pos_1 <= np.mean(mean_waiting_times))]
        plt.plot([x_pos_1, x_pos_1], [0, y_pos_2],
                 linestyle='--', color='green')
        plt.plot([x_pos_1, x_pos_2], [y_pos_2, y_pos_2],
                 linestyle='--', color='green')

        plt.xlabel(
            '$i^{th}$ customer. Reach E(W) at customer #' + str(x_pos_1))
        plt.ylabel('Mean waiting time')

        plt.show()

    def steady_state_reached(self, runs=15, elevators=[1, 3, 5, 7]):
        m = [[] for i in range(len(elevators))]
        x_axis = []

        for i in range(1, runs + 1):
            print("\r Game: " + str(i) + "/" + str(runs), end="")
            time = i * 1000
            x_axis.append(time)

            for j in range(len(elevators)):
                simulation = Simulation(time, elevators[j])
                results = simulation.simulate(False, 0)
                results.make_calculations()
                m[j].append(results.overall_mean_waiting_time)

        for j in range(len(elevators)):
            plt.plot(
                x_axis, m[j], label="number of elevators: " + str(elevators[j]))
        plt.xlabel("simulation duration in seconds")
        plt.ylabel("mean waiting time")
        plt.legend()
        plt.show()
        plt.close()

    def question_1(self):
        pass

    def question_2(self):
        pass

    def question_3(self, n_runs=10000, sim_time=8*60*60, elevators=[1, 2, 3, 4, 5], n_floors=5):
        """
        Method to answer question 3.

        :param n_runs:      The number of simulations
        :param sim_time:    The time each simulation runs, seconds.
        :param elevators:   List of values for the total number of elevators the system has.
        :param n_floors:    The number of floors of the system. (always 5 in our case)
        """

        prob_not_to_enter = np.zeros((len(elevators), n_floors, n_runs))

        # Iterate over the number of runs.
        for i in range(n_runs):

            # Display how far the simulation is.
            print("\r Game: " + str(i) + "/" + str(n_runs), end="")

            # Iterate over different numbers of elevators
            for j in range(len(elevators)):
                # Execute simulation and make calculations.
                simulation = Simulation(sim_time, elevators[j])
                results = simulation.simulate()
                results.make_calculations()

                for m in range(n_floors):
                    prob_not_to_enter[j][m][i] = results.prob_not_to_enter[m]

        # print("Hello")

        # Calculate the mean, standard deviation and half width.
        mean_per_elevator_and_floor = np.zeros((len(elevators), n_floors))
        sd_per_elevator_and_floor = np.zeros((len(elevators), n_floors))
        hw_per_elevator_and_floor = np.zeros((len(elevators), n_floors))
        for i in range(len(elevators)):
            for j in range(n_floors):
                mean_per_elevator_and_floor[i][j] = np.mean(
                    prob_not_to_enter[i][j])
                sd_per_elevator_and_floor[i][j] = np.std(
                    prob_not_to_enter[i][j])
                hw_per_elevator_and_floor[i][j] = 1.96 * \
                    np.sqrt(sd_per_elevator_and_floor[i][j] ** 2 / n_runs)

        # print the results
        print()
        print()
        print("probabilities matrix")
        print(np.round(mean_per_elevator_and_floor, 3))
        print()
        print("half widths matrix")
        print(np.round(hw_per_elevator_and_floor, 3))

    def question_4(self, n_runs, sim_time):
        """
                Method to answer question 3.

                :param n_runs:      The number of simulations
                :param sim_time:    The time each simulation runs, seconds.
        """

        chance_per_nr_elevators = []
        for nr_elevators in range(1, 11):
            chances = []
            nr_people = []
            for i in range(n_runs):
                simulation = Simulation(sim_time, nr_elevators)
                results = simulation.simulate()
                results.make_calculations()
                chances.append(results.chance_over_5_min_wait)
                nr_people.append(len(results.list_of_persons))
            # weight each result by the amount of people in the related simulation
            chance = 0
            for i in range(len(chances)):
                chance += chances[i]*nr_people[i]/sum(nr_people)
            chance_per_nr_elevators.append(chance)

        print("Q4: chance to wait long per nr of elevators:")
        print([str(i) + ":" + str(chance_per_nr_elevators[i]) +
              "\n" for i in range(len(chance_per_nr_elevators))])

    def question_5(self):
        pass

    def question_6(self, n_runs=100, sim_time=8*60*60, elevators=[1, 2, 3, 4, 5]):
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
        print()
        print()
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

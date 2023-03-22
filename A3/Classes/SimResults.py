import numpy as np

class SimulateResults:

    def __init__(self, nr_floors):

        """
        Class that keeps track of the important data and calculates the results.

        :param nr_floors:   The total number of floors the system has.
        """

        # Variables to store the data.
        self.list_of_persons = []                   # List of all persons who finished.
        self.people_in_elevator = [0, 0]            # Tuple: (summed number of people, count of up/down movements)

        # Variables to store the results.
        self.mean_waiting_time = -1                 # The mean waiting time until a person can enter an elevator.
        self.mean_people_in_elevator = -1           # The mean value of people in the elevator.
        self.prob_not_to_enter = [-1]*nr_floors     # The probability not being able to enter the elevator for floor i.

    def make_calculations(self):

        """
        Method that does all the necessary calculations. This method needs to be executed in order to have correct
        values in the variables used to store the results.
        """

        # Calculate mean waiting time.
        ##########################################
        total_waiting_time = 0
        for person in self.list_of_persons:
            total_waiting_time += person.enter_elevator - person.start_time
        self.mean_waiting_time = total_waiting_time / len(self.list_of_persons)

        # Calculate mean people in the elevator.
        ##########################################
        self.mean_people_in_elevator = self.people_in_elevator[0] / self.people_in_elevator[1]

        # Calculate probability not being able to board an elevator.
        ##########################################
        total_people_on_floor = [-1]*len(self.prob_not_to_enter)

        # Sum over all persons and the count how often they were not able to enter an elevator.
        # +1 because everybody was able to enter eventually.
        for person in self.list_of_persons:

            # In case someone used the stairs.
            #if -1 == person.could_not_enter_count:
            #    continue

            self.prob_not_to_enter[person.floor_nr] += person.could_not_enter_count
            total_people_on_floor[person.floor_nr] += person.could_not_enter_count + 1

        # Divide the total number of times someone was not able to enter by the total number of people on that floor.
        for i in range(len(self.prob_not_to_enter)):
            self.prob_not_to_enter[i] = self.prob_not_to_enter[i] / total_people_on_floor[i]

    def __str__(self):

        """
        Method to create a proper return string.
        """

        # Check implicitly whether the make_calculations method was already executed.
        if -1 == self.mean_waiting_time or -1 == self.mean_people_in_elevator:
            print("ERROR in Simulation Results: make_calculations was not executed yet.")
            return False

        tmp_str = "\nresults\n##################################\n"
        tmp_str += "mean waiting time: " + str(np.round(self.mean_waiting_time, 2)) + " [s]" + "\n"
        tmp_str += "mean people in elevator: " + str(np.round(self.mean_people_in_elevator, 2)) + "\n"
        tmp_str += "probability not to enter for floor i:\n----------------\n"

        for i in range(len(self.prob_not_to_enter)):
            tmp_str += "Floor " + str(i) + ": " + str(np.round(self.prob_not_to_enter[i], 3)) + "\n"

        tmp_str += "##################################\n"

        return tmp_str









import numpy as np


class SimulateResults:

    def __init__(self, extension_6, nr_floors=5):

        """
        Class that keeps track of the important data and calculates the results.
        Attention: Only mean_waiting_time and mean_waiting_time_2 have meaning if extension 6 is activated.

        :param extension_6: Bool. True if extension 6 is activated.
        :param nr_floors:   The total number of floors the system has.
        """

        # Variables to store the data.
        self.list_of_persons = []           # List of all persons who finished.
        self.people_in_elevator = [0, 0]    # Tuple: (summed number of people, count of up/down movements)
        self.list_impatient_persons = []    # List of people who took the stairs because they were too impatient.

        # Variables to store the results.
        self.mean_waiting_time = [-1]*nr_floors     # The mean waiting time per floor.
        self.mean_people_in_elevator = -1           # The mean value of people in the elevator.
        self.prob_not_to_enter = [-1]*nr_floors     # The probability not being able to enter the elevator for floor i.

        self.overall_mean_waiting_time = -1     # The overall mean waiting time over all floors.
        self.overall_mean_waiting_time_2 = -1   # The overall mean waiting time including people left due to impatience.

        # Other variables
        self.nr_floors = nr_floors                  # The number of floors of the system. For computational reasons.
        self.extension_6 = extension_6              # Bool. True if extension 6 is activated.
        self.make_calculations_executed = False     # Checks whether the method make_calculations was already executed.


    def make_calculations(self):

        """
        Method that decides which calculations need to be done and calls the corresponding method.
        This method needs to be executed in order to have correct values in the variables used to store the results.
        """

        # Switch make_calculations_executed to True.
        self.make_calculations_executed = True

        # Check whether extension 6 is activated.
        if self.extension_6:
            self.make_calculations_extension_6()
        else:
            self.make_calculations_normal()

    def make_calculations_normal(self):

        """
        Method that does all the necessary calculations in the normal case (extension 6 not activated)
        """

        # Calculate mean waiting time.
        ##########################################

        # Define two lists to hold the total numer of people and total waiting time on each floor.
        total_waiting_time = [0] * self.nr_floors
        total_people_on_floor = [0] * self.nr_floors

        # Do the calculations using a for loop and a division.
        for person in self.list_of_persons:
            total_waiting_time[person.floor_nr] += person.enter_elevator - person.start_time
            total_people_on_floor[person.floor_nr] += 1

        for i in range(self.nr_floors):
            self.mean_waiting_time[i] = total_waiting_time[i] / total_people_on_floor[i]

        # Calculate mean waiting time over all floors.
        ##########################################
        self.overall_mean_waiting_time = np.sum(total_waiting_time) / np.sum(total_people_on_floor)

        # Calculate mean people in the elevator.
        ##########################################
        self.mean_people_in_elevator = self.people_in_elevator[0] / self.people_in_elevator[1]

        # Calculate probability not being able to board an elevator.
        ##########################################

        # Define two lists to hold the total number of entry possibilities and occasions a person could not enter.
        total_could_not_enter = [0] * self.nr_floors
        total_possibilities = [0] * self.nr_floors

        # Sum over all persons and the count how often they were not able to enter an elevator.
        for person in self.list_of_persons:
            total_could_not_enter[person.floor_nr] += person.could_not_enter_count
            # +1 because everybody was able to enter eventually.
            total_possibilities[person.floor_nr] += person.could_not_enter_count + 1

        # Divide the total number of times someone was not able to enter by the total number of people on that floor.
        for i in range(self.nr_floors):
            self.prob_not_to_enter[i] = total_could_not_enter[i] / total_possibilities[i]

    def make_calculations_extension_6(self):

        """
        Method that does all the necessary calculations in the case that extension 6 is activated.
        """

        # Calculate mean waiting time.
        ##########################################

        # Define two lists to hold the total numer of people and total waiting time on each floor.
        total_waiting_time = 0
        total_people_on_floor = 0

        # Sum over all persons who were able to enter the elevator.
        for person in self.list_of_persons:
            total_waiting_time += person.enter_elevator - person.start_time
            total_people_on_floor += 1

        # Calculate the mean.
        self.overall_mean_waiting_time = total_waiting_time / total_people_on_floor

        # Sum over all persons who took the stairs because of impatience and add them.
        for person in self.list_impatient_persons:
            total_waiting_time += person.impatience
            total_people_on_floor += 1

        # Calculate the mean.
        self.overall_mean_waiting_time_2 = total_waiting_time / total_people_on_floor

    def __str__(self):

        """
        Method to create a proper return string.
        """

        # Check implicitly whether the make_calculations method was already executed.
        if not self.make_calculations_executed:
            print("ERROR in Simulation Results: make_calculations was not executed yet.")
            return False

        # Initialise return string.
        tmp_str = ""

        # Check if extension 6 is activated.
        if not self.extension_6:
            tmp_str += "\nresults\n##################################\n"
            tmp_str += "overall mean waiting time: " + str(np.round(self.overall_mean_waiting_time, 2)) + "\n"
            tmp_str += "mean waiting time per floor i:\n----------------\n"

            for i in range(self.nr_floors):
                tmp_str += "Floor " + str(i) + ": " + str(np.round(self.mean_waiting_time[i], 2)) + " [s]\n"

            tmp_str += "----------------\nmean people in elevator: " + str(np.round(self.mean_people_in_elevator, 2)) + "\n"
            tmp_str += "probability not to enter for floor i:\n----------------\n"

            for i in range(self.nr_floors):
                tmp_str += "Floor " + str(i) + ": " + str(np.round(self.prob_not_to_enter[i], 3)) + "\n"

            tmp_str += "##################################\n"

        else:
            tmp_str += "\nresults\n##################################\n"

            tmp_str += "mean waiting time: " + str(np.round(self.overall_mean_waiting_time, 2)) + "\n"
            tmp_str += "mean waiting time (incl. people left): " + str(np.round(self.overall_mean_waiting_time_2, 2))

            tmp_str += "\n##################################\n"

        return tmp_str









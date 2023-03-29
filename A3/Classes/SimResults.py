import numpy as np


class SimulateResults:

    def __init__(self, extension_6, nr_floors=5):
        """
        Class that keeps track of the important data and calculates the results.
        Attention: Only the "overall" variables are defined if extension 6 is activated.

        :param extension_6: Bool. True if extension 6 is activated.
        :param nr_floors:   The total number of floors the system has.
        """

        # Variable to control the data collection
        # The time after which peoples data is collected (warm up time)
        self.cut_off = -1

        # Variables to store the data.
        self.list_of_persons = []           # List of all persons who finished.
        # List of all people in elevator of all (up/down) movements.
        self.people_in_elevator_list = []
        # List of people who took the stairs because they were too impatient.
        #self.list_impatient_persons = []

        # Variables to store the results.
        # The mean waiting time per floor.
        self.mean_waiting_time = [-1]*nr_floors
        # Tme standard deviation per floor.
        self.sd_waiting_time = [-1]*nr_floors
        # The mean value of people in the elevator.
        self.mean_people_in_elevator = -1
        # The sd value of people in the elevator.
        self.sd_people_in_elevator = -1
        # The standard deviation of people in the elevator.
        self.sd_people_in_elevator = -1
        # The probability not being able to enter the elevator for floor i.
        self.prob_not_to_enter = [-1]*nr_floors

        # Overall variables. Metrics over all floors combined.
        # The overall mean waiting time over all floors.
        self.overall_mean_waiting_time = -1
        # The overall standard deviation over all floors.
        self.overall_sd_waiting_time = -1
        # The overall mean waiting time including people left due to impatience.
        self.overall_mean_waiting_time_2 = -1
        # The overall sd waiting time including people left due to impatience.
        self.overall_sd_waiting_time_2 = -1
        # The overall mean "impatience time". So mean time until a person will take the stairs.
        self.overall_mean_impatience = -1
        # The overall sd "impatience time". So mean time until a person will take the stairs.
        self.overall_sd_impatience = -1
        # The overall number of people took the stairs because of impatience.
        self.overall_percentage_stairs = -1

        # Other variables
        # The number of floors of the system. For computational reasons.
        self.nr_floors = nr_floors
        # Bool. True if extension 6 is activated.
        self.extension_6 = extension_6
        # Checks whether the method make_calculations was already executed.
        self.make_calculations_executed = False

        # variable for question 4
        self.chance_over_5_min_wait = None

    def make_calculations(self, cut_off=2028):
        """
        Method that decides which calculations need to be done and calls the corresponding method.
        This method needs to be executed in order to have correct values in the variables used to store the results.
        """

        if self.make_calculations_executed:
            print(
                "make_calculations already executed. This may lead to unwanted behaviour")

        # Switch make_calculations_executed to True.
        self.make_calculations_executed = True

        # Save how many people were cut off
        self.cut_off = cut_off
        # Cut of the first x persons.
        self.list_of_persons = self.list_of_persons[cut_off:]

        if len(self.list_of_persons) < 1:
            print("no persons in self.list_of_persons the simulation is not long enough or the cut off is to large")
            return

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

        # Define 2D-list of all waiting times and floors.
        waiting_times = [[] for i in range(self.nr_floors)]

        # list needed for deciding warm-up cutoff point
        self.one_dim_list_of_waiting_times = np.zeros(
            len(self.list_of_persons))

        # Sum over all finished persons
        for i, person in enumerate(self.list_of_persons):
            tmp_waiting_time = person.enter_elevator - person.start_time
            waiting_times[person.floor_nr].append(tmp_waiting_time)
            self.one_dim_list_of_waiting_times[i] = tmp_waiting_time

        for i in range(self.nr_floors):
            self.mean_waiting_time[i] = np.mean(waiting_times[i])

        # Calculate standard deviation of the waiting times per floor
        ##########################################
        for i in range(self.nr_floors):
            self.sd_waiting_time[i] = np.std(waiting_times[i])

        # Calculate mean waiting time over all floors.
        ##########################################
        all_waiting_times = []
        for i in range(len(waiting_times)):
            all_waiting_times += waiting_times[i]
        self.overall_mean_waiting_time = np.mean(all_waiting_times)

        # Calculate sd of the waiting times over all floors.
        ##########################################
        self.overall_sd_waiting_time = np.std(all_waiting_times)

        # Calculate mean and sd of people in the elevator.
        ##########################################
        self.mean_people_in_elevator = np.mean(self.people_in_elevator_list)
        self.sd_people_in_elevator = np.std(self.people_in_elevator_list)

        # Calculate probability not being able to board an elevator.
        ##########################################

        # Define two lists to hold the total number of entry possibilities and occasions a person could not enter.
        total_could_not_enter = [0] * self.nr_floors
        total_possibilities = [0] * self.nr_floors

        # Sum over all persons and the count how often they were not able to enter an elevator.
        count_wait_over_5_min = 0
        for person in self.list_of_persons:
            total_could_not_enter[person.floor_nr] += person.could_not_enter_count
            # +1 because everybody was able to enter eventually.
            total_possibilities[person.floor_nr] += person.could_not_enter_count + 1

            # check how many waited over 5 minutes
            if person.start_time + 300 < person.enter_elevator:
                count_wait_over_5_min += 1
        # calculate fraction of people waiting over 5 minutes
        self.chance_over_5_min_wait = count_wait_over_5_min / \
            len(self.list_of_persons)

        # Divide the total number of times someone was not able to enter by the total number of people on that floor.
        for i in range(self.nr_floors):
            try:
                self.prob_not_to_enter[i] = total_could_not_enter[i] / \
                    total_possibilities[i]
            except ZeroDivisionError:
                self.prob_not_to_enter[i] = 0

    def make_calculations_extension_6(self):
        """
        Method that does all the necessary calculations in the case that extension 6 is activated.
        """

        # Define 2D-list of all waiting times and floors.
        waiting_times = []
        impatient_times = []

        # Calculation for percentage. Sum over all people who took the stairs/elevator.
        sum_elevator = 0
        sum_stairs = 0

        # Sum over all finished persons
        for person in self.list_of_persons:
            impatient_times.append(person.impatience)
            if not person.took_stairs:
                sum_elevator += 1
                tmp_waiting_time = person.enter_elevator - person.start_time
                waiting_times.append(tmp_waiting_time)

        self.overall_mean_waiting_time = np.mean(waiting_times)
        self.overall_sd_waiting_time = np.std(waiting_times)

        # Calculate the mean impatience time.
        self.overall_mean_impatience = np.mean(impatient_times)
        self.overall_sd_impatience = np.std(impatient_times)

        # Sum over all finished persons
        for person in self.list_of_persons:
            if person.took_stairs:
                sum_stairs += 1
                tmp_waiting_time = person.impatience
                waiting_times.append(tmp_waiting_time)

        self.overall_mean_waiting_time_2 = np.mean(waiting_times)
        self.overall_sd_waiting_time_2 = np.std(waiting_times)

        # Calculate the percentage
        self.overall_percentage_stairs = sum_stairs / (sum_elevator + sum_stairs)

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
            tmp_str += "overall mean waiting time: " + \
                str(np.round(self.overall_mean_waiting_time, 2)) + "\n"
            tmp_str += "mean waiting time per floor i:\n----------------\n"

            for i in range(self.nr_floors):
                tmp_str += "Floor " + \
                    str(i) + ": " + \
                    str(np.round(self.mean_waiting_time[i], 2)) + " [s]\n"

            tmp_str += "----------------\nmean people in elevator: " + \
                str(np.round(self.mean_people_in_elevator, 2)) + "\n"
            tmp_str += "probability not to enter for floor i:\n----------------\n"

            for i in range(self.nr_floors):
                tmp_str += "Floor " + \
                    str(i) + ": " + \
                    str(np.round(self.prob_not_to_enter[i], 3)) + "\n"

            tmp_str += f"chance to wait over 5 minutes for an elevator: {self.chance_over_5_min_wait:.4f}"

            tmp_str += "\n##################################\n"

        else:
            tmp_str += "\nresults\n##################################\n"

            tmp_str += "mean waiting time: " + \
                str(np.round(self.overall_mean_waiting_time, 2)) + "\n"
            tmp_str += "mean waiting time (incl. people left): " + \
                str(np.round(self.overall_mean_waiting_time_2, 2))

            tmp_str += "\n##################################\n"

        return tmp_str

class SimulateResults:

    def __init__(self):

        self.list_of_persons = []           # List of all persons who finished.
        self.people_in_elevator = [0, 0]    # Tuple: (summed number of people, count of up/down movements)

        self.mean_waiting_time = -1         # The mean waiting time until a person can enter an elevator.

    def make_calculations(self):

        # Calculate mean waiting time
        total_waiting_time = 0
        for person in self.list_of_persons:
            total_waiting_time += person.enter_elevator - person.start_time
        self.mean_waiting_time = total_waiting_time / len(self.list_of_persons)


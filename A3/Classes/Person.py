

class Person():

    def __init__(self, destination, start_time):
        """
        Class that represents a person, has a destination and a starting time
        :param destination: the floor this person wants to go to
        :param start_time: the moment this person started waiting for an elevator
        """

        self.destination = destination
        self.start_time = start_time

        self.enter_elevator = -1        # The time the Person has finished entering the elevator.
        self.leave_elevator = -1        # The time the Person has finished exiting the elevator.

        self.could_not_enter_count = 0  # Counts how often a person could not enter.

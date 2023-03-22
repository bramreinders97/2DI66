

class Person():

    def __init__(self, destination, start_time, floor_nr):
        """
        Class that represents a person, has a destination and a starting time for the logic and keeps track of other
        important data as well.

        :param destination:     the floor this person wants to go to
        :param start_time:      the moment this person started waiting for an elevator

        :param floor_nr:        The number of the floor where the person enters the system.
        """

        self.destination = destination
        self.start_time = start_time

        self.enter_elevator = -1        # The time the person enters the elevator. (starting time + waiting + entering)
        self.leave_elevator = -1        # The time the person leaves the elevator. (... + traveling + exiting)

        self.floor_nr = floor_nr        # The floor number where the person enters the elevator.
        self.could_not_enter_count = 0  # Counts how often a person could not enter.

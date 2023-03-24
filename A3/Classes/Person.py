import numpy as np

class Person():

    def __init__(self, destination, start_time, floor_nr, impatience_base=180, impatience_add=20):
        """
        Class that represents a person, has a destination and a starting time for the logic and keeps track of other
        important data as well.

        :param destination:     the floor this person wants to go to
        :param start_time:      the moment this person started waiting for an elevator

        :param impatience_base: The base mean waiting time till someone will take the stairs.
        :param impatience_add:  Addition to the mean waiting time for each floor.

        :param floor_nr:        The number of the floor where the person enters the system.
        """

        self.destination = destination
        self.start_time = start_time

        # The time until a person takes the stairs instead of the elevator.
        impatience_mean = impatience_base + abs(floor_nr-destination) * impatience_add
        self.impatience = np.random.normal(impatience_mean)

        # Variables in order to collect the data
        self.enter_elevator = -1        # The time the person enters the elevator. (starting time + waiting + entering)
        self.leave_elevator = -1        # The time the person leaves the elevator. (... + traveling + exiting)

        self.floor_nr = floor_nr        # The floor number where the person enters the elevator.
        self.could_not_enter_count = 0  # Counts how often a person could not enter.



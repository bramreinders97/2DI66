

class Person():

    def __init__(self, destination, start_time):
        """
        Class that represents a person, has a destination and a starting time
        :param destination: the floor this person wants to go to
        :param start_time: the moment this person started waiting for an elevator
        """

        self.destination = destination
        self.start_time = start_time

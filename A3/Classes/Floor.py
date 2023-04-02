from A3.Classes.Event import Event
import numpy as np
from A3.Classes.Person import Person

class Floor():
    def __init__(self, floor_nr, probs, arrive_rate, extension_5):
        """
        Class that represents a floor. Has a list of queueing people.

        :param probs: list of probabilities for the destination of new people.
        :param arrive_rate: the arrival rate in people per minute for the poisson process
        :param extension_5: Whether to adjust the algorithm to run with the model extension for Q5
        """

        self.probs = probs
        self.arrive_rate = arrive_rate/60 #convert to seconds
        self.floor_nr = floor_nr
        self.up_queue = []
        self.down_queue = []
        self.extension_5 = extension_5

    def add_to_queue(self, person):
        """
        Adds a new person to the correct queue
        :param person: A person object that is to be added to a queue
        :return:
        """
        if self.extension_5 and self.floor_nr in [0,1,2]:
            if person.destination < self.floor_nr:
                #in the extension 5, remove people who are going down
                return
        if person.destination < self.floor_nr:
            self.down_queue.append(person)
        else:
            self.up_queue.append(person)

    def schedule_next_event(self, t):
        """
        Schedules the next queuer event for this floor and returns it fot putting on the heap.

        :param t: Current time
        :return: The next new_queuer event for this floor
        """
        return Event(0, t+np.random.exponential(1/self.arrive_rate), floor = self)

    def new_queuer(self, t, extension_6):
        """
        Adds a new person to the correct queue
        :param t: The time of the system.
        :param extension_6: Whether a system of impatience is implemented.
        :return: The next new_queuer event for this floor
        """
        # choose destination for person based on probs
        destination = np.random.choice([0,1,2,3,4], p = self.probs)
        self.add_to_queue(Person(destination, t, self.floor_nr, extension_6))
        return self.schedule_next_event(t)

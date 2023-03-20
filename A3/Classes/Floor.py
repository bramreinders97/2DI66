from A3.Classes.Event import Event
import numpy as np
from A3.Classes.Person import Person

class Floor():
    def __init__(self, floor_nr, probs, arrive_rate):
        """
        Class that represents a floor. Has a list of queueing people.

        :param probs: list of probabilities for the destination of new people.
        :param arrive_rate: the arrival rate in people per minute for the poisson process
        """

        self.probs = probs
        self.arrive_rate = arrive_rate
        self.floor_nr = floor_nr
        self.up_queue = []
        self.down_queue = []

    def add_to_queue(self, person):
        """
        Adds a new person to the correct queue
        :param person:
        :return:
        """
        if person.destination < self.floor_nr:
            self.down_queue.append(person)
        else:
            self.up_queue.append(person)

    def schedule_next_event(self, t):
        return Event(0, t+np.random.exponential(self.arrive_rate), floor = self)

    def new_queuer(self, t):
        #choose destination for person based on probs
        destination = np.random.choice([0,1,2,3,4], p = self.probs)
        self.add_to_queue(Person(destination, t))
        return self.schedule_next_event(t)

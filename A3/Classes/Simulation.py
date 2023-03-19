from Elevator import Elevator
from Floor import Floor
import heapq

class Simulation:

    def __init__(self, T, nr_elevators, probs, arrive_rate =(13.1, 3.4, 2.1, 9.2, 8.8)):
        """
        Prepares a single simulation to be ran for A3, creating elevators.
        :param T: The ending time for this simulation
        :param nr_elevators: The number of elevators desired in this simulation
        """

        self.T = T
        self.t = 0 #current time

        self.elevators = [Elevator() for i in range(nr_elevators)]
        self.floors = [Floor(i, probs[i], arrive_rate[i]) for i in range(5)]

        self.event_list = [] #list of events that still need to happen during simulation
        #types of events: enter elevator, leave elevator, elevator reaches a new floor, person arrives at queue

    def simulate(self):
        """
        Run a simulation with the given parameters
        :return:
        """

        #add starting events: all elevators start to move & all floors schedule their first group arriving

        while self.T > self.t:
            event = heapq.heappop(self.event_list)[1]
            self.t = event.t

            #handle the events
            new_event = event.handle_event()

            heapq.heappush(self.event_list, (new_event.t, new_event))

from A3.Classes.Elevator import Elevator
from A3.Classes.Floor import Floor
from A3.Classes.SimResults import SimulateResults
import heapq

class Simulation:

    def __init__(self, T, nr_elevators, probs = None, arrive_rate =(13.1, 3.4, 2.1, 9.2, 8.8)):
        """
        Prepares a single simulation to be ran for A3, creating elevators.
        :param T: The ending time for this simulation
        :param nr_elevators: The number of elevators desired in this simulation
        """

        self.T = T
        self.t = 0 #current time

        if probs == None:
            probs = [[0, 0.1, 0.3, 0.4, 0.2],
                     [0.7, 0, 0.1, 0.1, 0.1],
                     [0.6, 0.2, 0, 0.1, 0.1],
                     [0.6, 0.2, 0.1, 0, 0.1],
                     [0.5, 0.2, 0.2, 0.1, 0]]

        self.elevators = [Elevator(i) for i in range(nr_elevators)]
        self.floors = [Floor(i, probs[i], arrive_rate[i]) for i in range(5)]

        self.event_list = [] #list of events that still need to happen during simulation
        #types of events: enter elevator, leave elevator, elevator reaches a new floor, person arrives at queue

    def simulate(self):
        """
        Run a simulation with the given parameters
        :return:
        """

        simulation_results = SimulateResults()

        #add starting events: all elevators start to move & all floors schedule their first group arriving
        for elevator in self.elevators:
            event = elevator.schedule_next_event(self.t, self.floors[elevator.floor])
            event.floor = self.floors[event.destination_floor]
            heapq.heappush(self.event_list, (event.t, event))
        for floor in self.floors:
            event = floor.schedule_next_event(self.t)
            heapq.heappush(self.event_list, (event.t, event))

        print("list of starting events:")
        for i in self.event_list:
            print(i[1])
        print("list finished")

        while self.T > self.t:
            event = heapq.heappop(self.event_list)[1]
            self.t = event.t

            #handle the events
            new_event, finished_person = event.handle_event()

            if finished_person:
                simulation_results.list_of_persons.append(finished_person)
                print("hi")

            if new_event.event_type == 1:
                #rewrite the floor nr into the actual floor
                new_event.floor = self.floors[new_event.destination_floor]

            print(f"time: {self.t:.2f}, added {new_event}")

            heapq.heappush(self.event_list, (new_event.t, new_event))

        return simulation_results

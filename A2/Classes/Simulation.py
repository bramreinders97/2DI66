from A2.Classes.Event import Event
from A2.Classes.Queues import Queues

import numpy as np
import heapq


class Simulation:
    #def __init__(self, arrivalDist, pickFoodDist, serveCustCardDist, serveCustCashDist, extension_1=False, extension_2=False, extension_3=False):
    #    self.arrivalDist = arrivalDist
    #    self.pickFoodDist = pickFoodDist
    #    self.serveCustCardDist = serveCustCardDist
    #    self.serveCustCashDist = serveCustCashDist
    #    self.extension_1 = extension_1
    #    self.extension_2 = extension_2
    #    self.extension_3 = extension_3

    def __init__(self):
        self.T = 3600   # one hour -> 3600 s
        self.t = 0      # starting time

        self.event_list = []

        self.next_group_id = 0  # A counter to track the next group ID

    def simulate(self):

        # Create Queues
        queues = Queues()
        queues.add_queue()
        queues.add_queue()
        queues.add_queue()

        # Push first event onto the event_list
        event = Event(0, self.t)
        heapq.heappush(self.event_list, (event.t, event))

        # Main loop
        while self.t < self.T:

            # get next element from the event list
            event = heapq.heappop(self.event_list)[1]
            self.t = event.t

            if 0 == event.type:
                tmp_events = event.handle_arrival_event(self.next_group_id)
                self.next_group_id += 1
                self.schedule_events(tmp_events)

            elif 1 == event.type:
                tmp_events = event.handle_enter_queue_event(queues)
                self.schedule_events(tmp_events)

            elif 2 == event.type:
                tmp_events = event.handle_depature_event(queues.queues[event.customer.queue])
                self.schedule_events(tmp_events)

            else:
                print("ERROR: in simulat: unknown event type")
                break

            #print("Type: " + str(event.type) + " " + str(queues.queues[0].customers_in_queue) + " " + str(queues.queues[1].customers_in_queue) + " " + str(queues.queues[2].customers_in_queue))
        #print(queues.queues[0].integral/self.t)

    def schedule_events(self, events):

        for event in events:
            heapq.heappush(self.event_list, (event.t, event))


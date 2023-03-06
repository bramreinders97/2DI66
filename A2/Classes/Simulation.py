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

    def __init__(self, queue_speeds=[1, 1, 1], mobile_store=0, card_only=False):
        self.T = 3600           # End time: one hour -> 3600 s
        self.t = 0              # starting time

        self.queue_speeds = queue_speeds  # Determines how many queses there are and how fast they are
        self.mobile_store = mobile_store  # Determines whether there is a mobile store and how many groups are using it.
        self.card_only = card_only        # Determines whether only payment by card is accepted.

        self.event_list = []    # Event list

        self.next_group_id = 0  # A counter to track the next group ID

        self.finished_customer_list = []  # A list of all finished customers
        self.group_time_list = []         # A list of a 2D array: (max serving time, nr. of group members in the system)

    def simulate(self):

        # Create Queues
        queues = Queues()
        for queue_speed in self.queue_speeds:
            queues.add_queue(queue_speed)

        # Push first event onto the event_list
        event = Event(0, self.t)
        heapq.heappush(self.event_list, (event.t, event))

        # Main loop
        while self.t < self.T:

            # get next element from the event list
            event = heapq.heappop(self.event_list)[1]
            self.t = event.t

            if 0 == event.type:
                tmp_events = event.handle_arrival_event(self.next_group_id, self.mobile_store, self.card_only)
                self.next_group_id += 1
                self.schedule_events(tmp_events)

                # -1 because there is one type 0 event which must be excluded.
                self.group_time_list.append([-1, len(tmp_events)-1])

            elif 1 == event.type:
                tmp_events = event.handle_enter_queue_event(queues)
                self.schedule_events(tmp_events)

            elif 2 == event.type:

                # update queue
                updated_queue = event.handle_departure_event(queues.queues[event.customer.queue])
                queues.queues[event.customer.queue] = updated_queue

                # update and save customer
                event.customer.departure_time = self.t
                self.finished_customer_list.append(event.customer)

                # update group_time_list
                customer_time = event.customer.departure_time - event.customer.arrival_time
                max_time = max(self.group_time_list[event.customer.group_index][0], customer_time)
                self.group_time_list[event.customer.group_index][0] = max_time
                self.group_time_list[event.customer.group_index][1] -= 1

            else:
                print("ERROR: in simulate: unknown event type")
                break

    def schedule_events(self, events):

        for event in events:
            heapq.heappush(self.event_list, (event.t, event))


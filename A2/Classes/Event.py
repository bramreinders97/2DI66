import math

from A2.Classes.Customer import Customer

class Event:

    ARRIVAL = 0
    ENTER_QUEUE = 1
    DEPARTURE = 2

    def __init__(self, event_type, t, customer=None):
        self.type = event_type
        self.t = t
        self.customer = customer

    def handle_arrival_event(self, group_id):

        new_events = []

        # TODO: Distribution
        n_group_members = 3

        # TODO: Poisson Process
        time_till_next_arrival = 120    # The time until the next group arrives

        # Create an ENTER_QUEUE event for all customers in the group
        for i in range(n_group_members):

            tmp_customer = Customer(self.t, group_id)
            new_events.append(Event(1, self.t + tmp_customer.get_food_time, tmp_customer))

        # Create one new ARRIVAL event.
        new_events.append(Event(0, self.t + time_till_next_arrival))

        return new_events

    def handle_enter_queue_event(self, queues):
        new_events = []

        # get shortest queue (when equal the highest index is taken)
        shortest_queue = queues.queues[0].customers_in_queue
        shortest_queue_id = 0
        for i in range(1, len(queues.queues)):
            if queues.queues[i].customers_in_queue <= shortest_queue:
                shortest_queue_id = i

        # update to queue
        time_needed = queues.queues[shortest_queue_id].update_queue(self.t, self.customer.payment_method)

        new_events.append(Event(2, self.t + time_needed, self.customer))

        return new_events

    def handle_depature_event(self):

        new_events = []

        return new_events

    def __lt__(self, other):
        return self.t < other.t

    def __str__(self):
        return "Type: " + str(self.type) + "   Time: " + str(self.t)

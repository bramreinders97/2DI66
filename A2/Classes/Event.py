import random

from A2.Classes.Customer import Customer

class Event:

    ARRIVAL = 0
    ENTER_QUEUE = 1
    DEPARTURE = 2

    def __init__(self, event_type, t, customer=None):
        self.type = event_type      # Type of the event
        self.t = t                  # Time of the event
        self.customer = customer    # Customer linked to the event

    def handle_arrival_event(self, group_id, mobile_store, card_only):

        new_events = []

        # TODO: Distribution
        n_group_members = 3

        # Get the arrival time of the next group
        if not mobile_store:
            # TODO: Poisson Process
            time_till_next_arrival = 15    # The time until the next group arrives
        else:
            time_till_next_arrival = 0
            while True:
                # TODO: Poisson Process
                time_till_next_arrival += 15
                tmp = random.random()
                if tmp > mobile_store:
                    break

        # Create an ENTER_QUEUE event for all customers in the group
        for i in range(n_group_members):
            tmp_customer = Customer(self.t, group_id, card_only)
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
        time_needed = queues.queues[shortest_queue_id].update_queue_type_1(self.t, self.customer.payment_method)

        # create new DEPATURE event
        self.customer.queue = shortest_queue_id
        new_events.append(Event(2, self.t + time_needed, self.customer))

        return new_events

    def handle_departure_event(self, queue):
        queue.update_queue_type_2(self.t)
        return queue

    def __lt__(self, other):
        return self.t < other.t

    def __str__(self):
        return "Type: " + str(self.type) + "   Time: " + str(self.t)

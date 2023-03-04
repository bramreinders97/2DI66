from A2.Classes.Customer import Customer

import random

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

            # Decide for cash or card
            tmp = random.random()
            if tmp <= 0.4:
                payment_method = "cash"
            else:
                payment_method = "card"

            # Decide how long the Customer needs to get the food
            # TODO: Distribution
            get_food_time = 80

            tmp_customer = Customer(self.t, payment_method, group_id, get_food_time)
            new_events.append(Event(1, self.t + get_food_time, tmp_customer))

        # Create one new ARRIVAL event.
        new_events.append(Event(0, self.t + time_till_next_arrival))

        return new_events

    def __lt__(self, other):
        return self.t < other.t

    def __str__(self):
        return "Type: " + str(self.type) + "   Time: " + str(self.t)

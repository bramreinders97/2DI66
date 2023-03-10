import random
from A2.Classes.Customer import Customer
from A2.Classes.Generators import geo_distr, next_group_arriving


class Event:

    ARRIVAL = 0
    ENTER_QUEUE = 1
    DEPARTURE = 2

    def __init__(self, event_type, t, customer=None):
        """
        Class that represents an event and handles the different types of events

        :param event_type:  int.    The type of the event. (0: ARRIVAL, 1: ENTER_QUEUE, 2: DEPARTURE)
        :param t:           float.  The time of the event
        :param customer:    class.  The customer who is linked to the event.
        """

        self.type = event_type      # Type of the event
        self.t = t                  # Time of the event
        self.customer = customer    # Customer linked to the event

    def handle_arrival_event(self, group_id, mobile_store, card_only, lam):
        """
        Handles a type zero (ARRIVAL) event.

        :param group_id:        int.    The id of the next group.
        :param mobile_store:    float.  The percentage if a group chooses the mobile store. 0 if there is no
                                        mobile store.
        :param card_only:       bool.   True if only payment by card is accepted.
        :param lam:             float.  Lambda, the rate of new groups arriving per minute
        """

        # Initialize a list of new events to be added.
        new_events = []

        # get the number of Customers in the group.
        # Geometric distribution with mean 3

        n_group_members = geo_distr(3)

        # Get the arrival time of the next group
        if not mobile_store:

            time_till_next_arrival = next_group_arriving(lam)#30        # The time until the next group arrives
        else:
            time_till_next_arrival = 0
            # Iterate as long as one group does not choose the mobile store.
            while True:

                time_till_next_arrival += next_group_arriving(lam)    # The time until the next group arrives
                tmp = random.random()
                if tmp > mobile_store:
                    break

        # Create an ENTER_QUEUE event for all customers in the group
        for i in range(n_group_members):
            tmp_customer = Customer(self.t, group_id, card_only)
            new_events.append(
                Event(1, self.t + tmp_customer.get_food_time, tmp_customer))

        # get the number of new people in the canteen
        new_people_in_canteen = len(new_events)

        # Create one new ARRIVAL event.
        # Only do this if self.t < 3600. This is done to ensure that we keep going once
        # the hour is over until everyone left without having new people enter
        new_arrival_time = self.t + time_till_next_arrival
        if new_arrival_time < 3600:  # to be changed back to 3600 after testing period
            new_events.append(Event(0, new_arrival_time))

        # Return the list of new events to be added.
        return new_events, new_people_in_canteen

    def handle_enter_queue_event(self, queues):
        """
        Handles a type one (ENTER_QUEUE) event.

        :param queues:  Class.  A class that contains all the information about the queues.
        """

        # Initialize a list of new events to be added.
        new_events = []

        # An array that holds the index of the shortest queue or queues in cse of a tie
        tie_queue_ids = []

        # get shortest queue (when equal ties are broken randomly)
        # The queue with the index 0 is initialized as the first entry.
        shortest_queue = queues.queues[0].customers_in_queue
        tie_queue_ids.append(0)

        # A for-loop through all the queues except the first one.
        for i in range(1, len(queues.queues)):

            # In the case of a lower value the list od ids is newly crated with only the ned index as an entry.
            if queues.queues[i].customers_in_queue < shortest_queue:
                tie_queue_ids = [i]
                shortest_queue = queues.queues[i].customers_in_queue

            # If there is a tie the index of the other queue is added to the list.
            elif queues.queues[i].customers_in_queue == shortest_queue:
                tie_queue_ids.append(i)

        # Pick a random id form the list.
        shortest_queue_id = random.choice(tie_queue_ids)

        # Register the moment this customer enters the queue
        self.customer.log_enter_queue_time(self.t)

        # update to queue
        time_needed = queues.queues[shortest_queue_id].update_queue_type_1(
            self.t, self.customer.payment_method)

        # create new DEPATURE event
        self.customer.queue = shortest_queue_id
        new_events.append(Event(2, self.t + time_needed, self.customer))

        # Return the list of new events to be added.
        return new_events

    def handle_departure_event(self, queue):
        """
        Handles a type two (DEPARTURE) event.

        :param queue:  Class.  A class that contains all the information about the queue the Customer belongs to.
        """
        queue.update_queue_type_2(self.t)
        return queue

    def __lt__(self, other):
        return self.t < other.t

    def __str__(self):
        return "Type: " + str(self.type) + "   Time: " + str(self.t)

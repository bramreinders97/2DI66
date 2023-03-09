import random


class Customer:
    def __init__(self, arrival_time, group_index, card_only):
        """
        Class that represents a customer.

        :param arrival_time:    float.  The arrival-time of the customer.
        :param group_index:     int.    The index of the group the customer belongs to.
        :param card_only:       bool.   True if only card payment is allowed.
        """

        self.arrival_time = arrival_time    # Arrival-time of the customer.
        # Departure-time of the customer. -1 if still in the system.
        self.departure_time = -1

        # can either be "cash" or "card".
        self.payment_method = self.get_payment_method(card_only)
        # time the customer needs to find the products he/she likes.
        self.get_food_time = self.get_food_time()

        # The index of the group the customer belongs to.
        self.group_index = group_index
        # The queue to which the customer belongs to.
        self.queue = None

    def get_payment_method(self,  card_only):
        """
        Decides the payment method of the customer. This is done at random if not specified otherwise.

        :param card_only:    bool.  True if only card payment is allowed.
        """

        tmp = random.random()
        if card_only or tmp > 0.4:
            return "card"
        else:
            return "cash"

    def get_food_time(self):
        """
        Decides how long the customer needs to get his/her food. The decision is made according to a distribution.
        """

        # Decide how long the Customer needs to get the food
        # TODO: Distribution
        return 5

    def log_enter_queue_time(self, t):
        """
        Register the time a customer enters a queue

        :param t: float. The current time
        """
        self.enter_queue_time = t

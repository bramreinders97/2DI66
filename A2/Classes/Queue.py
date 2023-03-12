from A2.Classes.Generators import expo_distr

class Queue:

    def __init__(self, cashier_speed):

        """
        Class that represents one queue.

        :param cashier_speed:   float.  Determines the speed of the cashier in percent. (0.15 := 15%)
        """

        self.cashier_speed = cashier_speed  # The speed of the cashier in percent.

        self.time_till_finished = 0         # The time needed in order to serve all customers.
        self.customers_in_queue = 0         # The customers currently in the queue
        self.last_update = 0                # The time the queue was updated the last time.

        self.integral = 0                   # The numeric integral of the customers in the queue over time.

    def update_queue_type_1(self, t, payment_method):

        """
        Update the queue according to a type 1 (ENTER_QUEUE) event.

        :param t:               float.  The current time
        :param payment_method:  string. The payment method of the customer added to this queue
        """

        # Determine the time the cashier needs to server the customer
        if "cash" == payment_method:
            # Exponential distribution with mean 20
            time_needed_for_customer = expo_distr(20)
        elif "card" == payment_method:
            # exponential distribution with mean 12
            time_needed_for_customer = expo_distr(12)
        else:
            print("ERROR: in queue: payment method")
            return False

        # Multiply by the individual cashier speed.
        time_needed_for_customer *= self.cashier_speed

        # Update queue parameters
        time_passed = t - self.last_update
        self.integral += (time_passed * self.customers_in_queue)
        self.customers_in_queue += 1
        self.time_till_finished = max(self.time_till_finished - time_passed, 0) + time_needed_for_customer
        self.last_update = t

        # return time_till_finished to schedule the DEPARTURE event.
        return self.time_till_finished

    def update_queue_type_2(self, t):

        """
        Update the queue according to a type 2 (DEPARTURE) event.

        :param t:               float.  The current time
        """

        # Update queue parameters
        time_passed = t - self.last_update
        self.integral += (time_passed * self.customers_in_queue)
        self.customers_in_queue -= 1
        self.time_till_finished = self.time_till_finished - time_passed
        self.last_update = t

class Queue:

    def __init__(self, cashier_speed):

        self.cashier_speed = cashier_speed

        self.time_till_finished = 0
        self.customers_in_queue = 0
        self.last_update = -1

        self.integral = 0

    def update_queue(self, t, payment_method):

        # Determine the time the cashier needs to server the customer
        if "cash" == payment_method:
            # TODO: Distribution
            time_needed_for_customer = 20
        elif "card" == payment_method:
            # TODO: Distribution
            time_needed_for_customer = 12
        else:
            print("ERROR: in queue: payment method")
            return False

        time_needed_for_customer *= self.cashier_speed

        # Update queue parameters
        time_passed = t - self.last_update
        self.integral += (time_passed * self.customers_in_queue)
        self.customers_in_queue += 1
        self.time_till_finished = self.time_till_finished - time_passed + time_needed_for_customer
        self.last_update = t

        # return time_till_finished to schedule the DEPARTURE event.
        return self.time_till_finished




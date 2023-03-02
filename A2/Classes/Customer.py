class Customer:
    def __init__(self, arrival_time, payment_method, group_index):
        self.arrival_time = arrival_time
        self.payment_method = payment_method  # card/cash
        self.group_index = group_index  # specify to which group the customer belongs
        self.enter_queue_time = None  # the time at which the customer enters a queue
        self.queue = None  # the queue a customer is in

    def enter_queue(self, t):
        # Record the time the customer enters a queue -> update self.queue and self.enter_queue_time
        pass

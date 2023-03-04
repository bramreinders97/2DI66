
class Customer:
    def __init__(self, arrival_time, payment_method, group_index, get_food_time):
        self.arrival_time = arrival_time
        self.departure_time = -1

        self.payment_method = payment_method    # card/cash
        self.get_food_time = get_food_time      # time the customer needs to find the products he/she likes.

        self.group_index = group_index  # specify to which group the customer belongs
        self.queue = None               # the queue a customer is in



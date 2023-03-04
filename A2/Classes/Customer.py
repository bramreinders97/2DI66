import random

class Customer:
    def __init__(self, arrival_time, group_index):
        self.arrival_time = arrival_time
        self.departure_time = -1

        self.payment_method = self.get_payment_method()     # card/cash
        self.get_food_time = self.get_food_time()           # time the customer needs to find the products he/she likes.

        self.group_index = group_index  # specify to which group the customer belongs
        self.queue = None               # the queue a customer is in


    def get_payment_method(self):

        tmp = random.random()
        if tmp <= 0.4:
            return "cash"
        else:
            return "card"

    def get_food_time(self):

        # Decide how long the Customer needs to get the food
        # TODO: Distribution
        return 80



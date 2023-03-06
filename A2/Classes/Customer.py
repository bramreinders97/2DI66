import random

class Customer:
    def __init__(self, arrival_time, group_index, card_only):
        self.arrival_time = arrival_time
        self.departure_time = -1

        self.payment_method = self.get_payment_method(card_only)     # card/cash
        self.get_food_time = self.get_food_time()           # time the customer needs to find the products he/she likes.

        self.group_index = group_index  # specify to which group the customer belongs
        self.queue = None               # the queue a customer is in

    def get_payment_method(self,  card_only):

        tmp = random.random()
        if card_only or tmp > 0.4:
            return "card"
        else:
            return "cash"

    def get_food_time(self):

        # Decide how long the Customer needs to get the food
        # TODO: Distribution
        return 80



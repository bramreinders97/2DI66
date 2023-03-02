class Event:

    ARRIVAL = 0
    ENTER_QUEUE = 1
    DEPARTURE = 2

    def __init__(self, event_type, time, customer):
        self.type = event_type
        self.time = time
        self.customer = customer

    def __lt__(self, other):
        return self.time < other.time

from A2.Classes.Queue import Queue

class Queues:

    def __init__(self):

        self.queues = []

    def add_queue(self, cashier_speed=1):
        tmp_queue = Queue(cashier_speed)
        self.queues.append(tmp_queue)


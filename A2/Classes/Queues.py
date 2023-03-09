from A2.Classes.Queue import Queue

class Queues:

    def __init__(self):

        """
        Class that hold all queues in the system.
        """

        self.queues = []    # List of queues in the system.

    def add_queue(self, cashier_speed=1):

        """
        Adds one queue to the list of queues

        :param cashier_speed:   float.  Determines the speed of the cashier in percent. (0.15 := 15%)
        """

        # Add the queue to the list of queues.
        tmp_queue = Queue(cashier_speed)
        self.queues.append(tmp_queue)


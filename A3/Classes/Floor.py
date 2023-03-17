

class Floor():
    def __init__(self, probs, arrive_rate):
        """
        Class that represents a floor.

        :param probs: list of probabilities for the destination of new people.
        :param arrive_rate: the arrival rate in people per minute for the poisson process
        """

        self.probs = probs
        self.arrive_rate = arrive_rate


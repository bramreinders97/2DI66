import numpy as np


class SimulateResults:

    MAX_PEOPLE_IN_CANTEEN = 10000

    def __init__(self):
        self.sumS = 0  # for summing Sojourn times
        self.sumS2 = 0  # for variance sojourn times
        self.sumQTime = 0  # for summing total queueing time
        self.sumQTime2 = 0  # for summing total queueing time variance
        self.nPeopleHistogram = np.zeros(
        self.MAX_PEOPLE_IN_CANTEEN + 1)  # for the histogram of #people in canteen

        # for the sojourn times of groups of people.
        self.SojournGroups = np.deque()
        # each time a customer belonging to group i
        # departs the canteen, set self.SojournGroup[i]
        # to the sojourn time of that customer. This is
        # all we'll need to do (i think) because the
        # sojourn time of the entire group is decided
        # by the slowest member

        # for extension 1:
        self.QTimeSlow = 0  # waiting time slow cahsier
        self.QTimeSlow2 = 0  # variance waiting time slow cahsier
        self.QTimeFast = 0  # waiting time Fast cahsier
        self.QTimeFast2 = 0  # variance waiting time Fast cahsier

    def registerSojournTime(self, S):
        # register a specicif sojourn time
        pass

    def registerQueueingTime(self, QTime):
        # register a customers waiting time in a queue
        pass

    def registerNPeopleHist(self, n_people, t):
        # in the hist register that n_people were in in the canteen for t time
        pass

    # Will probably need more functions for the calculation of statistics and stuff

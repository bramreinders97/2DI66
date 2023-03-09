import numpy as np
from collections import deque
import matplotlib.pyplot as plt


class SimulateResults:

    MAX_PEOPLE_IN_CANTEEN = 10000

    def __init__(self, ext_1):
        self.ext_1 = ext_1  # Is aextension 1 activated?

        self.sumS = 0  # for summing Sojourn times
        self.sumS2 = 0  # for variance sojourn times
        self.sumQTime = 0  # for summing total queueing time
        self.sumQTime2 = 0  # for summing total queueing time variance
        self.nPeopleHistogram = np.zeros(
            self.MAX_PEOPLE_IN_CANTEEN + 1)  # for the histogram of #people in canteen

        # for the sojourn times of groups of people.
        self.SojournGroups = deque()
        # each time a customer belonging to group i
        # departs the canteen, set self.SojournGroup[i]
        # to the sojourn time of that customer. This is
        # all we'll need to do (i think) because the
        # sojourn time of the entire group is decided
        # by the slowest member

        # for extension 1:
        self.QTimeSlow = 0  # waiting time slow cahsier
        self.QTimeSlow2 = 0  # variance waiting time slow cahsier
        self.n_people_fast = 0
        self.n_people_slow = 0

    def registerDeparture(self, customer, slow_cashier=False):
        """
        Register all relevant information corresponding to the departure of a customer

        :param customer: Customer. Customer object of the customer leaving the canteen
        """
        # Calculate relevant times this customer
        sojourn_time = customer.departure_time - customer.arrival_time
        queue_time = customer.departure_time - customer.enter_queue_time

        # Update statistics
        self.sumS += sojourn_time
        self.sumS2 += sojourn_time**2
        self.SojournGroups[customer.group_index] = sojourn_time

        if slow_cashier:
            self.QTimeSlow += queue_time
            self.QTimeSlow2 += queue_time**2
            self.n_people_slow += 1
        else:
            self.sumQTime += queue_time
            self.sumQTime2 += queue_time**2
            self.n_people_fast += 1

    def registerNPeopleCanteen(self, time, n_people):
        """
        Update the histogram keeping track of the number of people present in the canteen 

        :param time: float. The amount of time we saw n_people in the canteen
        :param n_people: int. The number of people we saw in the canteen for time time
        """
        self.nPeopleHistogram[min(
            n_people, self.MAX_PEOPLE_IN_CANTEEN)] += time

        print(self.nPeopleHistogram[:6])

    def registerGroupArrival(self):
        # New group has arrived -> Append a new entry to the deque keeping track of sojourn time for groups
        self.SojournGroups.append(0)

    def getMeanSojournTime(self):
        # Return the Expected Sojourn time of a customer
        return self.sumS / (self.n_people_fast + self.n_people_slow)

    def getStDevSojournTime(self):
        # return the st deviation of the Sojourn time of a customer
        return np.sqrt(self.sumS2 / (self.n_people_fast + self.n_people_slow) - self.getMeanSojournTime()**2)

    def getMeanQueueTime(self):
        # Return the expected Queue time of a customer
        return self.sumQTime / self.n_people_fast

    def getStDevQueueTime(self):
        # Return the st devaiation of the Queue time of a customer
        return np.sqrt(self.sumQTime2 / self.n_people_fast - self.getMeanQueueTime()**2)

    def getMeanQueueTimeSlow(self):
        # Return the expected Queue time of a customer in the slow queue
        return self.QTimeSlow / self.n_people_slow

    def getStDevQueueTimeSlow(self):
        # Return the st devaiation of the Queue time of a customer in the slow queue
        return np.sqrt(self.QTimeSlow2 / self.n_people_slow - self.getMeanQueueTimeSlow()**2)

    def getExpectedNPeopleInCanteen(self):
        # Return the expected number of people in the canteen
        return sum(self.nPeopleHistogram * np.arange(self.MAX_PEOPLE_IN_CANTEEN + 1)) / sum(self.nPeopleHistogram)

    def getStDevNPeopleInCanteen(self):
        # Return the st deviation of the number of people in the canteen:
        # st_dev = ( E[n_people^2] - E[n_people]^2 )^(1/2)
        variance = sum(self.nPeopleHistogram * np.arange(self.MAX_PEOPLE_IN_CANTEEN + 1)**2) / sum(self.nPeopleHistogram) \
            - self.getExpectedNPeopleInCanteen()**2
        return np.sqrt(variance)

    def getMeanSojournGroup(self):
        # Return the Expected Sojourn time of a group. This is decided by the groups slowest member
        return np.mean(self.SojournGroups)

    def getStDevSojournGroup(self):
        # Return th st deviation of the sojourn time of a group.
        return np.std(self.SojournGroups)

    def plotHist(self, maxPeople=50):
        """ 
        Plot the histogram showing the probability having k people in the canteen at once.

        :param maxPeople: int. The max number of people in the canteen we're interested in
        """
        maxx = maxPeople + 1
        n_people_to_plot = self.nPeopleHistogram[0: maxx]
        probabilities = n_people_to_plot / n_people_to_plot.sum(0)
        plt.figure()
        plt.title('N people in canteen')
        plt.bar(range(0, maxx), probabilities)
        plt.ylabel('P (N = k)')
        plt.xlabel('k')
        plt.show()

    def __str__(self):
        if self.ext_1:
            return f"""
            Mean Queue time Fast = {self.getMeanQueueTime()}
            StDev Queue time Fast = {self.getStDevQueueTime()}

            Mean Queue time Slow = {self.getMeanQueueTimeSlow()}
            StDev Queue time Slow = {self.getStDevQueueTimeSlow()}
            """
        else:
            return f"""
            Q1: 
            Mean Sojourn time = {self.getMeanSojournTime()}
            StDev Sojourn time = {self.getStDevSojournTime()}
            Mean Queue time = {self.getMeanQueueTime()}
            StDev Queue time = {self.getStDevQueueTime()}
            Mean #customers in canteen = {self.getExpectedNPeopleInCanteen()}
            StDev #customers in canteen = {self.getStDevNPeopleInCanteen()}

            {40 * '-'}

            Q2:
            Mean Sojourn time groups = {self.getMeanSojournGroup()}
            StDev Sojourn time groups = {self.getStDevSojournGroup()}

            {40 * '-'}

            Q3: run simulator.plotHist()
            Q4: TODO
            """

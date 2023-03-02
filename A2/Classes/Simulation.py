class Simulation:
    def __init__(self, arrivalDist, pickFoodDist, serveCustCardDist, serveCustCashDist, extension_1=False, extension_2=False, extension_3=False):
        self.arrivalDist = arrivalDist
        self.pickFoodDist = pickFoodDist
        self.serveCustCardDist = serveCustCardDist
        self.serveCustCashDist = serveCustCashDist
        self.extension_1 = extension_1
        self.extension_2 = extension_2
        self.extension_3 = extension_3

    def simulate(self):
        T = 3600  # one hour -> 3600 s
        q1 = 0  # length first queue
        q2 = 0  # length second queue
        q3 = 0  # length third queue
        t = 0  # time
        n_groups_arrived = 0  # number of groups that arrived

        # Add all logic corresponding to possible events

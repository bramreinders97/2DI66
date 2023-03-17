

class Elevator:

    capacity = 10

    def __init__(self):
        """
        Class that represents an elevator. Has a current floor, open-close state, direction (up or down) and list of people inside it.
        """

        self.floor = 0
        self.open = True
        self.going_up = True
        self.people = []

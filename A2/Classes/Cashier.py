class Cashier:

    def __init__(self, slow=False):
        self.working_rate = 1.25 if slow else 1  # Useful for answering extension 1

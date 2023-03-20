

class Event:

    NEW_QUEUER = 0
    ELEVATOR_ARRIVES = 1
    ENTER_ELEVATOR = 2
    LEAVE_ELEVATOR = 3

    def __init__(self, event_type, t, elevator = None, floor = None, destination_floor = None):
        """
        Class that represents an event and handles the different types of events

        :param event_type:  int.    The type of the event.
        :param t:           float.  The time of the event
        """

        self.event_type = event_type
        self.t = t
        self.elevator = elevator
        self.floor = floor
        self.destination_floor = destination_floor

    def handle_event(self):
        """
        Calls functions in respective classes to handle each type of event
        :return:
        """

        if self.event_type == 0: #NEW_QUEUER
            temp_event = self.floor.new_queuer(self.t)
        elif self.event_type == 1: #ELEVATOR_ARRIVES
            temp_event = self.elevator.reach_floor(self.t, self.floor, self.destination_floor)
        elif self.event_type == 2: #ENTER_ELEVATOR
            self.elevator.add_person(self.floor)
            temp_event = self.elevator.schedule_next_event(self.t, self.floor)
        elif self.event_type == 3: #LEAVE_ELEVATOR:
            self.elevator.remove_person()
            temp_event = self.elevator.schedule_next_event(self.t, self.floor)
        else:
            raise ValueError(f"ERROR: in event handler: unknown event type {self.event_type}")

        return temp_event

    def __str__(self):
        string = f"type: {self.event_type}, time: {self.t:.2f}"
        if self.elevator:
            string += f", elevator: {self.elevator.id_nr}"
        if self.floor:
            string += f", floor: {self.floor.floor_nr}"
        if self.destination_floor:
            string += f", destination floor: {self.destination_floor}"

        return string







class Event:

    #helps remember which code is what, not used in code
    NEW_QUEUER = 0
    ELEVATOR_ARRIVES = 1
    ENTER_ELEVATOR = 2
    LEAVE_ELEVATOR = 3

    def __init__(self, event_type, t, elevator = None, floor = None, destination_floor = None):
        """
        Class that represents an event and handles the different types of events

        :param event_type:  int.    The type of the event.
        :param t:           float.  The time of the event
        :param elevator:    Elevator.   The elevator involved in the event, if any
        :param floor:       Floor.      The floor involved in the event, if any
        :param destination_floor    int.    The number for the destination of a moving elevator
        """

        self.event_type = event_type
        self.t = t
        self.elevator = elevator
        self.floor = floor
        self.destination_floor = destination_floor

    def handle_event(self, extension_6):
        """
        Calls functions in respective classes to handle each type of event

        :param extension_6: boolean whether extension_6 is activated
        :return: tuple of a new event to add to the stack and additional data to use in results.
        """

        additional_data = False

        if self.event_type == 0:  # NEW_QUEUER
            temp_event = self.floor.new_queuer(self.t, extension_6)
        elif self.event_type == 1:  # ELEVATOR_ARRIVES
            additional_data = len(self.elevator.people)
            temp_event = self.elevator.reach_floor(self.t, self.floor, self.destination_floor)
        elif self.event_type == 2:  # ENTER_ELEVATOR
            additional_data = self.elevator.add_person(self.floor, self.t, extension_6)
            temp_event = self.elevator.schedule_next_event(self.t, self.floor)
        elif self.event_type == 3:  # LEAVE_ELEVATOR:
            additional_data = self.elevator.remove_person(self.t)
            temp_event = self.elevator.schedule_next_event(self.t, self.floor)
        else:
            raise ValueError(f"ERROR: in event handler: unknown event type {self.event_type}")

        return temp_event, additional_data

    def __str__(self):
        string = f"type: {self.event_type}, time: {self.t:.2f}"
        if self.elevator:
            string += f", elevator: {self.elevator.id_nr}"
        if self.floor:
            string += f", floor: {self.floor.floor_nr}"
        if self.destination_floor:
            string += f", destination floor: {self.destination_floor}"

        return string





from A3.Classes.Floor import Floor
from A3.Classes.Event import Event
import numpy as np

class Elevator:

    capacity = 10

    def __init__(self, id):
        """
        Class that represents an elevator. Has a current floor, open-close state, direction (up or down) and list of people inside it.
        """

        self.id_nr = id
        self.floor = 0
        self.open = True
        self.going_up = True
        self.people = []

    def add_person(self, floor):
        """
        Have a person enter the elevator, if possible
        :return:
        """
        if self.going_up:
            if floor.up_queue:
                self.people.append(floor.up_queue.pop())
        else:
            if floor.down_queue:
                self.people.append(floor.down_queue.pop())

    def remove_person(self):
        """
        Remove a person with this floor as destination from the elevator.
        :return:
        """
        for i in range(len(self.people)):
            if self.people[i].destination == self.floor:
                self.people.pop(i)
                break


    def reach_floor(self, t, current_floor : Floor, destination_floor):
        """
        Event for reaching a certain floor.
        Schedule another event, but accounting for opening or not closing the doors
        Change elevator direction as necesary

        :return:
        """
        self.floor = destination_floor

        # change elevator direction
        if self.floor == 4:
            self.going_up = False
        if self.floor == 0:
            self.going_up = True
        #schedule next event with time adjustment
        next_event = self.schedule_next_event(t, current_floor)
        if next_event.event_type == 1:
            next_event.t = t+6
        else:
            next_event.t += np.random.exponential(3)
        return next_event

    def schedule_next_event(self, t, current_floor : Floor):
        """
        Creates next event concerning this elevator, with priorities:
        First someone leaving at the current floor
        Then someone entering at the current floor
        Finally going to a different floor

        :param current_floor: Floor. The current floor the elevator is on
        :return: Event.
        """

        #check for leavers
        for i in self.people:
            if i.destination == self.floor:
                #schedule leave event
                return Event(3, t+1, self, current_floor)

        #check for enterers:
        if self.going_up:
            if current_floor.up_queue:
                return Event(2, t+1, self, current_floor)


        # move floor up or down:
        if self.going_up:
            new_floor = self.floor+1
        else:
            new_floor = self.floor-1

        #new time: +6s + closing doors exponential mean 3
        new_time = t + 6 +  np.random.exponential(3)
        return Event(1, new_time, self, None, new_floor)


from A2.Classes.Event import Event
from A2.Classes.Queues import Queues
from A2.Classes.SimResults import SimulateResults
from A2.Classes.SimResults import SimulateResults
import heapq


class Simulation:

    def __init__(self, queue_speeds=[1, 1, 1], mobile_store=0, card_only=False, lam=1/60):
        """
        Class that does one singe simulation.

        :param queue_speeds:   array.   Determines how many queses there are (length of the array)
                                        1 => Cashier works at 100% speed. Set one value to 1.25 for extension 1
                                        and how fast they are (values of the array entries)
        :param queue_speeds:   array.   Determines how many queses there are (length of the array)
                                        1 => Cashier works at 100% speed. Set one value to 1.25 for extension 1
                                        and how fast they are (values of the array entries)
        :param mobile_store:   float.   Determines whether there is a mobile store and how many groups are using it.
                                        0.15 => 15% of the Groups go to the mobile store. Value must be between 0 and 1.
        :param card_only:      bool.    Determines whether only payment by card is accepted.
        :param lam:            float.   The mean number of groups that will arrive in an average *second*. Lambda for minute/60

        """

        self.T = 3600           # End time: one hour -> 3600 s
        self.t = 0              # starting time

        # Determines how many queses there are and how fast they are
        self.queue_speeds = queue_speeds
        # Determines whether there is a mobile store and how many groups are using it.
        self.mobile_store = mobile_store
        # Determines whether only payment by card is accepted.
        self.card_only = card_only
        # Determines how fast new groups arrive: the mean number of groups in a minute
        self.lam = lam

        self.event_list = []    # Event list

        self.next_group_id = 0  # A counter to track the next group ID

        # Keep track of the number of customers in the canteen at all times
        self.n_people_in_canteen = 0
        # Keep track of the number of customers in the canteen at all times
        self.n_people_in_canteen = 0

    def simulate(self):
        """
        Carries out one single simulation.
        """
        # Create object to keep track of results
        results = SimulateResults(ext_1=bool(sum(self.queue_speeds) > 3))
        # Create object to keep track of results
        results = SimulateResults(ext_1=bool(sum(self.queue_speeds) > 3))

        # Create Queues
        queues = Queues()
        for queue_speed in self.queue_speeds:
            queues.add_queue(queue_speed)

        # Push first event onto the event_list
        event = Event(0, self.t)
        heapq.heappush(self.event_list, (event.t, event))

        # Main loop
        # Note that we will not receive new customers after t=3600. This is done
        # by not scheduling new arrivals in event.handle_arrival_event() after this moment.
        # This choice is made such that we can let every customer who is still in the canteen
        # at t=3600 leave before calculating the results
        while self.event_list:
            # get next element from the event list
            event = heapq.heappop(self.event_list)[1]
            prev_time = self.t
            prev_time = self.t
            self.t = event.t

            print(f"New event at t = {self.t}. Event: {event}")

            if 0 == event.type:
                tmp_events, n_new_people = event.handle_arrival_event(
                    self.next_group_id, self.mobile_store, self.card_only, self.lam)
                self.next_group_id += 1
                self.schedule_events(tmp_events)

                # register a new group arrival in the results Class
                results.registerGroupArrival()

                # register the number of people that were in the canteen before this new arrival
                results.registerNPeopleCanteen(
                    self.t - prev_time, self.n_people_in_canteen)

                # update n people in canteen
                # -1 because there is one type 0 event which must be excluded.
                self.n_people_in_canteen += n_new_people

                # print("Extra people: ", n_new_people)

            elif 1 == event.type:
                tmp_events = event.handle_enter_queue_event(queues)
                self.schedule_events(tmp_events)

                # Event though the #customers does not change, update the hist because self.t will change
                results.registerNPeopleCanteen(
                    self.t - prev_time, self.n_people_in_canteen)

            elif 2 == event.type:

                # update queue
                updated_queue = event.handle_departure_event(
                    queues.queues[event.customer.queue])
                queues.queues[event.customer.queue] = updated_queue

                # update and save customer
                event.customer.departure_time = self.t

                slow_cashier = bool(
                    queues.queues[event.customer.queue].cashier_speed > 1)
                #print('slow: ', slow_cashier)

                # Register departure in Results Class
                results.registerDeparture(event.customer, slow_cashier)

                results.registerNPeopleCanteen(
                    self.t - prev_time, self.n_people_in_canteen)

                # update n people in canteen
                self.n_people_in_canteen -= 1

            else:
                print("ERROR: in simulate: unknown event type")
                break
        #print("last group:", self.next_group_id-1)
        # added to be able to check if group count makes sense
        results.group_count = self.next_group_id
        return results

    def schedule_events(self, events):
        """
        Schedules all events. The events to be scheduled are given in the argument and are pushed into the event list.

        :param events:  array.  An array of events.
        """

        for event in events:
            heapq.heappush(self.event_list, (event.t, event))

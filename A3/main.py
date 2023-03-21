from A3.Classes.Simulation import Simulation


simulation = Simulation(10000, 1)

results = simulation.simulate()

#print(len(results.list_of_persons))
#print(results.people_in_elevator[0]/results.people_in_elevator[1])
sum = 0
for person in results.list_of_persons:
    sum += person.could_not_enter_count

print(sum)

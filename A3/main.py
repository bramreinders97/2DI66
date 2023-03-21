from A3.Classes.Simulation import Simulation


simulation = Simulation(10000, 1)

results = simulation.simulate()

print(len(results.list_of_persons))
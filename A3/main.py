from A3.Classes.Simulation import Simulation


simulation = Simulation(10000, 1)

results = simulation.simulate()

results.make_calculations()

print(results)

import numpy as np
from Classes.Simulation import Simulation
from collections import deque

simulator = Simulation(queue_speeds=[1, 1, 1])

results = simulator.simulate()

print(results)
print(f"{simulator.n_people_in_canteen} people in canteen")

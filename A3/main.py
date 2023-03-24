from A3.Classes.Simulation import Simulation
from A3.Classes.Answer import Answer


#answer = Answer()

#answer.question_6()

simulation = Simulation(10000, 1)
results = simulation.simulate(True)
results.make_calculations()
print(results)

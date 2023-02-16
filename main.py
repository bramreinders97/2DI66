from Classes.Simulator import Simulator
import time

n_simulations = 100000

################ Test Q1 ################

t1 = time.time()
sim = Simulator()
sim.question_1_4(n_simulations)
t2 = time.time()

print(f"Took {t2 - t1} seconds")

################ Test Q4 ################

t1 = time.time()
sim = Simulator(q4=True)
sim.question_1_4(n_simulations)
t2 = time.time()

print(f"Took {t2 - t1} seconds")

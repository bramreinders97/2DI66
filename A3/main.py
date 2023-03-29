from A3.Classes.Answer import Answer
from time import time

ans = Answer()

#ans.warm_up_cut_off(n_elevators=8, T=60*60*8, n_runs=10000, modulo_for_printing=8)

#ans.question_6(3)


start_time = time()

# ans.warm_up_cut_off(n_elevators=8, T=60*60*8,
#                     n_runs=10000, modulo_for_printing=8)
ans.question_2(10,40000)

print(time()-start_time)

#
# import numpy as np
# arrive_rate = 8.8/60
# t = 0
# runs = 1000
# for i in range(runs):
#     t += np.random.exponential(1/arrive_rate)
#
# #expected time: nr of customers generated/arrive rate
# et = runs/arrive_rate
#
# print(t, et)

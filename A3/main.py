from A3.Classes.Answer import Answer
from time import time

ans = Answer()

start_time = time()

# ans.warm_up_cut_off(n_elevators=8, T=60*60*8,
#                     n_runs=10000, modulo_for_printing=8)
ans.question_4(10,40000)

print(time()-start_time)

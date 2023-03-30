from A3.Classes.Answer import Answer
from time import time

ans = Answer()

ans.warm_up_cut_off(n_elevators=4, T=60*60*8,
                    n_runs=20000, modulo_for_printing=8)

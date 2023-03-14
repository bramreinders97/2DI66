import numpy as np
from A2.Classes.Answers import Answers
from A2.Classes.Simulation import Simulation

lam = 4
n_runs = 2000


mean_sojourns = np.zeros(n_runs)
st_devs_sojourns = np.zeros(n_runs)

for i in range(n_runs):
    print('run ', i+1, ' of ', n_runs)

    simulator = Simulation(queue_speeds=[1, 1, 1], lam=lam / 60)
    results = simulator.simulate()

    extra = results.getExtraInfoQ2()
    mean_sojourns[i] = extra['mean']
    st_devs_sojourns[i] = extra['stDev']

str_print = f"""
\u03BB = {lam}
Mean sojourn time groups = {np.mean(mean_sojourns)}
St devs inside groups = {np.mean(st_devs_sojourns)}

"""

print(str_print)

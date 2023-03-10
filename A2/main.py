import numpy as np
from Classes.Simulation import Simulation
from collections import deque
import math
from time import time

# simulator = Simulation(queue_speeds=[1, 1, 1])
#
# results = simulator.simulate()
#
# print(results)
# print(f"{simulator.n_people_in_canteen} people in canteen")


#code to do 100 simulation runs, get values from each run, and return those values and their sds
#init empty result lists

def sd(my_list, mean):
    return math.sqrt(sum([(i - mean) ** 2 for i in my_list])/len(my_list))

start = time()
for lam in range(1,5):
    EW_list = []
    ES_list = []
    EN_list = []
    ESg_list = []
    group_count_list = []
    EW_sd_list = []
    ES_sd_list = []
    EN_sd_list = []
    ESg_sd_list = []

    for i in range(100):
        #create and run simulation
        simulator = Simulation(queue_speeds=[1, 1, 1], lam = lam/60)
        results = simulator.simulate()
        #add desired values to all summary lists
        #E[W] waiting time (over all cashiers): getMeanQueueTime()
        EW_list.append(results.getMeanQueueTime())
        EW_sd_list.append(results.getStDevQueueTime())
        #E[S]: getMeanSojournTime()
        ES_list.append(results.getMeanSojournTime())
        ES_sd_list.append(results.getStDevSojournTime())
        #E[n people inside]: getExpectedNPeopleInCanteen()
        EN_list.append(results.getExpectedNPeopleInCanteen())
        EN_sd_list.append(results.getStDevNPeopleInCanteen())
        #E[S_g]: getMeanSojournGroup()
        ESg_list.append(results.getMeanSojournGroup())
        ESg_sd_list.append(results.getStDevSojournGroup())
        #nr of groups in total
        group_count_list.append(results.group_count)


    #calculate standard deviations and means of the lists
    EW_mean = sum(EW_list)/len(EW_list)
    ES_mean = sum(ES_list) / len(ES_list)
    EN_mean = sum(EN_list) / len(EN_list)
    ESg_mean = sum(ESg_list) / len(ESg_list)
    groups_mean = sum(group_count_list)/len(group_count_list)
    #mean of individual run standard deviations
    EW_sd_mean = sum(EW_sd_list)/len(EW_sd_list)
    ES_sd_mean = sum(ES_sd_list) / len(ES_sd_list)
    EN_sd_mean = sum(EN_sd_list) / len(EN_sd_list)
    ESg_sd_mean = sum(ESg_sd_list) / len(ESg_sd_list)

    EW_sd = sd(EW_list, EW_mean)
    ES_sd = sd(ES_list, ES_mean)
    EN_sd = sd(EN_list, EN_mean)
    ESg_sd = sd(ESg_list, ESg_mean)
    groups_sd = sd(group_count_list, groups_mean)

    print(f"""
    
    lambda = {lam}
    Average nr of groups per simulation: {groups_mean:.2f} (sd: {groups_sd:.2f})
    E [Waiting]: {EW_mean:.2f}, sd[E[Waiting]] {EW_sd:.2f}, E[sd[Waiting]] {EW_sd_mean:.2f}
    E Sojourn: {ES_mean:.2f}, sd[E] {ES_sd:.2f}, E[sd[Sojourn] {ES_sd_mean:.2f}
    E Nr of people: {EN_mean:.2f}, sd[E] {EN_sd:.2f}, E[sd[nr]] {EN_sd_mean:.2f}
    E Sojourn groups: {ESg_mean:.2f}, sd[E] {ESg_sd:.2f}, E[sd[S group]] {ESg_sd_mean:.2f}
    runtime: {time()-start:.2f}
    
    
            """)




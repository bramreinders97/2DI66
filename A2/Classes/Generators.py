import numpy as np





#geometric distribution:
def geo_distr(mean):
    return np.random.geometric(1/mean)

#poisson process generator: time between events is an exponential distribution
#exponential distribution:
def expo_distr(lam):
    return np.random.exponential(1/lam)

def next_group_arriving(lam):
    """
    Returns time until the next group arrives at a group arriving event
    :return: float
    """
    return np.random.exponential(1/lam) #maybe this needs to be simply lam? not sure

def time_for_getting_food(n):
    """
    n times for a group of n people to get food
    :param n: int
    :return: array[float]
    """
    return np.random.exponential(1 / 80, size=n)

#cash: np.random.exponential(1/20)
#card: np.random.exponential(1/12)

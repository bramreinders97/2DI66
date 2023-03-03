import numpy as np





#geometric distribution:
def geo_distr(mean):
    return np.random.geometric(1/mean)

#poisson process generator: time between events is an exponential distribution
#exponential distribution:
def expo_distr(lam):
    return np.random.exponential(1/lam)
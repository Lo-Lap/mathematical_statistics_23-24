import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np


# Poisson distribution
n = 1000
poisson_dist = sps.poisson.rvs(mu=10, size=n)
# matplotlib histogram
x = np.arange(min(min(poisson_dist)-1, 0), max(poisson_dist) + 1, 1)

plt.figure(figsize=(13, 7))
plt.plot(x, sps.poisson.pmf(x, mu=10), color='red', label='Плотность случайной величины')

plt.hist(poisson_dist, color='blue', edgecolor='black', bins=21, density=True, label='Гистограмма выборки')
# n=10 => bins=9
# n=50 => bins=18
# n=1000 => bins=21
# Add labels
plt.title(f'Histogram of Poisson Distribution n={n}')
plt.legend(fontsize=10, loc=1)
plt.xlabel('poissonNumbers')
plt.ylabel('Density')
plt.show()



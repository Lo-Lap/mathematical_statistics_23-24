import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np
import math


# normal distribution
n = 1000
normal_dist = sps.norm.rvs(size=n)
# matplotlib histogram
mu = 0
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(min(normal_dist) - 0.5, max(normal_dist) + 0.5, 100)

plt.figure(figsize=(13, 7))
plt.plot(x, sps.norm.pdf(x, mu, sigma), color='red', label='Плотность случайной величины')

plt.hist(normal_dist, color='blue', edgecolor='black', bins=30, density=True, label='Гистограмма выборки')
# n=10 => bins=8
# n=50 => bins=20
# n=1000 => bins=30

# Add labels
plt.title(f'Histogram of Normal distribution n={n}')
plt.legend(fontsize=10, loc=1)
plt.xlabel('normalNumbers')
plt.ylabel('Density')
plt.show()


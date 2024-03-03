import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np


# Cauchy distribution
n = 1000
cauchy_dist = sps.cauchy.rvs(loc=0, scale=1, size=n)
# matplotlib histogram
x = np.linspace(min(cauchy_dist) - 0.5, max(cauchy_dist) + 0.5, 100)

plt.figure(figsize=(13, 7))
# for n = 1000:
plt.yscale("log")
plt.plot(x, sps.cauchy.pdf(x, loc=0, scale=1), color='red', label='Плотность случайной величины')

plt.hist(cauchy_dist, color='blue', edgecolor='black', bins=100, density=True, label='Гистограмма выборки')

# n=10 => bins=7
# n=50 => bins=27
# n=1000 => bins=100
# n=1000 =>
# Add labels
plt.title(f'Histogram of Cauchy Distribution n={n}')
plt.legend(fontsize=10, loc=1)
plt.xlabel('cauchyNumbers')
plt.ylabel('Density')
plt.show()

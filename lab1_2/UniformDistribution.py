import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np
import math

# Uniform distribution
n = 1000
a = -math.sqrt(3)
b = math.sqrt(3)

uniform_dist = sps.uniform.rvs(loc=a, scale=2*b, size=n)
# matplotlib histogram
x = np.linspace(a-2, b+2, 1000)

plt.figure(figsize=(13, 7))
plt.plot(x, sps.uniform.pdf(x, loc=a, scale=2*b), lw=2, color='red', label='Плотность случайной величины')

plt.hist(uniform_dist, color='blue', edgecolor='black', bins=24, density=True, label='Гистограмма выборки')
# n=10 => bins=10
# n=50 => bins=16
# n=1000 => bins=24
# Add labels
plt.title(f'Histogram of Uniform Distribution n={n}')
plt.legend(fontsize=10, loc=1)
plt.xlabel('uniformNumbers')
plt.ylabel('Density')
plt.show()

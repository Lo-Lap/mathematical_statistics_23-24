import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np

# Student distribution
n = 1000
student_dist = sps.t.rvs(df=3, size=n)
# matplotlib histogram
x = np.linspace(min(student_dist) - 0.5, max(student_dist) + 0.5, 100)

plt.figure(figsize=(13, 7))
plt.plot(x, sps.t.pdf(x, df=3), color='red', label='Плотность случайной величины')

plt.hist(student_dist, color='blue', edgecolor='black', bins=50, density=True, label='Гистограмма выборки')
# n=10 => bins=8
# n=50 => bins=30
# n=1000 => bins=50
# Add labels
plt.title(f'Histogram of Student Distribution n={n}')
plt.legend(fontsize=10, loc=1)
plt.xlabel('studentNumbers')
plt.ylabel('Density')
plt.show()


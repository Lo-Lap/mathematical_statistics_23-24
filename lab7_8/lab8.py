import math
import statistics as st
import scipy.stats as sps
import numpy as np
import matplotlib.pyplot as plt


class hypothesis_testing_F:
    def __init__(self, n):
        self.distribution = sps.norm.rvs(size=n)

    def hyp_test(self, m, n, alpha):
        state = np.random.get_state()

        x_sample = np.random.choice(self.distribution, size=m, replace=False)
        y_sample = np.random.choice(self.distribution, size=n, replace=False)
        plt.figure(figsize=(13, 7))
        plt.hist(self.distribution, label='Гистограмма генеральной совокупности N=100', alpha=0.4, color='green',
                 edgecolor='green')
        plt.hist(y_sample, label=f'Гистограмма выборки 2 n={n}', alpha=0.4, color='yellow', edgecolor='yellow')
        plt.hist(x_sample, label=f'Гистограмма выборки 1 m={m}', alpha=0.4, color='red', edgecolor='red')
        plt.legend()
        plt.xlabel('Нормально распределёные числа')
        plt.ylabel('Количество чисел содержащихся в бине')
        plt.show()

        np.random.set_state(state)

        avg_x = np.mean(x_sample)
        avg_y = np.mean(y_sample)

        x_sqr = [(x_sample[i] - avg_x)**2 for i in range(m)]
        y_sqr = [(y_sample[i] - avg_y)**2 for i in range(n)]

        s_x_sqr = sum(x_sqr) / (m - 1)
        print(s_x_sqr)
        s_y_sqr = sum(y_sqr) / (n - 1)
        print(s_y_sqr)

        if s_x_sqr > s_y_sqr:
            F_b = s_x_sqr / s_y_sqr
        else:
            F_b = s_y_sqr / s_x_sqr

        F_quant = sps.f(m-1, n-1).ppf(1 - alpha / 2)
        print("F_quant = ", F_quant)
        print("F_B = ", F_b)
        return F_quant > F_b


test_h = hypothesis_testing_F(100)
print("m=20, n=40")
print(test_h.hyp_test(20, 40, 0.05))
print()
print("m=20, n=100")
print(test_h.hyp_test(20, 100, 0.05))

import math
import statistics as st
import scipy.stats as sps
import numpy as np


class hypothesis_testing_chi:
    def __init__(self, n, distribution, param):
        self.n = n

        if distribution == "normal":
            self.distribution = sps.norm()
            self.sampling = sps.norm.rvs(size=n)

        if distribution == "student":
            self.distribution = sps.t(df=param["df"])
            self.sampling = sps.t.rvs(df=param["df"], size=n)

        if distribution == "uniform":
            self.distribution = sps.uniform(loc=param["loc"], scale=param["scale"])
            self.sampling = sps.uniform.rvs(loc=param["loc"], scale=param["scale"], size=n)

    def test_hyp(self, alpha):
        k = 1 + math.floor(3.3 * math.log10(self.n))
        print("k = ", k)

        a_min = self.sampling.min()
        a_max = self.sampling.max()
        a = np.linspace(a_min, a_max, k - 1)

        a_ = [a[i] for i in range(len(a))]
        a_.append(float('inf'))
        a_.insert(0, float('-inf'))

        i = 0
        k_ = k
        while i != len(a_) - 1:
            if i + 1 == len(a_) - 1:
                p_i = self.distribution.cdf(a_[-1]) - self.distribution.cdf(a_[-2])
                if self.n * p_i >= 5:
                    i += 1
                    break
                a_.remove(a_[-2])
                k_ -= 1
                continue
            p_i = self.distribution.cdf(a_[i + 1]) - self.distribution.cdf(a_[i])
            if self.n * p_i >= 5:
                i += 1
                continue
            a_.remove(a_[i + 1])
            k_ -= 1

        print(a_)
        print("new k = ", k_)
        p = []
        for i in range(k_):
            p_i = self.distribution.cdf(a_[i + 1]) - self.distribution.cdf(a_[i])
            p.append(p_i)
            print(p_i*self.n)
        print("sum p_i = ", sum(p))

        n_k = [0 for _ in range(k_)]
        for value in self.sampling:
            for i in range(k_):
                if a_[i] < value <= a_[i + 1]:
                    n_k[i] += 1
                    break

        print("sum n_k = ", sum(n_k))
        chi_B_list = [((n_k[i] - self.n * p[i]) ** 2) / (self.n * p[i]) for i in range(k_)]
        chi_B = sum(chi_B_list)
        chi_2_alp = round(sps.chi2.ppf(1 - alpha, k_ - 1), 2)
        print(chi_B)
        print(chi_2_alp)
        return chi_B < chi_2_alp


hyp_test = hypothesis_testing_chi(20, 'normal', '')
print('normal, n=20 ')
print(hyp_test.test_hyp(0.05))

hyp_test = hypothesis_testing_chi(100, 'normal', '')
print('normal, n=100 ')
print(hyp_test.test_hyp(0.05))
print()

param_student = {"df": 3}

hyp_test = hypothesis_testing_chi(20, 'student', param_student)
print('student, n=20 ')
print(hyp_test.test_hyp(0.05))

hyp_test = hypothesis_testing_chi(100, 'student', param_student)
print('student, n=100 ')
print(hyp_test.test_hyp(0.05))
print()

param_uniform = {"loc": -math.sqrt(3),
                 "scale": 2 * math.sqrt(3)}
hyp_test = hypothesis_testing_chi(20, 'uniform', param_uniform)
print('uniform, n=20 ')
print(hyp_test.test_hyp(0.05))

hyp_test = hypothesis_testing_chi(100, 'uniform', param_uniform)
print('uniform, n=100 ')
print(hyp_test.test_hyp(0.05))

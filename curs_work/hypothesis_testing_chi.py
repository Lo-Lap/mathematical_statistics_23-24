import copy
import math
import scipy.stats as sps
import numpy as np


class hypothesis_testing_chi:
    def __init__(self, sampling: list):
        self.n = len(sampling)
        self.distribution = sps.norm(loc=np.mean(sampling), scale=np.std(sampling))
        self.sampling = copy.deepcopy(sampling)

    def test_hyp(self, alpha, flag):
        k = 1 + math.floor(3.3 * math.log10(self.n))
        # print("k = ", k)

        a = np.linspace(min(self.sampling) + 0.5, max(self.sampling) - 0.5, k - 1)

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

        # print(a_)
        # print("new k = ", k_)
        p = []
        for i in range(k_):
            p_i = self.distribution.cdf(a_[i + 1]) - self.distribution.cdf(a_[i])
            p.append(p_i)
            # print(p_i*self.n)
        # print("p=  ", p)
        # print("sum p_i = ", sum(p))
        n_k = [0 for _ in range(k_)]
        for value in self.sampling:
            for i in range(k_):
                if a_[i] < value <= a_[i + 1]:
                    n_k[i] += 1
                    break
        # print("n_k = ", n_k)
        # print("sum n_k = ", sum(n_k))
        # print("n_i-np_i =  ", [n_k[i] - self.n * p[i] for i in range(k_)])
        # print("sum_n_i-np_i =  ", sum([n_k[i] - self.n * p[i] for i in range(k_)]))
        # print("(n_i-np_i)**2 =  ", [(n_k[i] - self.n * p[i])**2 for i in range(k_)])
        # print("sum_n_i-np_i**2 =  ", sum([(n_k[i] - self.n * p[i])**2 for i in range(k_)]))
        np_i = [round(p[i] * self.n, 2) for i in range(len(p))]
        n_k_np_i = [round(n_k[i] - self.n * p[i], 2) for i in range(k_)]
        sqr_n_k_np_i = [round((n_k[i] - self.n * p[i]) ** 2, 2) for i in range(k_)]
        chi_B_list = [round(((n_k[i] - self.n * p[i]) ** 2) / (self.n * p[i]), 2) for i in range(k_)]
        # print("(n_i-np_i)**2/np_i =  ", chi_B_list)
        chi_B = sum(chi_B_list)
        chi_2_alp = round(sps.chi2.ppf(1 - alpha, k_ - 1), 2)
        p = [round(p[i], 2) for i in range(len(p))]
        # print(chi_B)
        # print(chi_2_alp)
        if flag == 1:
            print(f"{1} & ($-\infty,{'%.2f' % a_[1]}$] &{p[0]} & {np_i[0]}&{n_k[0]}&{n_k_np_i[0]}"
                  f"&{sqr_n_k_np_i[0]}&{chi_B_list[0]}", end='\\\\ \\hline \n')
            for i in range(1, len(p) - 1):
                print(f"{i+1} & ({'%.2f' % a_[i]}, {'%.2f' % a_[i+1]}] & {p[i]}&{np_i[i]}&{n_k[i]}&{n_k_np_i[i]}"
                      f"&{sqr_n_k_np_i[i]}&{chi_B_list[i]}", end='\\\\ \\hline \n')
            print(f"{k_} & (${'%.2f' % a_[-2]},\infty$)&{p[-1]} & {np_i[-1]}&{n_k[-1]}&{n_k_np_i[-1]}"
                  f"&{sqr_n_k_np_i[-1]}&{chi_B_list[-1]}", end='\\\\ \\hline \n')
            print(f"\sum &-&{round(sum(p),2)} &{round(sum(np_i),2)}&{round(sum(n_k),2)}&{round(sum(n_k_np_i),2)}"
                  f"&{round(sum(sqr_n_k_np_i),2)}&{round(sum(chi_B_list), 2)}", end='\\\\ \\hline \n')
        result = chi_B < chi_2_alp

        return k, k_, chi_B, chi_2_alp, result


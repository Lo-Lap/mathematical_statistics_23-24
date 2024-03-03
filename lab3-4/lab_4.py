import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np
import math


class Confid_interval:
    def __init__(self, type_sample: str, n: int):
        """

        :param type_sample: тип распределения
        :param n: количество элементов выборки
        """
        match type_sample:
            case "Normal":
                self.sample = sps.norm.rvs(size=n)
            case "Random":
                self.sample = np.random.rand(n)

        self.type = type_sample

        self.n = n

        self.m = sum(self.sample) / self.n  # выборочное среднее

        sample_sqr = [(x - self.m) ** 2 for x in self.sample]

        s_2 = 1 / self.n * sum(sample_sqr)  # выборочная дисперсия
        self.s = math.sqrt(s_2)  # выборочное среднеквадратичное отклонение

        self.m_right = None
        self.m_left = None
        self.sigma_right = None
        self.sigma_left = None

    def confid_interval_m(self, alpha: float):
        """
        Доверительный интервал среднего выборочного для нормального распределения
        :param alpha: уровень значимости
        :return: доверительный интервал
        """
        _alpha = 1 - alpha / 2

        quant = 0
        k = 1
        # для нормального распределения
        match self.type:
            case "Normal":  # для нормального распределения
                quant = sps.t.ppf(_alpha, df=self.n - 1)  # квантиль распределения Стьюдента
                k = self.n - 1  # степень свободы
            case "Random":  # для произвольного распределения
                quant = sps.norm.ppf(_alpha)  # квантиль нормального распределения
                k = self.n  # степень свободы

        self.m_right = self.m + self.s * quant / math.sqrt(k)
        self.m_left = self.m - self.s * quant / math.sqrt(k)
        return [self.m_left, self.m_right]

    def confid_interval_sigma(self, alpha: float):
        """
        Доверительный интервал для среднего квадратичного интервала нормального распределения
        :param alpha: уровень значимости
        :return: доверительный интервал
        """

        if self.type == "Normal":
            chi_2_alpha2_df = sps.chi2.ppf(alpha / 2, self.n - 1)
            alpha1 = 1 - alpha / 2
            chi_2_alpha1_df = sps.chi2.ppf(alpha1, self.n - 1)
            self.sigma_left = self.s * math.sqrt(self.n - 1) / math.sqrt(chi_2_alpha1_df)
            self.sigma_right = self.s * math.sqrt(self.n - 1) / math.sqrt(chi_2_alpha2_df)
            return [self.sigma_left, self.sigma_right]

        u_alpha = sps.norm.ppf(1 - alpha / 2)
        sample_fourth = [(x - self.m) ** 4 for x in self.sample]
        m_4 = 1 / self.n * sum(sample_fourth)  # четвёртый выборочный центральный момент
        e = m_4 / (self.s ** 4) - 3  # эксцесс

        self.sigma_left = self.s * (1 - 0.5 * u_alpha * math.sqrt(e + 2) / math.sqrt(self.n))
        self.sigma_right = self.s * (1 + 0.5 * u_alpha * math.sqrt(e + 2) / math.sqrt(self.n))
        return [self.sigma_left, self.sigma_right]

    def print_hist(self):
        x = [self.m_left, self.m_left]
        if self.type == "Normal":
            y = [0.0, 0.8]
        else:
            y = [0.0, 2]
        plt.figure(figsize=(4, 7))
        plt.hist(self.sample, color='#FFEFDB', edgecolor='black', bins=10, density=True,
                 label=f'{self.type} hyst n={self.n}')
        plt.plot(x, y, color='#8A2BE2', label='mu_min, mu_max', marker=".", markersize=9)

        x = [self.m_right, self.m_right]
        plt.plot(x, y, color='#8A2BE2', marker=".", markersize=9)

        x = [self.m_left - self.sigma_right, self.m_left - self.sigma_right]
        plt.plot(x, y, color='blue', label='m_min - sigma_max, m_min + sigma_max', marker=".", markersize=9)

        x = [self.m_right + self.sigma_right, self.m_right + self.sigma_right]
        plt.plot(x, y, color='blue', marker=".", markersize=9)

        plt.legend(fontsize=10, loc=1)
        plt.show()


def print_sigma_interval(sigma20: list, sigma100: list, type_: str):
    y1 = [1.0, 1.0]
    y2 = [1.1, 1.1]
    plt.figure(figsize=(4, 7))
    plt.title(type_)
    plt.ylim(0.9, 1.4)
    plt.plot(sigma20, y1, color='#8A2BE2', label='sigma interval n=20', marker=".", markersize=9)
    plt.plot(sigma100, y2, color='blue', label='sigma interval n=100', marker=".", markersize=9)
    plt.legend(fontsize=10, loc=1)
    plt.show()


if __name__ == "__main__":
    list_n = [20, 100]
    sigma_normal = []
    sigma_random = []
    for n_ in list_n:
        norm_dist = Confid_interval("Normal", n=n_)
        print("Normal n=" + str(n_))
        print("m: ", end=" ")
        print(norm_dist.confid_interval_m(0.05))
        print("sigma: ", end=" ")
        sigma_ = norm_dist.confid_interval_sigma(0.05)
        print(sigma_)
        sigma_normal.append(sigma_)
        print()
        norm_dist.print_hist()

        random_dist = Confid_interval("Random", n=n_)
        print("Random n=" + str(n_))
        print("m: ", end=" ")
        print(random_dist.confid_interval_m(0.05))
        print("sigma: ", end=" ")
        sigma_ = random_dist.confid_interval_sigma(0.05)
        print(sigma_)
        sigma_random.append(sigma_)
        print()
        random_dist.print_hist()

    print_sigma_interval(sigma_normal[0], sigma_normal[1], "Normal")
    print_sigma_interval(sigma_random[0], sigma_random[1], "Random")



import math
import statistics as st
import scipy.stats as sps


class PositionCharacteristics:
    def __init__(self, n_: int, distribution: str, param: dict):
        self.n_ = n_
        self.distribution = distribution
        self.param = param

    def GenList(self) -> list:

        if self.distribution == "normal":
            return sps.norm.rvs(size=self.n_)

        if self.distribution == "cauchy":
            return sps.cauchy.rvs(loc=self.param["loc"], scale=self.param["scale"], size=self.n_)

        if self.distribution == "student":
            return sps.t.rvs(df=self.param["df"], size=self.n_)

        if self.distribution == "poisson":
            return sps.poisson.rvs(mu=self.param["mu"], size=self.n_)

        if self.distribution == "uniform":
            return sps.uniform.rvs(loc=self.param["loc"], scale=self.param["scale"], size=self.n_)

    def average_sample(self):

        sum_avg = 0
        sum_avg_sqr = 0
        for _ in range(1000):
            list_x = []
            list_x = self.GenList()
            avg = sum(list_x) / self.n_
            sum_avg += avg
            sum_avg_sqr += avg * avg

        m_x_ = sum_avg / 1000
        d_x_ = sum_avg_sqr / 1000 - m_x_ * m_x_
        print(f'среднее среднего выборочного = {m_x_}')
        print(f'квадрат среднего выборочного = {d_x_}\n')

    def mediana_(self):
        sum_med = 0
        sum_med_sqr = 0
        for _ in range(1000):
            list_x = []
            list_x = self.GenList()
            med = st.median(list_x)
            sum_med += med
            sum_med_sqr += med * med

        m_med = sum_med / 1000
        d_med = sum_med_sqr / 1000 - m_med * m_med
        print(f'среднее медианы = {m_med}')
        print(f'квадрат медианы = {d_med}\n')

    def hulf_sum_extreme_elem(self):
        sum_psum = 0
        sum_psum_sqr = 0

        for _ in range(1000):
            list_x = []
            list_x = self.GenList()
            list_x.sort()
            psum = (list_x[0] + list_x[-1]) / 2
            sum_psum += psum
            sum_psum_sqr += psum * psum

        m_psum = sum_psum / 1000
        d_psum = sum_psum_sqr / 1000 - m_psum * m_psum
        print(f'среднее полусуммы экстр = {m_psum}')
        print(f'квадрат полусуммы экстр = {d_psum}\n')

    def quartile(self, p: float, list_x: list):
        i, d = math.modf(self.n_ * p)
        if self.n_ * p == d:
            return list_x[int(self.n_ * p) - 1]
        return list_x[int(d)]

    def hulf_sum_quartile(self):
        sum_pqua = 0
        sum_pqua_sqr = 0
        for _ in range(1000):
            list_x = []
            list_x = self.GenList()
            list_x.sort()
            quart_1 = self.quartile(0.25, list_x)
            quart_3 = self.quartile(0.75, list_x)
            p_quart = (quart_1 + quart_3) / 2
            sum_pqua += p_quart
            sum_pqua_sqr += p_quart * p_quart

        m_pqua = sum_pqua / 1000
        d_pqua = sum_pqua_sqr / 1000 - m_pqua * m_pqua

        print(f'среднее полусуммы квартилей = {m_pqua}')
        print(f'квадрат полусуммы квартилей = {d_pqua}\n')

    def truncted_average(self):
        sum_trunc = 0
        sum_trunc_sqr = 0
        r = int(self.n_ / 4)
        for _ in range(1000):
            list_x = []
            list_x = self.GenList()
            list_x.sort()
            trunc = 1 / (self.n_ - 2 * r) * sum(list_x[int(self.n_ / 4):self.n_ - int(self.n_ / 4)])
            sum_trunc += trunc
            sum_trunc_sqr += trunc * trunc

        m_trunc = sum_trunc / 1000
        d_trunc = sum_trunc_sqr / 1000 - m_trunc * m_trunc

        print(f'среднее усечённого среднего = {m_trunc}')
        print(f'квадрат усечённого среднего = {d_trunc}\n')


if __name__ == "__main__":
    size_ = [10, 100, 1000]

    param_cauchy = {"loc": 0,
                    "scale": 1}

    param_student = {"df": 3}

    param_poisson = {"mu": 10}

    param_uniform = {"loc": -math.sqrt(3),
                     "scale": 2 * math.sqrt(3)}
    for n in size_:
        print(f"normal n={n}")
        norm_char = PositionCharacteristics(n, "normal", {})
        norm_char.average_sample()
        norm_char.mediana_()
        norm_char.hulf_sum_extreme_elem()
        norm_char.hulf_sum_quartile()
        norm_char.truncted_average()
        print()

        print(f"cauchy n={n}")
        cauchy_char = PositionCharacteristics(n, "cauchy", param_cauchy)
        cauchy_char.average_sample()
        cauchy_char.mediana_()
        cauchy_char.hulf_sum_extreme_elem()
        cauchy_char.hulf_sum_quartile()
        cauchy_char.truncted_average()
        print()

        print(f"student n={n}")
        student_char = PositionCharacteristics(n, "student", param_student)
        student_char.average_sample()
        student_char.mediana_()
        student_char.hulf_sum_extreme_elem()
        student_char.hulf_sum_quartile()
        student_char.truncted_average()
        print()

        print(f"poisson n={n}")
        poisson_char = PositionCharacteristics(n, "poisson", param_poisson)
        poisson_char.average_sample()
        poisson_char.mediana_()
        poisson_char.hulf_sum_extreme_elem()
        poisson_char.hulf_sum_quartile()
        poisson_char.truncted_average()
        print()

        print(f"uniform n={n}")
        uniform_char = PositionCharacteristics(n, "uniform", param_uniform)
        uniform_char.average_sample()
        uniform_char.mediana_()
        uniform_char.hulf_sum_extreme_elem()
        uniform_char.hulf_sum_quartile()
        uniform_char.truncted_average()
        print()

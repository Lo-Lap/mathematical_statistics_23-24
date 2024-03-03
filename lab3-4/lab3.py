import matplotlib.pyplot as plt
import scipy.stats as sps
import math


class Boxplot:
    def __init__(self, type_distribution: str, n: list, param: dict):
        self.type_distribution = type_distribution
        self.n = n
        self.param = param

    def Generate_sampling(self, n: int):
        match self.type_distribution:
            case "Normal":
                return sps.norm.rvs(size=n)
            case "Cauchy":
                return sps.cauchy.rvs(loc=self.param["loc"], scale=self.param["scale"], size=n)
            case "Poisson":
                return sps.poisson.rvs(mu=self.param["mu"], size=n)
            case "Student":
                return sps.t.rvs(df=self.param["df"], size=n)
            case "Uniform":
                return sps.uniform.rvs(loc=self.param["loc"], scale=self.param["scale"], size=n)

    def create_boxplot(self):
        data = []
        for n_ in self.n:
            data.append(self.Generate_sampling(n_))

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111)

        # Creating axes instance
        ax.boxplot(data, vert=False)
        ax.set_yticklabels(self.n)

        # Adding title
        plt.title(self.type_distribution + " distribution")

        # Removing top axes and right axes
        # ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.xlabel('x')
        plt.ylabel(self.type_distribution)
        # show plot
        plt.show()


if __name__ == "__main__":
    list_n = [20, 100]

    param_cauchy = {"loc": 0,
                    "scale": 1}

    param_student = {"df": 3}

    param_poisson = {"mu": 10}

    param_uniform = {"loc": -math.sqrt(3),
                     "scale": 2 * math.sqrt(3)}

    # normal distribution
    normal_dist = Boxplot("Normal", list_n, {})
    normal_dist.create_boxplot()

    # cauchy distribution
    cauchy_dist = Boxplot("Cauchy", list_n, param_cauchy)
    cauchy_dist.create_boxplot()

    # student distribution
    student_dist = Boxplot("Student", list_n, param_student)
    student_dist.create_boxplot()

    # poisson distribution
    poisson_dist = Boxplot("Poisson", list_n, param_poisson)
    poisson_dist.create_boxplot()

    # uniform distribution
    uniform_dist = Boxplot("Uniform", list_n, param_uniform)
    uniform_dist.create_boxplot()

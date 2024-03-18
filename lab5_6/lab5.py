import matplotlib.pyplot as plt
import scipy.stats as sps
from matplotlib.patches import Ellipse
import pandas as pn
import math
import numpy as np


def quadr(x, y):
    med_x = np.median(x)
    med_y = np.median(y)
    r_q_list = [np.sign(x[i] - med_x) * np.sign(y[i] - med_y) for i in range(len(x))]
    r_Q = np.average(r_q_list)
    return r_Q


def correlation_coefficients(rho, n, type):
    coef_pearson = []
    coef_spearmanr = []
    coef_quadrant = []
    coef_tau = []

    for _ in range(1000):
        if type == "mix":
            variables = 0.9 * np.random.multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]], size=n) + \
                        0.1 * np.random.multivariate_normal(mean=[0, 0], cov=[[100, -rho * 100], [-rho * 100, 100]],
                                                            size=n)
        else:
            variables = np.random.multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]], size=n)
        c_p = sps.pearsonr(variables[:, 0], variables[:, 1])
        coef_pearson.append(c_p.statistic)

        c_s = sps.spearmanr(variables[:, 0], variables[:, 1])
        coef_spearmanr.append(c_s.statistic)

        c_q = quadr(variables[:, 0], variables[:, 1])
        coef_quadrant.append(c_q)
        coef_tau.append(sps.kendalltau(variables[:, 0], variables[:, 1]).statistic)

    print("Коэффициент Пирсона")
    mean_coef_p = np.average(coef_pearson)
    coef_p_sqr = [c * c for c in coef_pearson]
    mean_sqr_c_p = np.average(coef_p_sqr)
    disper = np.var(coef_pearson)

    print("     среднее значение: ", mean_coef_p)
    print("     среднее значение квадрата: ", mean_sqr_c_p)
    print("     дисперсия: ", disper)

    print()
    print("Коэффициент Спирмена")

    mean_coef_s = np.average(coef_spearmanr)
    coef_s_sqr = [c * c for c in coef_spearmanr]
    mean_sqr_s_p = np.average(coef_s_sqr)
    disper = np.var(coef_spearmanr)

    print("     среднее значение: ", mean_coef_s)
    print("     среднее значение квадрата: ", mean_sqr_s_p)
    print("     дисперсия: ", disper)

    print()
    print("Квадрантный коэффициент")

    mean_coef_q = np.average(coef_quadrant)
    coef_q_sqr = [c * c for c in coef_quadrant]
    mean_sqr_q_p = np.average(coef_q_sqr)
    disper = np.var(coef_quadrant)

    print("     среднее значение: ", mean_coef_q)
    print("     среднее значение квадрата: ", mean_sqr_q_p)
    print("     дисперсия: ", disper)

    print("Кендалл")

    mean_coef_q = np.average(coef_tau)
    coef_q_sqr = [c * c for c in coef_tau]
    mean_sqr_q_p = np.average(coef_q_sqr)
    disper = np.var(coef_tau)

    print("     среднее значение: ", mean_coef_q)
    print("     среднее значение квадрата: ", mean_sqr_q_p)
    print("     дисперсия: ", disper)


def print_distribution(n_list: list, rho_list: list):
    variables = {}
    for n in n_list:
        list_var = []
        for rho in rho_list:
            dict_var = {rho: np.random.multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]], size=n)}
            list_var.append(dict_var)
        variables[n] = list_var

    for n in n_list:
        list_var = variables[n]

        fig = plt.figure(figsize=(13, 7))
        k = 1
        for rho in rho_list:
            ax = fig.add_subplot(1, 3, k)
            pts = list_var[k - 1][rho]

            cov = np.cov(pts[:, 0], pts[:, 1])
            lambda_, v = np.linalg.eig(cov)
            lambda_ = np.sqrt(lambda_)
            mean_x = np.mean(pts[:, 0])
            mean_y = np.mean(pts[:, 1])
            ax.add_artist(Ellipse(xy=(mean_x, mean_y),
                          width=lambda_[0] * 2 * 2, height=lambda_[1] * 2 * 2,
                          angle=np.rad2deg(np.arccos(v[0, 0])), facecolor='g', edgecolor='k', alpha=.1))

            plt.scatter(pts[:, 0], pts[:, 1], alpha=0.7)
            plt.title("size = {n}; p = {rho}".format(n=n, rho=rho))
            plt.axis('equal')
            k += 1

        plt.show()


n_list = [20, 60, 100]
rho_list = [0, 0.5, 0.9]
for n in n_list:
    for rho in rho_list:
        print()
        print("size = {n}; p = {rho}".format(n=n, rho=rho))
        correlation_coefficients(rho, n, "")
#print_distribution([20, 60, 100], [0, 0.5, 0.9])

print()
print("Mix distribution")
for n in n_list:
    print("size = {n}".format(n=n))
    correlation_coefficients(0.9, n, "mix")

k = 1
fig = plt.figure(figsize=(13, 7))
for n in n_list:
    pts = 0.9 * np.random.multivariate_normal(mean=[0, 0], cov=[[1, 0.9], [0.9, 1]], size=n) + \
          0.1 * np.random.multivariate_normal(mean=[0, 0], cov=[[100, -90], [-90, 100]], size=n)
    ax = fig.add_subplot(1, 3, k)
    cov = np.cov(pts[:, 0], pts[:, 1])
    lambda_, v = np.linalg.eig(cov)
    lambda_ = np.sqrt(lambda_)
    mean_x = np.mean(pts[:, 0])
    mean_y = np.mean(pts[:, 1])
    ax.add_artist(Ellipse(xy=(mean_x, mean_y),
                          width=lambda_[0] * 2 * 2, height=lambda_[1] * 2 * 2,
                          angle=np.rad2deg(np.arccos(v[0, 0])), facecolor='g', edgecolor='k', alpha=.1))
    plt.scatter(pts[:, 0], pts[:, 1], alpha=0.7)
    plt.title("size = {n}".format(n=n))
    plt.axis('equal')
    k += 1
plt.show()

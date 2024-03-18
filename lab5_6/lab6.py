import numpy as np
import scipy.stats as sps
import math

# МНК
def mnk(x: list, y: list):
    avg_x = np.average(x)
    avg_y = np.average(y)

    x_sqrt = [x[i] * x[i] for i in range(len(x))]
    xy = [x[i] * y[i] for i in range(len(x))]

    avg_x_sqrt = np.average(x_sqrt)
    avg_xy = np.average(xy)

    b_eval = (avg_xy - avg_x * avg_y) / (avg_x_sqrt - avg_x ** 2)
    a_eval = avg_y - avg_x * b_eval

    print("МНК")
    print("Оценка а= ", a_eval)
    print("Оценка-точное = ", abs(a_eval - 2))
    print("Оценка b= ", b_eval)
    print("Оценка-точное = ", abs(b_eval - 2))
    print()


# робастые оценки
def mnm(x: list, y: list):
    med_x = np.median(x)
    med_y = np.median(y)

    r_q_list = [np.sign(x[i] - med_x) * np.sign(y[i] - med_y) for i in range(len(x))]

    r_Q = np.average(r_q_list)

    n = len(x)
    i, d = math.modf(n / 4)
    if n / 4 == d:
        l = int(n / 4) - 1
    else:
        l = int(d)

    j = n - l - 1

    sort_x = np.sort(x)
    sort_y = np.sort(y)

    k_n = 1.491
    q_y = (sort_y[j] - sort_y[l])

    q_x = (sort_x[j] - sort_x[l])

    b_eval_R = r_Q * q_y / q_x

    a_eval_R = med_y - b_eval_R * med_x

    print("МНМ")
    print("Оценка а= ", a_eval_R)
    print("Оценка-точное = ", abs(a_eval_R - 2))
    print("Оценка b= ", b_eval_R)
    print("Оценка-точное = ", abs(b_eval_R - 2))
    print()


# Без возмущений
x = np.linspace(-1.8, 2, 20)
e = sps.norm.rvs(size=20)

y = [2 + 2 * x[i] + e[i] for i in range(len(x))]
print("Без возмущений: ")
mnk(list(x), y)
mnm(list(x), y)

y[0] = y[0] + 10
y[19] = y[19] - 10

print("С возмущениями: ")
mnk(list(x), y)
mnm(list(x), y)

import numpy as np
import scipy.stats as sps
import math
import matplotlib.pyplot as plt


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
    print("Оценка-точное = ", abs(a_eval - 2)/2*100)
    print("Оценка b= ", b_eval)
    print("Оценка-точное = ", abs(b_eval - 2)/2*100)
    print()
    return a_eval, b_eval


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
    print("Оценка-точное = ", abs(a_eval_R - 2)/2*100)
    print("Оценка b= ", b_eval_R)
    print("Оценка-точное = ", abs(b_eval_R - 2)/2*100)
    print()
    return a_eval_R, b_eval_R


def draw_graph(y, y_mnk, y_mnm, x, title):
    plt.figure(figsize=(13, 7))
    plt.scatter(x, y, color="red")
    plt.plot(x, y, color="red", label="Эталонная зависимость")
    plt.scatter(x, y_mnk, color="green")
    plt.plot(x, y_mnk, color="green", label="МНК")
    plt.scatter(x, y_mnm, color="blue")
    plt.plot(x, y_mnm, color="blue", label="МНМ")
    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


# Без возмущений
x = np.linspace(-1.8, 2, 20)
e = sps.norm.rvs(size=20)

y = [2 + 2 * x[i] + e[i] for i in range(len(x))]
print("Без возмущений: ")
# a, b = mnk(list(x), y)
a, b = 2.24, 1.87
# a_R, b_R = mnm(list(x), y)
a_R, b_R = 2.33, 1.87
y_ = [2 + 2 * x[i] + e[i] for i in range(len(x))]
y_mnk = [a + b * x[i] + e[i] for i in range(len(x))]
y_mnm = [a_R + b_R * x[i] + e[i] for i in range(len(x))]
draw_graph(y_, y_mnk, y_mnm, list(x), "Без возмущений")
y_ = [2 + 2 * x[i] for i in range(len(x))]
y_mnk = [a + b * x[i] for i in range(len(x))]
y_mnm = [a_R + b_R * x[i] for i in range(len(x))]
draw_graph(y_, y_mnk, y_mnm, list(x), "Без возмущений (без e_i)")
y[0] = y[0] + 10
y[19] = y[19] - 10

print("С возмущениями: ")
# a, b = mnk(list(x), y)
a, b = 2.38, 0.44
# a_R, b_R = mnm(list(x), y)
a_R, b_R = 2.38, 1.4
y_ = [2 + 2 * x[i] + e[i] for i in range(len(x))]
y_mnk = [a + b * x[i] + e[i] for i in range(len(x))]
y_mnm = [a_R + b_R * x[i] + e[i] for i in range(len(x))]
draw_graph(y_, y_mnk, y_mnm, list(x), "С возмущениями")
y_ = [2 + 2 * x[i] for i in range(len(x))]
y_mnk = [a + b * x[i] for i in range(len(x))]
y_mnm = [a_R + b_R * x[i] for i in range(len(x))]
draw_graph(y_, y_mnk, y_mnm, list(x), "С возмущениями (без e_i)")

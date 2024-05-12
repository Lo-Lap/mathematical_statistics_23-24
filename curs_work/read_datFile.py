import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from hypothesis_testing_chi import hypothesis_testing_chi
import scipy.stats as sps


def work_name_file(name: str):
    name = name.split("\\")[1]
    mass_name = name.split("V_sp")
    x = float(mass_name[0])
    sp = int(mass_name[1].split(".dat")[0])
    return x, sp


def read_all_file():
    df_dict = {}
    path = './rawData/'
    file = Path(path).glob('*V_sp*.dat')
    for name in file:
        x, sp = work_name_file(name.__str__())
        df_dict[x] = []

    file = Path(path).glob('*V_sp*.dat')
    for name in file:
        x, sp = work_name_file(name.__str__())
        df = pd.read_csv(name, sep=' ', header=None, names=['col1', 'col2', 'col3', 'col4', 'col5',
                                                            'col6', 'col7', 'col8', 'col9', 'col10', 'col11'])
        df_dict[x] = df_dict.get(x, []) + [[sp, df]]

    # print(df_dict)
    return df_dict


def for_zero(mas1, mas2, mas3, mas4, mas5):
    mas = np.add(np.add(np.add(np.add(mas1, mas2), mas3), mas4), mas5)

    avg_mas = np.divide(mas, [5])
    return avg_mas


def read_zero(df_dict):
    list_sp_df = df_dict[0.0]
    mass_list = []
    for sp, df in list_sp_df:
        mass = massiv_from_df(df, sp)
        mass_list.append(mass)

    avg_mass = for_zero(mass_list[0], mass_list[1], mass_list[2], mass_list[3], mass_list[4])
    return avg_mass


def massiv_from_df(df, num):
    list_mass = []
    for i in range(1, 9):
        mass = df.iloc[:, i].values.tolist()
        ind = 1024 - num + 1
        new_mass = mass[-ind:] + mass[:-ind]
        list_mass.append(new_mass)
    return list_mass


def chi_q(df_dict: dict, mas_zero: list):
    for x in df_dict.keys():
        list_sp_df = df_dict[x]
        print(f"x = {x}:")

        mas_k_all = []
        mas_new_k_all = []
        mas_chi_all = []
        mas_chi_table_all = []
        mas_result_all = []
        mas_sp = []
        for sp, df in list_sp_df:
            mas_sp.append(sp)
            mass_ = massiv_from_df(df, sp)
            mass = np.subtract(mass_, mas_zero)
            i = 1
            mas_k = []
            mas_new_k = []
            mas_chi = []
            mas_chi_table = []
            mas_result = []
            # print(f"sp = {sp}:")
            for column in mass:
                hyp_test = hypothesis_testing_chi(column)
                # print(f"series {i}:")
                k, k_, chi_B, chi_2_alp, result = hyp_test.test_hyp(0.05, 0)
                mas_k.append(k)
                mas_new_k.append(k_)
                mas_chi.append(round(chi_B, 2))
                mas_chi_table.append(chi_2_alp)
                mas_result.append(result)
                # print(mas_k)
                i += 1

            mas_k_all.append(mas_k)
            mas_new_k_all.append(mas_new_k)
            mas_chi_all.append(mas_chi)
            mas_chi_table_all.append(mas_chi_table)
            mas_result_all.append(mas_result)

        print("\n")
        print(*(mas_sp), sep=" & ")
        mas_k_all = np.transpose(mas_k_all)
        mas_new_k_all = np.transpose(mas_new_k_all)
        mas_chi_all = np.transpose(mas_chi_all)
        mas_chi_table_all = np.transpose(mas_chi_table_all)
        mas_result_all = np.transpose(mas_result_all)

        for ind in range(8):
            print("\multirow{5}{*}{$", f"{ind + 1}", "$}", end='')
            print("& $k_0$ &", end=' ')
            print(*(mas_k_all[ind]), sep=" & ", end='\\\\ \\cline{2-7} \n')
            # print("\n")
            print("& $k$ &", end=' ')
            print(*(mas_new_k_all[ind]), sep=" & ", end='\\\\ \\cline{2-7} \n')
            # print("\n")
            print("& $\chi^2_B$ &", end=' ')
            print(*mas_chi_all[ind], sep=" & ", end='\\\\ \\cline{2-7} \n')
            # print("\n")
            print("& $\chi_{1-\\alpha}^2(k-1)$ &", end=' ')
            print(*mas_chi_table_all[ind], sep=" & ", end='\\\\ \\cline{2-7} \n')
            # print("\n")
            print("&$\chi^2_B < \chi_{1-\\alpha}^2(k-1)$ &", end=' ')
            print(*mas_result_all[ind], sep=" & ", end='\\\\ \\hline \n')
            print("\n")
            print()


def test_table(df_dict, mas_zero):
    list_sp_df = df_dict[0.0]
    sp, df = list_sp_df[0]
    mass_ = massiv_from_df(df, sp)
    mass = np.subtract(mass_, mas_zero)

    hyp_test = hypothesis_testing_chi(mass[0])
    k, k_, chi_B, chi_2_alp, result = hyp_test.test_hyp(0.05, 1)
    plt.figure(figsize=(13, 7))
    column = mass[0]
    x = np.linspace(min(column) - 0.5, max(column) + 0.5, 100)
    plt.plot(x, sps.norm.pdf(x, loc=np.mean(column), scale=np.std(column)), color='red',
             label='Плотность случайной величины')
    plt.hist(column, color='blue', edgecolor='black', bins=30, density=True,
             label='Гистограмма выборки')
    plt.title(f'Histogram of series = {1}')
    plt.legend(fontsize=10, loc=1)
    plt.xlabel('Numbers')
    plt.ylabel('Density')
    plt.show()


df_dict = read_all_file()
zero = read_zero(df_dict)
# zero = [[0 for _ in range(1024)] for _ in range(8)]
chi_q(df_dict, zero)
test_table(df_dict, zero)


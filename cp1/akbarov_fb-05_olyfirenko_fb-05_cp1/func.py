import math
import pandas as pd
import numpy as np

#Функция calc_e рассчитывает энтропию по заданным значениям. Переменные переименованы в e_value и total_value
def сalc_e(e_value, total_value):
    return 1 - (e_value / math.log2(total_value))

#Функция entropiy рассчитывает энтропию по заданному словарю и количеству элементов. Переменные переименованы в dict_data и num_elem
def entropiy(dict_data, num_elem):
    entropies = []
    for k in dict_data.keys():
        if dict_data[k] != 0:
            entropies.append(abs(float(dict_data[k]) * math.log2(dict_data[k]) / num_elem))
    return sum(entropies)

#Функция freq_of_letters рассчитывает частоту букв в тексте по заданному алфавиту. Переменные переименованы в data_txt и alph
def freq_of_letters(data_txt,alph):
    dictionary = {}
    for l in alph:
        dictionary.update({l: 0})
    for i in data_txt:
        dictionary[i] += 1
    for l in alph:
        dictionary.update({l: round(dictionary[l] / len(data_txt), 5)})
    return dictionary

#Функция freq_of_bigrams рассчитывает частоту биграм в тексте по заданному алфавиту. Переменные переименованы в data_txt, alph и crs
def freq_of_bigrams(data_txt,alph, crs=True):
    dictionary = {}
    for l1 in alph:
        for l2 in alph:
            dictionary.update({l1 + l2: 0})

    if crs == True:
        for i in range(len(data_txt) - 1):
            dictionary[data_txt[i] + data_txt[i + 1]] += 1
        for key in dictionary.keys():
            dictionary[key] = round(dictionary[key] / (len(data_txt) - 1), 5)
    else:
        if len(data_txt) % 2 == 1:
            data_txt += "а"
        for i in range(len(data_txt) - 1):
            if i % 2 == 1:
                continue
            dictionary[data_txt[i] + data_txt[i + 1]] += 1
        for key in dictionary.keys():
            dictionary[key] = round(dictionary[key] / (len(data_txt) - 1), 5)
    return dictionary

#Функция save_results сохраняет результаты в файлы. Переменные переименованы в first_data, second_data, first_data_1,
#first_data_2, second_data_1, second_data_2
def save_results(first_data, second_data, first_data_1, first_data_2, second_data_1, second_data_2):
    pd.DataFrame(first_data.values(), index=first_data.keys()).to_excel('one.xlsx')
    time_verable = np.array(list(first_data_1.values()))
    pd.DataFrame(time_verable.reshape((34, 34)), index=first_data.keys(), columns=first_data.keys()).to_excel('two.xlsx')
    time_verable = np.array(list(first_data_2.values()))
    pd.DataFrame(time_verable.reshape((34, 34)), index=first_data.keys(), columns=first_data.keys()).to_excel('three.xlsx')
    pd.DataFrame(second_data.values(), index=second_data.keys()).to_excel('4.xlsx')
    vva = np.array(list(second_data_1.values()))
    pd.DataFrame(vva.reshape((33, 33)), index=second_data.keys(), columns=second_data.keys()).to_excel('fifth.xlsx')
    time_verable, a22 = np.array(list(second_data_2.values())), pd.DataFrame(vva.reshape((33, 33)), index=second_data.keys(),
                                                                   columns=second_data.keys())
    a22.to_excel('six.xlsx')
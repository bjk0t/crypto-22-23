import math
import pandas as pd
import numpy as np
import re
class Textes:
    def __init__(self, name_file, alfavit):
        self.name_file = name_file
        self.alfavit = alfavit
        self.text = self.get_text()
    def get_text(self):
        file = open(self.name_file, encoding='utf8')
        text = file.read().lower().replace('\n', '')
        text = re.sub(r'[^а-яё ]', '', text).replace(' ', '')
        file.close()
        return text
    def get_freq_of_letters(self):
        dictionary = {}
        for l in self.alfavit:
            dictionary.update({l: 0})
        for i in self.text:
            dictionary[i] += 1
        for l in self.alfavit:
            dictionary.update({l: round(dictionary[l] / len(self.text), 5)})
        return dictionary
    def get_entropiy(self, dictionary):
        entropies = []
        for k in dictionary.keys():
            if dictionary[k] != 0:
                entropies.append(abs(float(dictionary[k]) * math.log2(dictionary[k]) / len(self.alfavit)))
        return sum(entropies)
    def get_calc_e(self,e_value, total_value):
        return 1 - (e_value / math.log2(total_value))
    def get_freq_of_bigrams(self,alfavit, crs=True):
        dictionary = {}
        for l1 in alfavit:
            for l2 in alfavit:
                dictionary.update({l1 + l2: 0})
        if crs == True:
            for i in range(len(self.text) - 1):
                dictionary[self.text[i] + self.text[i + 1]] += 1
            for key in dictionary.keys():
                dictionary[key] = round(dictionary[key] / (len(self.text) - 1), 5)
        else:
            if len(self.text) % 2 == 1:
                self.text += "а"
            for i in range(len(self.text) - 1):
                if i % 2 == 1:
                    continue
                dictionary[self.text[i] + self.text[i + 1]] += 1
            for key in dictionary.keys():
                dictionary[key] = round(dictionary[key] / (len(self.text) - 1), 5)
        return dictionary
    def save_results(self, first_data, second_data, first_data_1, first_data_2, second_data_1, second_data_2):
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
class WithProb(Textes):
    def __init__(self, name_file, alfavit):
        super().__init__(name_file,alfavit)
    def get_text(self):
        file = open(self.name_file, encoding='utf8')
        text = file.read().lower().replace('\n', '')
        text = re.sub(r'[^а-яё ]', '', text)
        file.close()
        return text
    def print_data(self):
        temp1 = self.get_freq_of_letters()
        e_temp1 = self.get_entropiy(temp1)
        print(f'Частота букв в таблиці букви.xlsx\nH1={e_temp1}\nНадлишковість - {self.calculate_entropy_lett(self._probel)}')
        temp11 = self.get_freq_of_bigrams(self.alfavit, True)
        e_temp11 = self.get_entropiy(temp11)
        print(f'Частота біграм в таблиці біграми.xlsx\nH2={e_temp11}\nНадлишковіть -  {self.calculate_entropy_bigr(self._probel, 1)}')
        temp12 = self.get_freq_of_bigrams(self.alfavit, False)
        etemp12 = self.get_entropiy(temp12)
        print(f'Частота перехресних біграм в таблиці перехрені_біграми.xlsx\nH2={etemp12}\nНадлишковість -{self.calculate_entropy_bigr(self._probel, 0)}')
        return temp1,temp11,temp12
class WithoutProb(Textes):
    def __init__(self, name_file, alfavit):
        super().__init__(name_file,alfavit)
    def calculate_entropy_bigr(self, txt, touch_point):
        distance = len(txt)
        if distance % 2 == 1 and touch_point == 0:
            distance -= 1
        bigr = []
        for i in range(0, distance - 1, 2 - touch_point):
            bigr.append(txt[i] + txt[i + 1])
        count = len(bigr)
        frequency = Counter(bigr)
        for i in frequency:
            frequency[i] /= count
        result = sum(frequency[k] * math.log(frequency[k], 2) for k in frequency) / (-2)
        return result
    def calculate_entropy_lett(self, txt):
        distance = len(txt)
        frequency = Counter(txt)
        for i in frequency:
            frequency[i] /= distance
        result = -1 * sum(frequency[k] * math.log(frequency[k], 2) for k in frequency)
        return result
    def print_data(self):
        temp2 = self.get_freq_of_letters()
        e_temp2 = self.get_entropiy(temp2)
        print(f'Частота букв в таблиці букви_без_пробілів.xlsx\nH1={e_temp2}\nНадлишковість - {self.calculate_entropy_lett(self._say_no_to_probel)}')
        temp21 = self.get_freq_of_bigrams(self.alfavit, True)
        e_temp21 = self.get_entropiy(temp21)
        print(f'Частота біграм в таблиці біграми_без_пробілів.xlsx\nH2={e_temp21}\nНадлишковість -{self.calculate_entropy_bigr(self._say_no_to_probel, 1)}')
        temp22 = self.get_freq_of_bigrams(self.alfavit, False)
        etemp22 = self.get_entropiy(temp22)
        print(f'Частота перехресних/біграм в таблиці перехресні_біграми_без_пробілів.xlsx\nH2-p = {etemp22}\nНадлилшковість - {self.calculate_entropy_bigr(self._say_no_to_probel, 0)}')
        return temp2, temp21, temp22

def save_results(first_data, second_data, first_data_1, first_data_2, second_data_1, second_data_2):
    pd.DataFrame(first_data.values(), index=first_data.keys()).to_excel('букви.xlsx')
    time_verable = np.array(list(first_data_1.values()))
    pd.DataFrame(time_verable.reshape((34, 34)), index=first_data.keys(), columns=first_data.keys()).to_excel(
        'біграми.xlsx')
    time_verable = np.array(list(first_data_2.values()))
    pd.DataFrame(time_verable.reshape((34, 34)), index=first_data.keys(), columns=first_data.keys()).to_excel(
        'перехресні_біграми.xlsx')
    pd.DataFrame(second_data.values(), index=second_data.keys()).to_excel('букви_без_пробілів.xlsx')
    vva = np.array(list(second_data_1.values()))
    pd.DataFrame(vva.reshape((33, 33)), index=second_data.keys(), columns=second_data.keys()).to_excel('біграми_без_пробілів.xlsx')
    time_verable, a22 = np.array(list(second_data_2.values())), pd.DataFrame(vva.reshape((33, 33)),
                                                                             index=second_data.keys(),
                                                                             columns=second_data.keys())
    a22.to_excel('перехресні_біграми_без_пробілів.xlsx')
def main():
    alfavit_with_prob = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя '
    alfavit = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
    with_prob = WithProb('data.txt', alfavit_with_prob)
    temp1,temp11,temp12 = with_prob.print_data()
    without_prob = WithoutProb('data.txt', alfavit)
    temp2, temp21, temp22=without_prob.print_data()
    save_results(temp1, temp2, temp11, temp12, temp21, temp22)
if __name__ == '__main__':
    main()
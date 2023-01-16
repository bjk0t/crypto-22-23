import re
import math
import pandas as pd
import numpy as np



class TextAnalyzer():
    def __init__(self):
        self.alfavit = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
        self.alfavit_with_prob = self.alfavit + ' '
    def nadl(self, e, total):# Рассчитываем значение переменной "e"
        # путем вычитания единицы из результата деления переменной "e"
        # на результат возведения числа в логарифм с двумя аргументами
        # по основанию 2 и переменной "total"
        return 1 - (e / math.log2(total))
    def entropy(self, dictionary, n):
        # Функция entropy принимает два аргумента: словарь и число n.
        # Функция использует цикл for для перебора всех ключей в словаре и проверки, что значение ключа не равно 0.
        # Если значение не равно 0, то добавляется в массив entropies.
        entropies = []
        for k in dictionary.keys():
            if dictionary[k] != 0:
                entropies.append(abs(float(dictionary[k]) * math.log2(dictionary[k]) / n))
        return sum(entropies)# В конце функция возвращает сумму всех значений из массива entropies.
    def fre_of_letters(self, txt,alfavit):
        # Цикл for проходит по всем элементам алфавита с вероятностями
        # Для каждого элемента создается пустой словарь с нулевым значением
        dictionary = {}
        for l in alfavit:
            dictionary.update({l: 0})
        # Цикл for проходит по всем символам текста
        # Для каждого символа словарь увеличивается на один
        for i in txt:
            dictionary[i] += 1
        # Цикл for проходит по всем элементам алфавита с вероятностями
        for l in alfavit:
            dictionary.update({l: round(dictionary[l] / len(txt), 5)})# Для каждого элемента считается вероятность и округляется до 5 знаков после запятой
        return dictionary        # Функция возвращает результирующий словарь
    def fre_of_bigrams(self, txt,alfavit, cross=True):
        # функция fre_of_bigrams() создает словарь с частотами встречаемости биграмм в тексте.
        # Параметр cross позволяет определить, будут ли в словарь добавляться и подсчитываться
        # биграммы, заканчивающиеся и начинающиеся на одну и ту же букву.
        dictionary = {}
        for l1 in alfavit:
            for l2 in alfavit:
                dictionary.update({l1 + l2: 0})

        if cross == True:
            for i in range(len(txt) - 1):
                dictionary[txt[i] + txt[i + 1]] += 1
            for key in dictionary.keys():
                dictionary[key] = round(dictionary[key] / (len(txt) - 1), 5)
        else:
            if len(txt) % 2 == 1:
                txt += "а"
            for i in range(len(txt) - 1):
                if i % 2 == 1:
                    continue
                dictionary[txt[i] + txt[i + 1]] += 1
            for key in dictionary.keys():
                dictionary[key] = round(dictionary[key] / (len(txt) - 1), 5)
        return dictionary
    def save(self,f1,f2,f11,f12,f21,f22):
        pd.DataFrame(f1.values(), index=f1.keys()).to_excel('Частота букв з пробілами.xlsx') #частота букв с пробелом
        time_verable = np.array(list(f11.values()))
        pd.DataFrame(time_verable.reshape((34, 34)), index=f1.keys(), columns=f1.keys()).to_excel('Частота біграм з пробілами.xlsx')
        time_verable = np.array(list(f12.values()))
        pd.DataFrame(time_verable.reshape((34, 34)), index=f1.keys(), columns=f1.keys()).to_excel('Частота перехресних біграм з пробілами.xlsx')
        pd.DataFrame(f2.values(), index=f2.keys()).to_excel('Частота букв без пробілів.xlsx')
        vva = np.array(list(f21.values()))
        pd.DataFrame(vva.reshape((33, 33)), index=f2.keys(), columns=f2.keys()).to_excel('Частота біграм без пробілів.xlsx')
        time_verable, a22 = np.array(list(f22.values())), pd.DataFrame(vva.reshape((33, 33)), index=f2.keys(), columns=f2.keys())
        a22.to_excel('Частота перехресних біграм без пробілів.xlsx')





    def main(self):

        # Этот код открывает файл 2.txt в кодировке UTF-8,
        # читает и преобразует его в нижний регистр, а также
        # удаляет переносы строк. Затем он использует регулярное
        # выражение для замены всех символов, кроме букв русского
        # алфавита и пробелов, на пустое значение. Далее он вычисляет
        # частоту букв и биграм, а также энтропию и надлишек, используя
        # соответствующие функции.
        file = open('2.txt', encoding='utf8')
        text = file.read().lower().replace('\n', '')
        text = re.sub(r'[^а-яё ]', '', text)
        file.close()
        print(f'===З пробілами===')
        f1 = self.fre_of_letters(text,self.alfavit_with_prob)
        print(f'Частота букв-{f1}')
        e_f1 = self.entropy(f1, 1)
        print(f'H1={e_f1}')
        print(f'Надл={self.nadl(e_f1, len(self.alfavit_with_prob))}')
        f11 = self.fre_of_bigrams(text,self.alfavit_with_prob, True)
        print(f'Частота біграм-{f11}')
        e_f11 = self.entropy(f11, 2)
        print(f'H2={e_f11}')
        print(f'Надл = {self.nadl(e_f11, len(self.alfavit_with_prob))}')
        f12 = self.fre_of_bigrams(text,self.alfavit_with_prob, False)
        print(f'Частота перехресних біграм - {f11}')
        ef12 = self.entropy(f12, 2)
        print(f'H2п={ef12}')
        print(f'Надл-{self.nadl(ef12, len(self.alfavit_with_prob))}')
        print(f'===Без пробілів===')
        file = open('2.txt', encoding='utf8')
        text = file.read().lower().replace('\n', '')
        text = re.sub(r'[^а-яё ]', '', text).replace(' ', '')
        file.close()
        f2 = self.fre_of_letters(text,self.alfavit)
        print(f'Частота букв-{f2}')
        e_f2 = self.entropy(f2, 1)
        print(f'H1={e_f2}')
        print(f'Надлишков={self.nadl(e_f2, len(self.alfavit))}')
        f21 = self.fre_of_bigrams(text,self.alfavit, True)
        print(f'Частота біграм-{f21}')
        e_f21 = self.entropy(f21, 2)
        print(f'H2={e_f21}')
        print(f'Надлишковість ={self.nadl(e_f21, len(self.alfavit))}')
        f22 = self.fre_of_bigrams(text, self.alfavit,False)
        print(f'Частота перехресних біграм - {f21}')
        ef22 = self.entropy(f22, 2)
        print(f'H2-p = {ef22}')
        print(f'Надлилшковість = {self.nadl(ef22, len(self.alfavit))}')
        self.save(f1, f2, f11, f12, f21, f22)

analyzer = TextAnalyzer()
analyzer.main()
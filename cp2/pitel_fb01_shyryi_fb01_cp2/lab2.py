import pandas as pd
from itertools import cycle
from collections import Counter

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

text = open('open text.txt', encoding='utf-8').read()
keys = open('keys.txt', encoding='utf-8').read().split()

def vigenere_encode(text, key, alphabet):
    key_cycle = cycle(key)
    encoded_text = ''
    for t, k in zip(text, key_cycle):
        encoded_text += alphabet[(alphabet.index(t) + alphabet.index(k)) % len(alphabet)]
    return encoded_text

def calculate_index(text):
    n, total, frequency_list = len(text), 0, {}
    for i in text: frequency_list[i] = 1 if i not in frequency_list else frequency_list[i] + 1
    frequency_list = sorted(frequency_list.items(), key=lambda item: item[1], reverse=True)
    for t in range(len(frequency_list)):
        chance = frequency_list[t][1]
        total += chance * (chance - 1)
    return (1 / (n * (n - 1))) * total

encoded_texts = []
index_values = [('key_length', 'index'), ('PlainText', calculate_index(text))]
for key in keys:
    encoded_text = vigenere_encode(text, key, alphabet)
    encoded_texts.append(encoded_text)
    blocks = [encoded_text[i::len(key)] for i in range(len(key))]
    blocks_index = sum(Counter(block)[max(Counter(block), key=lambda x: Counter(block)[x])] * (Counter(block)[max(Counter(block), key=lambda x: Counter(block)[x])] - 1) for block in blocks) / (len(encoded_text) * (len(encoded_text) - 1))
    index_values.append((len(key), blocks_index))

with open("encrypted_text.txt", "w") as f:
    for t in encoded_texts:
        f.write(t + '\n')

df1 = pd.DataFrame(index_values)
with pd.ExcelWriter("index.xlsx") as writer:
    df1.to_excel(writer, sheet_name = 'Task')

import matplotlib.pyplot as plt

x = [2, 3, 4, 6, 12, 16]
y = [0.004802738, 0.003780489, 0.00266055, 0.001876857, 0.001014531, 0.000781039]

plt.plot(x, y)
plt.xlabel('Довжина ключа')
plt.ylabel('Індекс відповідності')

plt.plot(x, y)
plt.show()

import matplotlib.pyplot as plt

x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
y = [0.037096826, 0.035352452, 0.039793512, 0.035435129, 0.037052369, 0.035223605, 0.044912132, 0.035450252, 0.03709763, 0.035062146, 0.039788848, 0.035509197, 0.037093872, 0.035384371, 0.055397665, 0.035524349, 0.03705114, 0.035315991, 0.039798398, 0.035056697, 0.03688095, 0.03526676, 0.044862927, 0.035316877, 0.037310869, 0.035247591, 0.039690867, 0.035584904, 0.036928329, 0.035273465]



plt.plot(x, y)
plt.xlabel('Довжина ключа')
plt.ylabel('Індекс відповідності')

plt.show()

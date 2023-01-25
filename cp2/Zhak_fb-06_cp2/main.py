from math import gcd
import string
import glob
import os
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter
matplotlib.use('TkAgg')
indexes = {}

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


'''
1. Самостійно підібрати текст для шифрування (2-3 кб) та ключі довжини r = 2, 3,
4, 5, а також довжини 10-20 знаків. Зашифрувати обраний відкритий текст шифром
Віженера з цими ключами.
'''

# with open('final.txt', 'r', encoding='utf-8') as file:
#     text = file.read()
#
# keys = {'r2': 'нг', 'r3': 'жак', 'r4': 'рево', 'r5': 'водка', 'r10': 'абдулкасим', 'r13': 'пивнаяторпеда',
#            'r17': 'материализовывать'}
#
# def encrypt(text, r):
#     encrypted = ""
#     for i in range(len(text)):
#         encrypted += alphabet[(alphabet.find(text[i]) + alphabet.find(r[i % len(r)])) % 32]
#     return encrypted
#
# for r, length in keys.items():
#     encrypted = encrypt(text, length)
#     with open(f"{r}.txt", 'w', encoding='utf-8') as file:
#         file.write(encrypted)


'''
2. Підрахувати індекси відповідності для відкритого тексту та всіх одержаних
шифртекстів і порівняти їх значення.
'''


def count_index(text):
    index = 0
    for char in alphabet:
        index += text.count(char) * (text.count(char) - 1)
    index *= 1 / (len(text) * (len(text) - 1))
    return index


# for file in glob.glob("*.txt"):
#     with open(file, 'r', encoding='utf-8') as f:
#         encrypted_text = f.read()
#     indexes[os.path.basename(f.name[:-4])] = count_index(encrypted_text)
#
# keys = ['r2', 'r3', 'r4', 'r5', 'r10', 'r13', 'r17', 'final']
# values = [indexes[key] for key in keys]
# for key in keys:
#     print(key + ' index: ' + str(indexes[key]))
#
# plt.bar(range(len(indexes)), values, align='center')
# plt.xticks(range(len(indexes)), keys)
# plt.show()


'''
3. Використовуючи наведені теоретичні відомості, розшифрувати наданий
шифртекст (згідно свого номеру варіанта).
'''


with open('encrypted_text.txt', 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

def create_blocks(text, r):
    blocks = []
    for i in range(r):
        blocks.append(text[i::r])
    return blocks


def calculate_indexes(text):
    indexes = {}
    for r in range(2, 35):
        blocks = create_blocks(text, r)
        index = 0
        for block in blocks:
            index += count_index(block)
        index /= r
        indexes[r] = index
    return indexes


# indexes = calculate_indexes(text)
# plt.figure(figsize=(12, 8))
# plt.bar(range(len(indexes)), list(indexes.values()), align='center')
# plt.xticks(range(len(indexes)), list(indexes.keys()))
# plt.show()


def find_key():
    period = 20
    blocks = create_blocks(text, period)
    encrypted_key = ''
    for block in blocks:
        letters_freq = Counter(block)
        encrypted_key += max(letters_freq, key=letters_freq.get)
    return encrypted_key


def decrypt_key():
    with open('common_letters.txt', 'r', encoding='utf-8') as file:
        letters = file.read()
    encrypted_key = find_key()
    key = ''
    for c in encrypted_key:
        key += alphabet[(alphabet.find(c) - alphabet.find(letters[0])) % 32]
    return key


def decrypt(text, key):
    decrypted_text = ''
    for i in range(len(text)):
        decrypted_text += alphabet[(alphabet.find(text[i]) - alphabet.find(key[i % 20])) % 32]
    return decrypted_text

key = 'улановсеребряныепули'
print(decrypt(text, key))


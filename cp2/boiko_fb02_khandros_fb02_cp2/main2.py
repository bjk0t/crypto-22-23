import re
from collections import Counter

alpha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
plain = re.sub(r'[^а-яА-Я]', '', open('open.txt', encoding='utf-8').read()).lower()
var9 = re.sub(r'[^а-яА-Я]', '', open('text.txt', encoding='utf-8').read()).lower()

def encrypt(text, key):
    cipher = ''
    for num, letter in enumerate(text):
        cipher += alpha[(alpha.index(letter) + alpha.index(key[num % len(key)])) % len(alpha)]
    return cipher

def c_index(segment):
    q = Counter(segment)
    c_ind = 0
    for el in q:
        c_ind += q[el] * (q[el] - 1)
    c_ind /= len(segment) * (len(segment) - 1)
    return c_ind

def find_cipher_key(text):
    c_index_theor = 0.0553
    keys_ind = {}
    for key_len in range(2, 35):
        avg_ind = 0.0
        segments = [text[i::key_len] for i in range(key_len)]
        for segm in segments:
            avg_ind += c_index(segm)
        avg_ind = avg_ind / len(segments)
        print(key_len)
        print(avg_ind)
        keys_ind[avg_ind] = key_len
    found_key_len = keys_ind.get(c_index_theor) or keys_ind[min(keys_ind.keys(), key=lambda key: abs(key - c_index_theor))]
    freq_letters = []
    for segm in [text[i::found_key_len] for i in range(found_key_len)]:
        freq_letters.append(Counter(segm).most_common(1)[0][0])
    possible_key = ''
    for e in range(len(freq_letters)):
        possible_key += alpha[(alpha.index(freq_letters[e]) - alpha.index('о')) % len(alpha)]
    return possible_key


def decrypt(text, key):
    plain = ''
    for pointer, char in enumerate(text):
        plain += alpha[(alpha.index(text[pointer % len(text)]) - alpha.index(
            key[pointer % len(key)]) + len(alpha)) % len(alpha)]
    print(plain)


#keys = ['да', 'так', 'дата', 'сырник', 'тысячаночей', 'оченьмногосимволов']
# for key in keys:
#     encr = encrypt(plain, key)
#     print(f'key: {key}, conformity: {c_index(encr)}')
#     print(encr)
# print(c_index(plain))
# print(find_cipher_key(var9))
# key = find_cipher_key(var9)
# print(key)
decrypt(var9, 'войнамагаэндшпиль')
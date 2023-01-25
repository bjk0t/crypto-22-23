from math import gcd
from collections import Counter
from math import log
from itertools import *

alph = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
top_rus_bigrams = ['ст', 'но', 'ен', 'то', 'на']

k = open('var8.txt', 'r', encoding='utf-8')
var8 = k.read()


def extended_evklid(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x

def linear(a, b, n):
    a = a % n
    b = b % n
    d = gcd(a, n)
    array = []
    if d == 1:
        array.append((extended_evklid(a, n) * b) % n)
        return array
    else:
        if b % d != 0:
            return array
        else:
            a = a // d
            b = b // d
            n = n // d
            array.append((linear(a, b, n)[0]))
            for i in range(1, d):
                array.append(array[-1] + n)
            return array


def bigrams_in_text(text):
    bigram_block= []
    for i in range(0, len(text) - 1, 2):
        bigram_block.append(text[i:i + 2])
    second_bigram_block = dict(Counter(bigram_block))
    sort = dict(islice(sorted(second_bigram_block.items(), key=lambda i: i[1], reverse=True), 5))
    return sort

bigrams_in_decoded_text = bigrams_in_text(var8)
print(bigrams_in_decoded_text)


def get_index(bigram):
    index = alph.index(bigram[0])*len(alph) + alph.index(bigram[1])
    return index


def linear_systems(text):
    bigrams = []
    linear_systems = []
    for i in top_rus_bigrams:
        for j in bigrams_in_decoded_text:
            bigrams.append((i, j))
    for i in bigrams:
        for j in bigrams:
            if i == j or (j, i) in linear_systems:
                continue
            elif i[0] == j[0] or i[1] == j[1]:
                continue
            linear_systems.append((i, j))
    return linear_systems

def solutions(linear_systems):
    key = []
    x1, x2, y1, y2 = get_index(linear_systems[0][0]), get_index(linear_systems[1][0]), get_index(
        linear_systems[0][1]), get_index(linear_systems[1][1])
    a = linear(x1 - x2, y1 - y2, 31 ** 2)
    for i in a:
        if gcd(i, 31) != 1:
            continue
        b = (y1 - i * x1) % 31 ** 2
        key.append((i, b))
    return key

def decode(decoded_text, my_key):
    array = []
    first_key,second_key = my_key[0], my_key[1]
    for i in range(0, len(decoded_text) - 1, 2):
        x = (extended_evklid(first_key, 31 ** 2) * (get_index(decoded_text[i:i + 2]) - second_key)) % (31 ** 2)
        array.append(alph[x // 31] + alph[x % 31])
    notsecrettext = ''.join(i for i in array)
    return notsecrettext



def find_keys(text):
    keys = []
    bigram_sys = linear_systems(text)
    for i in bigram_sys:
        solutions_of_sys = solutions(i)
        if len(solutions_of_sys) != 0:
            for j in range(len(solutions_of_sys)):
                keys.append(solutions_of_sys[j])
    return keys


def entropy(text):
    count_letters = Counter(text)
    for i in count_letters:
        count_letters[i]  /= len(text)
    answer = -1 * sum(float(count_letters[i]) * log(count_letters[i], 2) for i in count_letters)
    return answer



def keys_is_right(keys, cyphertext):
    no_matches = "no matches"
    for x in keys:
        e = entropy(decode(cyphertext, x))
        if (e > 4.0) and (e < 4.5):
            return x
    return no_matches

cipher = var8
keys_a_b = keys_is_right(find_keys(cipher), cipher)
print(keys_a_b)
decrypt = decode(cipher, keys_a_b)
print(decrypt)
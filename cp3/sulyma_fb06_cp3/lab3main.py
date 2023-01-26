from math import log
from collections import Counter

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
freq_check = ['о', 'а', 'е']


with open('text_utf.txt', 'r', encoding='utf-8') as x:
    text = x.read()
ciphertext = ''.join(i for i in text if i in alphabet)


def gcd(a, b):
    if b == 0:
        return abs(a)
    else:
        return gcd(b, a % b)


def mod_equ(a, b, m):
    a, b = a % m, b % m
    d = gcd(a, m)
    y = []
    if d == 1:
        y.append((euclid(a, m) * b) % m)
        return y
    else:
        if b % d != 0:
            return y
        else:
            a, b, m = a // d, b // d, m // d
            y.append((mod_equ(a, b, m)[0]))
            for i in range(1, d):
                y.append(y[-1] + m)
            return y


def euclid(a, b):
    y = [0, 1]
    while a != 0 and b != 0:
        if a > b:
            y.append(a // b)
            a = a % b
        elif b > a:
            y.append(b // a)
            b = b % a
        else:
            print("ne isnye")
    for i in range(2, len(y) - 1):
        y[i] = y[i - 2] + (-y[i]) * y[i - 1]
    return y[-2]


def most_common_bigrams(text):
    freqs_bigram = {}
    for i in range(len(text) - 1):
        bigram = (text[i], text[i + 1])
        if bigram not in freqs_bigram:
            freqs_bigram[bigram] = 0
        freqs_bigram[bigram] = freqs_bigram[bigram] + 1
    final_bigrams = list(sorted(freqs_bigram.items(), key=lambda item: item[1], reverse=True))[:5]
    sort_bigram = []
    for i in range(len(final_bigrams)):
        sort_bigram.append(final_bigrams[i][0])
    return sort_bigram


def bignum(bigram):
    num = alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])
    return num


def equa_sys(text):
    ru_freq = ['ст', 'но', 'ен', 'то', 'на']
    freq_text = most_common_bigrams(text)
    bigrams, sys_equa = [], []
    for i in ru_freq:
        for j in freq_text:
            bigrams.append((i, j))
    for i in bigrams:
        for j in bigrams:
            if i == j or (j, i) in sys_equa:
                continue
            elif i[0] == j[0] or i[1] == j[1]:
                continue
            sys_equa.append((i, j))
    return sys_equa


def decryption(text, keys):
    decipher = []
    x, y = keys[0], keys[1]
    for i in range(0, len(text) - 1, 2):
        k = (euclid(x, 31 ** 2) * (bignum(text[i:i + 2]) - y)) % (31 ** 2)
        decipher.append(alphabet[k // 31] + alphabet[k % 31])
    decrypt = ''.join(i for i in decipher)
    return decrypt


def sys_res(system_res):
    results = []
    x1, x2, y1, y2 = bignum(system_res[0][0]), bignum(system_res[1][0]), bignum(system_res[0][1]), bignum(system_res[1][1])
    k = mod_equ(x1 - x2, y1 - y2, 31 ** 2)
    for i in k:
        if gcd(i, 31) != 1:
            continue
        n = (y1 - i * x1) % 31 ** 2
        results.append((i, n))
    return results


def bigram_keys(text):
    x = []
    sys = equa_sys(text)
    for i in sys:
        root = sys_res(i)
        if len(root) != 0:
            for j in range(len(root)):
                x.append(root[j])
    return x


def entropy(text):
    counter = Counter(text)
    for i in counter:
        counter[i] /= len(text)
    res = -1 * sum(float(counter[i]) * log(counter[i], 2) for i in counter)
    return res


def truekeys(keys, text):
    for i in keys:
        decipher = decryption(text, i)
        x = list(sorted(Counter(decipher).items(), key=lambda item: item[1], reverse=True))
        sort = []
        for j in range(len(x)):
            sort.append(x[j][0])
        if sort[0] not in freq_check:
            continue
        theor_entropy = 4.35
        h = entropy(decryption(text, i))
        if (h > theor_entropy - 0.2) and (h < theor_entropy + 0.2):
            return i
    return -1


key = truekeys(bigram_keys(ciphertext), ciphertext)
print(key)
decrypt = decryption(ciphertext, key)
print(decrypt)

x = open('c.txt', 'w', encoding='utf-8')
x.write(decrypt)
x.close()

















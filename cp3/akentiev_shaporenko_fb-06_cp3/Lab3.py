from collections import Counter
from math import log2
import re
from math import gcd

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
file = open('V6.txt', encoding='utf-8')
text = file.read()
m = len(alphabet)


def text_space(text):
    txt = re.sub(r'[^а-яА-Я ]', '', text)
    space = txt.lower().replace('  ', ' ').replace('   ', ' ')
    return space


file_Space = open('S.txt', 'w', encoding='utf-8')
file_Space.write(text_space(text))
file_Space.close()

textWithSpace = text_space(text)
textWithoutSpace = textWithSpace.replace(' ', '')

file_No_Space = open('nS.txt', 'w', encoding='utf-8')
file_No_Space.write(textWithoutSpace)
file_No_Space.close()


def bigram_freq(textWithoutSpace):
    dict_bigram = [textWithoutSpace[i] + textWithoutSpace[i + 1] for i in range(0, len(textWithoutSpace)-1)]
    return dict_bigram


def bigram_freq5(textWithoutSpace):
    freq_bigram = {}
    for i in bigram_freq(textWithoutSpace):
        freq_bigram[i] = freq_bigram.get(i, 0) + 1
    return sorted(dict(Counter(freq_bigram)), key=dict(Counter(freq_bigram)).get, reverse=True)[:5]


def bigrams(textWithoutSpace):
    bigrams = [[b, b2] for b2 in bigram_freq5(textWithoutSpace) for b in ['ст', 'но', 'ен', 'то', 'на']]
    return  bigrams


def sys(textWithoutSpace):
    system = []
    for i, b in enumerate(bigrams(textWithoutSpace)):
        for j, b2 in enumerate(bigrams(textWithoutSpace)):
            if i == j: continue
            elif b[0] == b2[0]: continue
            elif b[1] == b2[1]: continue
            system.append([b, b2])
    return system


def newSys(textWithoutSpace):
    new_sus=[]
    for i in range(len(sys(textWithoutSpace))):
        a = sys(textWithoutSpace)[i]
        clist = [[alphabet.index(a[j][x][0]) * 31 + alphabet.index(a[j][x][1]) for x in range(2)] for j in range(2)]
        new_sus.append(clist)
    return new_sus


def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = ext_gcd(b % a, a)
    return gcd, y - (b // a) * x, x


def inverse(a, b):
    gcd, x, y = ext_gcd(a, b)
    if gcd == 1:
        return x % b
    else:
        return 0


def equations(a, b, mod):
    a %= mod
    b %= mod
    d = gcd(a, mod)
    if b % d:
        return []
    else:
        a //= d
        b //= d
        mod //= d
        x0 = inverse(a, mod)
        x0 = (x0 * b) % mod
        res = []
        for i in range(d):
            res.append((x0 + i * mod) % mod)
        return res


def keys():
    keys = []
    for i in newSys(textWithoutSpace):
        for j in equations(i[0][0] - i[1][0], i[0][1] - i[1][1], m ** 2):
            if gcd(j, len(alphabet)) != 1: continue
            keys.append([j, (i[0][1] - j * i[0][0]) % m ** 2])
    return keys


def decrypt(textWithoutSpace, keys):
    text = [(alphabet[(inverse(keys[0], 31 ** 2) * (alphabet.index(textWithoutSpace[i:i + 2][0]) * 31 + alphabet.index(textWithoutSpace[i:i + 2][1]) - keys[1])) % (31 ** 2) // 31] + alphabet[(inverse(keys[0], 31 ** 2) * (alphabet.index(textWithoutSpace[i:i + 2][0]) * 31 + alphabet.index(textWithoutSpace[i:i + 2][1]) - keys[1])) % (31 ** 2) % 31]) for i in range(0, len(textWithoutSpace) - 1, 2)]
    return ''.join(text)


def entropy(textWithoutSpace):
    letters = Counter(textWithoutSpace)
    entrop = 0
    for i in letters.keys():
        letters[i] = (letters[i]/len(textWithoutSpace))
        entrop -= (letters[i] * log2(letters[i]))
    return entrop


def main():
    for i in keys():
        if entropy(decrypt(textWithoutSpace, i)) < 4.5 and entropy(decrypt(textWithoutSpace, i)) > 4.4:
            print('Ключ:\n', i)
            print('Ентропія:\n', entropy(decrypt(textWithoutSpace, i)))
            print('Текст:\n', decrypt(textWithoutSpace, i))


main()

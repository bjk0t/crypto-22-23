from collections import Counter
from itertools import permutations

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"


def gcd_extended(a, b):
    arr = []
    while a > 0 and b > 0:
        if a > b:
            arr.append(-(a // b))
            a %= b
        else:
            arr.append(-(b // a))
            b %= a
    return [arr, a + b]


def summa(arr):
    q1 = 0
    q2 = 1
    for q in arr:
        temp = q2
        q2 = q2 * q + q1
        q1 = temp
    return q1


def inverse(a, mod):
    data = gcd_extended(a, mod)
    rev = summa(data[0])
    if rev > 0:
        return [rev, data[1]]
    return [rev + mod / data[1], data[1]]


def linear_equation(a, b, mod):
    payload = inverse(a, mod)
    if b % payload[1] == 0:
        i = 0
        arr = []
        x = ((b / payload[1]) * payload[0]) % (mod / payload[1])
        while i < payload[1]:
            arr.append(i * (mod / payload[1]) + x)
            i += 1
        return arr


def pull_number(let):
    return alphabet.index(let)
def pull_letter(n):
    return alphabet[n]


def nb(bi):
    n = pull_number(bi[0])
    n1 = pull_number(bi[1])
    return 31 * n + n1


def bn(num):
    n = pull_letter(int(num // 31))
    n1 = pull_letter(int(num % 31))
    return n + n1


def all_keys(y1, y2, x1, x2):
    mod = 31 ** 2
    x = nb(x1) - nb(x2)
    y = nb(y1) - nb(y2)
    if x < 0:
        x += mod
    if y < 0:
        y += mod
    a = linear_equation(x, y, mod)
    if a:
        b = (nb(y1) - nb(x1) * a[0]) % mod
        if b < 0:
            b += mod
        return [a[0], b]


def ckeys(arr):
    i = 0
    all = []
    common_bi = ['ст', 'но', 'то', 'на', 'ен']
    while i < 4:
        res = all_keys(arr[i], arr[i + 1], common_bi[i], common_bi[i + 1])
        all.append(res)
        i += 1
    return all


def decrypt(key, bigram):
    num = nb(bigram)
    inv = inverse(key[0], 31 ** 2)[0]
    inv = ((num - key[1]) * int(inv)) % (31 ** 2)
    return bn(inv)


def ret_keys(arr):
    perm = permutations(arr)
    arr = []
    for i in perm:
        arr += ckeys(i)
    return arr



datalab = open("datalab3.txt", encoding='utf-8')
datalab = datalab.read()

l = len(datalab)
cipher_bi_array = []
f = 0
while f < (l - 2):
    cipher_bi_array.append(datalab[f:f + 2])
    f += 2

cS = Counter(cipher_bi_array).most_common(5)
freq_bi_encr = [e[0] for e in cS]
print(freq_bi_encr)

allKeys = ret_keys(freq_bi_encr)

# keys = list(filter(lambda key: key != None, allKeys))
# print(list(filter(lambda key: key[0] == 13, keys)))
# for k in allKeys:
#     print(k)

#[314, 34]
# decrypted = ''
# for bi in cipher_bi_array:
#     decrypted += decrypt([314, 34], bi)
#
# print(decrypted)


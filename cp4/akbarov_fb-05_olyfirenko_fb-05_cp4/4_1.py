import random
import math
def prime(lenBits):
    while True:
        a = (random.randrange(2 ** (lenBits - 1), 2 ** lenBits))
        if miller(a):
            return a
def GKP():
    for i in range(0, 4):
        key = prime(256)
        keys.append(key)
    if keys[0] * keys[1] < keys[2] * keys[3]:
        return True
    else:
        keys.clear()
        GKP()
def miller(p, q=30):
    if p <= 3:
        raise Exception('number should be more than 3. ')
    if p % 2 == 0:
        return False
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(q):
        a = random.randint(2, p-2)
        b = pow(a, d, p)
        if b == 1 or b == p-1:
            continue
        for i in range(s-1):
            b = (b*b) % p
            if b == p-1:
                break
        else:
            return False
    return True

def Evklid(first, second):
    if first == 0:
        return second, 0, 1
    gcd, x0, y0 = Evklid(second % first, first)
    x = y0 - (second // first) * x0
    y = x0
    return [gcd, x, y]
def rev_el(number, module):
    gcd, x, y = Evklid(number, module)
    if gcd == 1:
        return (x % module + module) % module
    else:
        return -1
def  GKPRSA(p, q):
    n = p * q
    elerN = (p - 1) * (q - 1)
    e = random.randrange(2, elerN - 1)
    while math.gcd(e, elerN) != 1:
        e = random.randrange(2, elerN - 1)
    d = rev_el(e, elerN) % elerN
    return d, n, e
def Encrypt(M, e, n):
    C = pow(M, e, n)
    return C
def Decrypt(C, d, n):
    M = pow(C, d, n)
    return M
def sig(M, d, n):
    S = pow(M, d, n)
    return S
def ver(M, S, e, n):
    return M == pow(S, e, n)
def seke(k, d, e1, n1, n):
    K1 = Encrypt(k, e1, n1)
    S = sig(k, d, n)
    S1 = Encrypt(S, e1, n1)
    return K1, S1
def recke(K1, S1, d1, n1, e, n):
    K = Decrypt(K1, d1, n1)
    f.write(f'Розшифрований k = {k}')
    S = Decrypt(S1, d1, n1)

    if ver(K, S, e, n):
        f.write('Ключ отримано\n')
        return K
    else:
        f.write('Ключ не вдалося отримати')
def authentication(S, e, n):
    k = pow(S, e, n)
    return k
f=open('1.txt','w')
keys = []
GKP()
p = keys[0]
q = keys[1]
p1 = keys[2]
q1 = keys[3]
f.write('Перша пара  А:')
f.write(f'p:{p},q:{q})')
f.write('\nДруга пара  В:')
f.write(f'p:{p1},q:{q1})')
e, n, d =  GKPRSA(keys[0], keys[1])
f.write(f'e = {e}')
f.write(f'n = {n}',)
f.write(f'd = {d}')
e1, n1, d1 =  GKPRSA(keys[2], keys[3])
f.write(f'e1 = {e1}')
f.write(f'n1 = {n1}')
f.write(f'd1 = {d1}')
f.write("---------Ключі  А---------")
f.write('Відкриті ключі для А:')
f.write(f'e = {e}')
f.write(f'n = {n}',)
f.write('Секретний ключ для А:')
f.write(f'd = {d}')
f.write(f'p = {p}')
f.write(f'q = {q}')
f.write("---------Ключі  B---------")
f.write('Відкриті ключі для В:')
f.write(f'e1 = {e1}')
f.write(f'n1 = {n1}')
f.write('Секретний ключ для В:')
f.write(f'd1 = {d1}')
f.write(f'p1 = {p1}')
f.write(f'q1 = {q1}')
M = random.randint(0, n)
k = random.randint(0, n)
f.write(f'Початковий k = {k}')
f.write(f"Повідомлення: {M}")
K1, S1 = seke(k, d, e1, n1, n)
f.write(f'{type(S1)}')
E = Encrypt(M, e, n)
K = recke(K1, S1, d1, n1, e, n)
f.write(f"Шифрування: {E}")
D = Decrypt(E, d, n)
f.write(f"Розшифрування:{D}")
elerFun = (p - 1) * (q - 1)
f.write(f"Ф-ція Ейлера: {elerFun}")
f.write(f"Перевірка тексту: {M == D}" )
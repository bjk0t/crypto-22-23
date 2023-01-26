import random
import math

# ______________ №1 ______________

def miller_rabin(p, q=50):

    if p % 2 == 0:
        return False

    if p <= 3:
        return False
    else:
        #p-1 = d*2**s
        #s=0 => 2**s = 1

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

                    for _ in range(s-1):
                        b = (b**2) % p
                        if b == p-1:
                            break
                else:
                    return False
    return True


# ____________________ №2 ___________________

# Ф-ція для генерування простого числа
def prime_number(mass):
    while True:
        a = (random.randrange(2**(mass - 1), 2**mass))
        if miller_rabin(a):
            return a
        else:
            continue


def GenerateKeyPair():
    i = 0
    while i < 4:
        key = prime_number(256)
        arr.append(key)
        i=i+1
    if arr[0] * arr[1] < arr[2] * arr[3]:
        return True
    else:

        arr.clear()
        GenerateKeyPair()


arr = []
GenerateKeyPair()

for i in range (0,4):
    
    if i == 0:
        print("\n №2 \n\n")
        p = arr[i]
        print("Числа для абонента А:\np:", p)
    if i == 1:
        q = arr[i]
        print("q:", q)
    if i == 2:
        p1 = arr[i]
        print("\nЧисла для абонента В:\np:", p1)
    if i == 3:
        q1 = arr[i]    
        print("q:", q1)


# ______________________ №3 _______________________


def expanded_Evklid(first, second):
    if first == 0:
        return second, 0, 1

    gcd, x0, y0 = expanded_Evklid(second % first, first)
    x = y0 - (second // first) * x0
    y = x0

    return [gcd, x, y]


def reverse_el(number, module):
    gcd, x, y = expanded_Evklid(number, module)

    if gcd == 1:
        return (x % module + module) % module

    else:
        return -1


# Ф-ція для знаходження ключових пар для RSA
def key_pair_RSA(p, q):
    n = p * q
    u = (p - 1) * (q - 1)
    e = random.randrange(2, u - 1)
    while math.gcd(e, u) != 1:
        e = random.randrange(2, u - 1)
    d = reverse_el(e, u) % u
    return d, n, e


print('\n\n №3 \n\n')
e, n, d = key_pair_RSA(p, q)
print('e: ', e)
print('n: ', n)
print('d : ', d, '\n')

e1, n1, d1 = key_pair_RSA(p1, q1)
print('e1: ', e1)
print('n1: ', n1)
print('d1: ', d1, '\n')


print('Відкриті ключі [e,n] для aбонента А:')
print('e = ', e)
print('n = ', n)
print('Секретний ключ для абонента А:')
print('d = ', d)
print('p = ', p)
print('q = ', q, '\n')

print('Відкриті ключі [e,n] для абонента В:')
print('e1 = ', e1)
print('n1 = ', n1)
print('Секретний ключ для абонента В:')
print('d1 = ', d1)
print('p1 = ', p1)
print('q1 = ', q1, '\n')


# ______________________ №4 ______________________


def Encrypt(M, e, n):
    C = pow(M, e, n)
    return C


def Decrypt(C, d, n):
    M = pow(C, d, n)
    return M


def Sign(M, d, n):
    S = pow(M, d, n)
    return S

def Verify(M, S, e, n):
    return M == pow(S, e, n)


def SendKey(k, d, e1, n1, n):
    K1 = Encrypt(k, e1, n1)
    S = Sign(k, d, n)
    S1 = Encrypt(S, e1, n1)

    return K1, S1


def RecieveKey(K1, S1, d1, n1, e, n):
    K = Decrypt(K1, d1, n1)
    print('Розшифрований k: ', k, '\n')
    S = Decrypt(S1, d1, n1)

    if Verify(K, S, e, n):
        print('Ключ отримано\n')
        return K
    else:
        print('Ключ не вдалося отримати')


def authentication(S, e, n):
    k = pow(S, e, n)
    return k


M = random.randint(0, n)


print('\n\n №4 \n\n')

k = random.randint(0, n)
print('Початковий k = ', k, '\n')

print("Повідомлення: ", M, '\n')


K1, S1 = SendKey(k, d, e1, n1, n)

E = Encrypt(M, e, n)


K = RecieveKey(K1, S1, d1, n1, e, n)
print("Шифрування: ", E,"\n")


D = Decrypt(E, d, n)
print("Розшифрування:", D,"\n")

elerFun = (p - 1) * (q - 1)
print("Функція Ейлера:", elerFun,"\n")

print("Перевірка: ", M == D)

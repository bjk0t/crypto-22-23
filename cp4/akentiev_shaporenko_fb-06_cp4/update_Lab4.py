import random


def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = ext_gcd(b % a, a)
    return gcd, y - (b // a) * x, x


def inverse(a, b):
    gcd, x, y = ext_gcd(a, b)
    if gcd == 1:
        i = x % b
        return i
    else:
        return 0


def miller_rabin(n):
    if n == 2: return True
    elif n % 2 == 0: return False
    r = 0
    d = n - 1
    while d % 2 == 0:
        r = r + 1
        d = d // 2
    for _ in range(50):
        a = random.randrange(2, n - 1)
        if pow(a, d, n) == 1: continue
        elif pow(a, d, n) == n - 1: continue
        for _ in range(r - 1):
            if pow(pow(a, d, n), 2, n) == n - 1: break
        else:
            return False
    return True


def list():
    l = []
    n = 0
    x = 2**256-1
    y = 2**257
    while n < 4:
        num = random.randint(x, y)
        if miller_rabin(num):
            if num not in l:
                l.append(num)
                n = n + 1
    l.sort()
    return l


def generateKeyPair(p, q):
    return (p * q), inverse(100001, (p - 1) * (q - 1))


def decrypt(cipher, d, n):
    return pow(cipher, d, n)


def encrypt(message, e, n):
    return pow(message, e, n)


def verify(message, sign, e, n):
    return message == pow(sign, e, n)


def sign(message, d, n):
    return pow(message, d, n)


def sendKey(k, d, e1, n1, n):
    return encrypt(k, e1, n1), encrypt(sign(k, d, n), e1, n1)


def recieveKey(k1, S1, d1, n1, e, n):
    if verify(decrypt(k1, d1, n1), decrypt(S1, d1, n1), e, n):
        print('Key received\n')
        return decrypt(k1, d1, n1)
    else:
        print('The key could not be retrieved')


def main():
    n, d = generateKeyPair(list()[0], list()[1])
    n1, d1 = generateKeyPair(list()[2], list()[3])
    k = random.randint(0, n)
    k1, S1 = sendKey(k, d, 100001, n1, n)
    print('Message : ', 550)
    print('-------A-------')
    print('Public exponent: ', 100001)
    print('Public n: ', n)
    print('Encrypted A: ', encrypt(550, 100001, n))
    print('Decrypted A: ', decrypt(encrypt(550, 100001, n), d, n))
    print('Sign A: ', sign(550, d, n))
    print('Verify A: ', verify(550, sign(550, d, n), 100001, n))
    print('-------B-------')
    print('Public exponent1: ', 100001)
    print('Public n1: ', n1)
    print('Encrypted B: ', encrypt(550, 100001, n1))
    print('Decrypted B: ', decrypt(encrypt(550, 100001, n1), d1, n1))
    print('Sign B: ', sign(550, d1, n1))
    print('Verify B: ', verify(550, sign(550, d1, n1), 100001, n1), '\n')
    print('k = ', k, '\n')
    k = recieveKey(k1, S1, d1, n1, 100001, n)
    print('Encryption: ', encrypt(550, 100001, n))
    print('Decoding: ', decrypt(encrypt(550, 100001, n), d, n))
    print('Checking the text: ', 550 == decrypt(encrypt(550, 100001, n), d, n))


main()


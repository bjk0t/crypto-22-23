import random

min = 1 + 2 ** 225
max = -1 + 2 ** 256


def mirlabtest(number):
    t, s = number - 1, 0
    while t % 2 == 0:
        t = t // 2
        s += 1

    for i in range(300):
        a = random.randint(2, number - 2)
        y = pow(a, t, number)
        if (y == number - 1) or (y == 1):
            continue
        y = pow(y, 2, number)
        if y == 1 or y != number - 1:
            return False
    return True


def number_generate(min=min, max=max):
    number = random.randrange(min, max)
    while not mirlabtest(number):
        number = random.randrange(min, max)

    return number


def pair_create():
    new_pair = (number_generate(), number_generate())
    while new_pair[0] == new_pair[1]:
        new_pair[1] = number_generate()

    return new_pair


def extgcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extgcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def invers(x, y):
    a, b, c = extgcd(x, y)
    if a != 1:
        return 0
    else:
        return b % y


def rsa_generator(pair):
    k = pair[0] * pair[1]
    m = (pair[0] - 1) * (pair[1] - 1)
    flag = False
    while flag == False:
        e = random.randint(2, m)
        g, x, y = extgcd(e, m)
        if g == 1:
            flag = True
    d = invers(e, m)
    key = (e, k)
    privatekey = (d, pair[0], pair[1])
    return key, privatekey


class Rsa():
    def __init__(self):
        pair = pair_create()
        self.key, self.privatekey = rsa_generator(pair)

    def encrypt_func(self, text, key):
        return pow(text, key[0], key[1])

    def decrypt_func(self, text, privatekey):
        return pow(text, privatekey[0], privatekey[1] * privatekey[2])

    def sign_func(self, text, privatekey):
        return pow(text, privatekey[0], privatekey[1] * privatekey[2])

    def verify_func(self, sign, text, key):
        return text == pow(sign, key[0], key[1])

    def encrypted_message(self, text, key):
        etext = self.encrypt_func(text, key)
        sign = self.sign_func(text, self.privatekey)
        return etext, sign

    def decrypted_message(self, data, key):
        text, sign = data
        text = self.decrypt_func(text, self.privatekey)

        if self.verify_func(sign, text, key):
            print(text)


a = Rsa()
b = Rsa()

text = 312
data = a.encrypted_message(text, b.key)
b.decrypted_message(data, a.key)

x = open('log.txt', 'a', encoding='utf-8')
x.write('a Open key is: ' + str(a.key[0]) + str(a.key[1]) + '\n\n')
x.write('a private key is: ' + str(a.privatekey[0]) + str(a.privatekey[1]) + str(a.privatekey[2]) + '\n\n')
x.write('b Open key is: ' + str(b.key[0]) + str(b.key[1]) + '\n\n')
x.write('b private key is: ' + str(b.privatekey[0]) + str(b.privatekey[1]) + str(b.privatekey[2]) + '\n\n')
x.write('Sign: ' + str(data[1]))
x.close()

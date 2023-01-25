from random import randint
from numpy import gcd


def prime_test(num):
    if num % 2 == 0 or num % 3 == 0 or num % 5 == 0 or num % 7 == 0 or num % 11 == 0 or num % 13 == 0:
        print(num, 'not prime')
        return False

    d = num - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1

    x = randint(2, num - 2)

    if gcd(x, num) > 1:
        print(num, 'not prime')
        return False

    if pow(x, d, num) == 1 or pow(x, d, num) == -1:
        return True

    for i in range(1, s - 1):
        x = (x ** 2) % num
        if x == - 1:
            return True
        if x == 1:
            print(num, 'not prime')
            return False
    print(num, 'not prime')
    return False


def choose_number(h, l=0):
    while True:
        x = randint(l, h)
        if prime_test(x):
            return x


def make_keys(p, q):
    e = 2 ** 16 + 1
    n = p * q
    f = (p - 1) * (q - 1)
    d = pow(e, -1, f)
    return (n, e), (d, p, q)


def encrypt(message, open):
    return pow(message, open[1], open[0])


def decrypt(message, secret):
    return pow(message, secret[0], secret[1] * secret[2])


def sign(message, secret):
    return pow(message, secret[0], secret[1] * secret[2])


def verify(message, signed, open):
    if message == pow(signed, open[1], open[0]):
        return True
    return False


a_nums = (choose_number(2 ** 258, 2 ** 256), choose_number(2 ** 258, 2 ** 256))
b_nums = (choose_number(2 ** 258, 2 ** 256), choose_number(2 ** 258, 2 ** 256))

if a_nums[0] * a_nums[1] > b_nums[0] * b_nums[1]:
    a_nums, b_nums = b_nums, a_nums

a_open, a_secret = make_keys(a_nums[0], a_nums[1])
b_open, b_secret = make_keys(b_nums[0], b_nums[1])

print(f"A open key:{a_open}")
print(f"A secret key:{a_secret}")
print(f"B open key:{b_open}")
print(f"B secret key:{b_secret}")

message = randint(0, a_nums[0] * a_nums[1])

print(f"Message: {message}")

encrypted_message = encrypt(message, b_open)
print(f"Encrypted message: {encrypted_message}")

signed = sign(message, a_secret)
print(f"Signature: {signed}")

encrypted_sign = encrypt(signed, b_open)
print(f"Encrypted signature: {encrypted_sign}")

decrypted_message = decrypt(encrypted_message, b_secret)
print(f"Decrypted message: {decrypted_message}")

decrypted_sign = decrypt(encrypted_sign, b_secret)
print(f"Decrypted signature: {decrypted_sign}")


if verify(decrypted_message, decrypted_sign, a_open):
    print("Verified.")
else:
    print("Error.")
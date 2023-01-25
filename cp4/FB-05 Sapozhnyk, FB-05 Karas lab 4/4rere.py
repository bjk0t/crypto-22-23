import random
import math


class MillTst:
    def __init__(self, num, k=8):
        self.num = num
        self.k = k

    def test_number(self):
        if self.num == 2 or self.num == 3:
            return True
        if self.num % 2 == 0:
            return False
        r, s = 0, self.num - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        for _ in range(self.k):
            a = random.randrange(2, self.num - 1)
            x = pow(a, s, self.num)
            if x == 1 or x == self.num - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, self.num)
                if x == self.num - 1:
                    break
            else:
                return False
        return True


class PrimNum:
    def __init__(self, bits):
        self.bits = bits

    def find_number(self):
        print("Noprimary\n")
        while True:
            prim_number = (random.randrange(2 ** (self.bits - 1), 2 ** self.bits))
            if not MillTst(prim_number).test_number():
                print(f"{prim_number}")
            else:
                return prim_number


class KeyGen:
    def __init__(self):
        pass

    def generate_keys(self):
        keys = []
        for _ in range(4):
            key = PrimNum(256).find_number()
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys


class EvcExt:
    def __init__(self, first_number, second_number):
        self.first_number = first_number
        self.second_number = second_number

    def extended_evclid(self):
        if self.first_number == 0:
            return self.second_number, 0, 1
        else:
            div, koef_x, koef_y = EvcExt(self.second_number % self.first_number,
                                                 self.first_number).extended_evclid()
        return div, koef_y - (self.second_number // self.first_number) * koef_x, koef_x


class ModInv:
    def __init__(self, first_number, second_number):
        self.first_number = first_number
        self.second_number = second_number

    def inverse_mod(self):
        return list(EvcExt(self.first_number, self.second_number).extended_evclid())[1]


class RSAKeyPair:
    def __init__(self, first_key, second_key):
        self.first_key = first_key
        self.second_key = second_key

    def rsa_pair(self):
        res = []
        n = self.first_key * self.second_key
        oiler = (self.first_key - 1) * (self.second_key - 1)
        e = random.randrange(2, oiler - 1)
        while math.gcd(e, oiler) != 1:
            e = random.randrange(2, oiler - 1)
        d = ModInv(e, oiler).inverse_mod() % oiler
        res.append(d)
        res.append(n)
        res.append(e)
        return res


class Encrypting:
    def __init__(self, m, e, n):
        self.m = m
        self.e = e
        self.n = n

    def enc_msg(self):
        return pow(self.m, self.e, self.n)


class Decryption:
    def __init__(self, c, d, n):
        self.c = c
        self.d = d
        self.n = n

    def dec_msg(self):
        return pow(self.c, self.d, self.n)


class DigitalSign:
    def __init__(self, m, d, n):
        self.m = m
        self.d = d
        self.n = n

    def sign(self):
        return pow(self.m, self.d, self.n)


class SignCheck:
    def __init__(self, m, s, e, n):
        self.m = m
        self.s = s
        self.e = e
        self.n = n

    def sign_check(self):
        return self.m == pow(self.s, self.e, self.n)


class KeySend:
    def __init__(self, k, d, e1, n1, n):
        self.k = k
        self.d = d
        self.e1 = e1
        self.n1 = n1
        self.n = n

    def send_key(self):
        k1 = Encrypting(self.k, self.e1, self.n1).enc_msg()
        s = DigitalSign(self.k, self.d, self.n).sign()
        s1 = Encrypting(s, self.e1, self.n1).enc_msg()
        return k1, s1


class KeyReceiving:
    def __init__(self, key1, s1, d1, n1, e, n):
        self.key1 = key1
        self.s1 = s1
        self.d1 = d1
        self.n1 = n1
        self.e = e
        self.n = n

    def receive_key(self):
        key = Decryption(self.key1, self.d1, self.n1).dec_msg()
        s = Decryption(self.s1, self.d1, self.n1).dec_msg()
        if SignCheck(key, s, self.e, self.n).sign_check():
            return True, key
        else:
            return False, 0


gen_keys = KeyGen().generate_keys()
p, q, p1, q1 = gen_keys[0], gen_keys[1], gen_keys[2], gen_keys[3]
rsa_keys_a = RSAKeyPair(p, q).rsa_pair()
e, n, d = rsa_keys_a[0], rsa_keys_a[1], rsa_keys_a[2]
rsa_keys_b = RSAKeyPair(p1, q1).rsa_pair()
e1, n1, d1 = rsa_keys_b[0], rsa_keys_b[1], rsa_keys_b[2]
message = random.randint(0, n)
start_key = random.randint(0, n)
encrypted_key, dig_sign = KeySend(start_key, d, e1, n1, n).send_key()
encrypted_msg = Encrypting(message, e, n).enc_msg()
received_key = KeyReceiving(encrypted_key, dig_sign, d1, n1, e, n).receive_key()
decrypted_msg = Decryption(encrypted_msg, d, n).dec_msg()
print("\n\nА\n\n")
print(f'e: {e}\n'
      f'n: {n}\n'
      f'd: {d}\n'
      f'p: {p}\n'
      f'q: {q}\n')

print("\n\nB\n\n")
print(f'e1: {e1}\n'
      f'n1: {n1}\n'
      f'd1: {d1}\n'
      f'p1: {p1}\n'
      f'q1: {q1}\n')
print(f'Start kluch: {start_key}\n'
      f'Msg: {message}\n')
if received_key[0]:
    print(f'Kluch buv otryman: '
          f'{received_key[1]}\n')
if not received_key[0]:
    print('nevdacha y otrymci klucha')
print(f"zashyfrovane povidomlennya: {encrypted_msg}\n"
      f"rozshyfrovane povidomlennya: {decrypted_msg}")
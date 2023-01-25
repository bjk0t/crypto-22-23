from random import randint, getrandbits
class Random:
    @staticmethod
    def randint(size):
        return randint(2, size - 1)
    @staticmethod
    def getrandbits(size):
        return getrandbits(size)
class KeyGenerator:
    def __init__(self):
        pass

    def generate_keys(self):
        keys = []
        for _ in range(4):
            key = TestPrime(256).find_number()
            keys.append(key)
        if keys[0] * keys[1] < keys[2] * keys[3]:
            return keys

class g_c_d:
    @staticmethod
    def g_c_d(a, b):
        b2, y = b, \
                [-1]
        while y[-1] != 0:
            y.append(a - a // b * b)
            a, b = b,\
                   y[-1]
        return b2 \
            if (y[-1] == 0 and len(y) == 2) else y[-2]
class f_unc:
    @staticmethod
    def f_unc(a, b):
        odds = [0, 1]
        if g_c_d.g_c_d(a, b) > 1:
            return 0
        val1, val2, m = b, a, []
        while val2:
            m.append(-(val1 // val2))
            val1, val2 = val2, val1 % val2
        for i in range(len(m) - 1): odds.append(m[i] * odds[-1] + odds[-2])
        return odds[-1] + b if odds[-1] < 0 else odds[-1]
class p_o_w:
    @staticmethod
    def p_o_w(index, d, n):
        d_bin, result = list(bin(int(d))[2:]), 1
        for i in range(len(d_bin)):
            result = ((result * (index ** int(d_bin[i]))) ** 2) % n if i != len(d_bin) - 1 else (result * (
                    index ** int(d_bin[i]))) % n
        return result
class TestPrime:
    @staticmethod
    def test_for_prime_c(p):
        for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
            if p % i == 0:
                return \
                    False
        k, s, d = 8, 0, p - 1
        while d % 2 == 0:
            s, d = s + 1, d // 2
        iteration = 0
        while iteration < k:
            x = Random.randint(p)
            if g_c_d.g_c_d(x, p) != 1:
                return \
                    False
            ps = p_o_w.p_o_w(x, d, p)
            if ps == 1 or ps == -1:
                iteration += 1
                continue
            for r in range(1, s):
                x = p_o_w.p_o_w(x, 2, p)
                if x == -1:
                    return \
                        False
                elif x == 1:
                    return \
                        True
            iteration += 1
            return \
                False
        return \
            True
class RandPrime:
    @staticmethod
    def rand_prime(size):
        while True:
            value = Random.getrandbits(size)
            if TestPrime.test_for_prime_c(value):
                return \
                    value
class CreatePair:
    @staticmethod
    def create_pair():
        while True:
            p1, q1, p2, q2 = RandPrime.rand_prime(256), \
                             RandPrime.rand_prime(256), \
                             RandPrime.rand_prime(256), \
                             RandPrime.rand_prime(256)
            if p1 * q1 <= p2 * q2:
                return [[p1, q1], [p2, q2]]
class RSAPair:
    @staticmethod
    def rsa_pair(p, q):
        n = p * q
        phi = (p - 1) * (q - 1)
        while True:
            e = 65537
            if g_c_d.g_c_d(e, phi) == 1:
                d = f_unc.f_unc(e, phi)
                return [[d, p, q],
                        [e, n]]
class Encrypt:
    def __init__(self, m, e, n):



     def enc_msg(self):
            return p_o_w.p_o_w(self.m, self.e, self.n)
    @staticmethod
    def encrypt(self, m, e, n):
        return p_o_w.p_o_w(m,
                           e,
                           n)

class Decrypt:
    def __init__(self, c, d, n):
        self.c = c
        self.d = d
        self.n = n

    def dec_msg(self):
        return pow(self.c, self.d, self.n)
    @staticmethod
    def decrypt(c, d, n):
        return p_o_w.p_o_w(c, d, n)
class DS:
    @staticmethod
    def get_ds(m, d, n):
        return [m, p_o_w.p_o_w(m, d, n)]
    @staticmethod
    def ds_is_verified(ms, e, n):
        message, signature = ms[0], ms[1]
        return True if p_o_w.p_o_w(signature, e, n) == message else False

class DigiSign:
    def __init__(self, m, d, n):
        self.m = m
        self.d = d
        self.n = n

    def sign(self):
        return pow(self.m, self.d, self.n)


class SiCh:
    def __init__(self, m, s, e, n):
        self.m = m
        self.s = s
        self.e = e
        self.n = n

    def sich(self):
        if self.m == pow(self.s, self.e, self.n):
            print("Vdaloysa!")
        else:
            print("Nevdacha!")
        return self.m == pow(self.s, self.e, self.n)

    class KeySend:
        def __init__(self, k, d, e1, n1, n):
            self.k = k
            self.d = d
            self.e1 = e1
            self.n1 = n1
            self.n = n

        def send_key(self):
            k1 = Encrypt(self.k, self.e1, self.n1).enc_msg()
            s = DigiSign(self.k, self.d, self.n).sign()
            s1 = Encrypt(s, self.e1, self.n1).enc_msg()
            return k1, s1

    class KeyReceiving:
        def __init__(self, key_1, s1, d1, n1, e, n):
            self.key_1 = key_1
            self.s1 = s1
            self.d1 = d1
            self.n1 = n1
            self.e = e
            self.n = n

        def receive_key(self):
            key = Decrypt(self.key_1, self.d1, self.n1).dec_msg()
            s = Decrypt(self.s1, self.d1, self.n1).dec_msg()
            if SiCh(key, s, self.e, self.n).sich():
                return True, key
            else:
                return False, 0



class Start:
    @staticmethod
    def start():
        M = Random.getrandbits(256)
        pq1, pq2 = CreatePair.create_pair()[0], CreatePair.create_pair()[1]
        K_A = RSAPair.rsa_pair(pq1[0], pq1[1])
        K_B = RSAPair.rsa_pair(pq2[0], pq2[1])
        d1, \
        p1, \
        q1, \
        e1, \
        n1 = \
            K_A[0][0], \
             K_A[0][1],\
             K_A[0][2], \
             K_A[1][0],\
             K_A[1][1]
        d2,\
        p2,\
        q2,\
        e2,\
        n2 = \
            K_B[0][0], \
             K_B[0][1], \
             K_B[0][2],\
             K_B[1][0], \
             K_B[1][1]
        C = Encrypt.encrypt(M, e1, n1)
        MS = DS.get_ds(C, d2, n2)
        D = Decrypt.decrypt(MS[0], d1, n1) if DS.ds_is_verified(MS, e2, n2) else False
        if D:
            if D == M:
                print(f'B→A: OK!')
        else:
            print(f'B→A: Failed!')
        f=open('otvet.txt','w')
        f.write(str(f'\np1 = {p1}\n'
                    f'q1 -> {q1}\n'
                    f'p2 -> {p2}\n'
                    f'q2 ->{q2}\n\n'
                    f'd1 -> {d1}\n'
                    f'd2 -> {d2}\n'
                    f'e -> {e1}\n'
                    f'n1 -> {n1}\n'
                    f'n2 -> {n2}'))
        f.write(str(f'\nM -> {M}\n'
                    f'C -> {C}\n'
                    f'S -> {MS[1]}\n'
                    f'M\' -> {D}'))
Start.start()




n = int("B820DBA73C3FD23181372C74F18AE5FF883008DC01B9B47906C17F436D340CA5", 16)
print(f'n: {n}')
e = int("10001", 16)
print(f'e: {e}')
msg = int("65537", 16)
print(f'Message: {msg}')
encrypted_msg = Encrypt(msg, e, n).enc_msg()
print(f"Ciphertext: {hex(encrypted_msg)}")
sign = int("67857205CEAF5A3549C7E5747B8494B792D2DDC1341856997784BD492B875402", 16)
print(f"Sign is: {sign}")
SiCh(msg, sign, e, n).sich()
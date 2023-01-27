from random import randint

rmin_recommended = int('1' + '0' * 255, 2)
rmax_recommended = int('1' * 256, 2)


class RSA:
    optimal_rounds_num = 40

    def mr_test(k, n):

        rn = 2 + randint(1, n - 4)

        x = pow(rn, k, n)
        if (x == 1 or x == n - 1):
            return True

        while (k != n - 1):
            x = (x * x) % n
            k *= 2
            if (x == 1):
                return False
            if (x == n - 1):
                return True
        return False

    def isprime(n, rounds=optimal_rounds_num):

        # обработка крайних случаев
        if (n <= 1 or n == 4):
            return False
        if (n <= 3):
            return True

        k = n - 1
        while (k % 2 == 0):
            k //= 2
        for i in range(rounds):
            if (RSA.mr_test(k, n) == False):
                return False

        return True

    def prime_gen(rmin, rmax):
        while True:
            rn = randint(rmin, rmax)
            boolean = RSA.isprime(rn)
            # print(boolean)
            if boolean:
                return rn

    def smallbig_gen(rmin, rmax):
        n1 = RSA.prime_gen(rmin, rmax)
        n2 = RSA.prime_gen(rmin, rmax)
        return (n1, n2) if n1 <= n2 else (n2, n1)

    def pairs_gen(rmin, rmax):
        p1 = RSA.smallbig_gen(rmin, rmax)
        p2 = RSA.smallbig_gen(rmin, rmax)
        return (p1[0], p2[0]), (p1[1], p2[1])

    def gcd(a, mod):
        if a == 0:
            return mod, 0, 1
        gcd, x1, y1 = RSA.gcd(mod % a, a)
        x = y1 - (mod // a) * x1
        y = x1
        return gcd, x, y

    def inv_mod(a, m):
        gcd, x, y = RSA.gcd(a, m)
        if gcd == 1:
            return (x % m + m) % m
        else:
            return -1

    def keys_gen(p, q):
        n = p * q
        phi_n = (p - 1) * (q - 1)
        while True:
            e = randint(2, phi_n - 1)
            if RSA.gcd(e, phi_n)[0] == 1:
                d = RSA.inv_mod(e, phi_n)
                return e, n, d


class ABconversation:
    def __init__(self, p, q):
        self.q = q
        self.p = p

        rsa_keys = RSA.keys_gen(p, q)
        self.e = rsa_keys[0]
        self.n = rsa_keys[1]
        self.d = rsa_keys[2]

    def encrypt(self, message, e, n):
        result = pow(message, e, n)
        return result

    def _hex_encrypt(self, message, e, n):
        return hex(self.encrypt(int(message, 16), int(e, 16), int(n, 16)))

    def decrypt(self, ciphertext):
        result = pow(ciphertext, self.d, self.n)
        return result

    def _hex_decrypt(self, ciphertext):
        return hex(self.decrypt(int(ciphertext, 16)))

    def sign(self, message):
        result = pow(message, self.d, self.n)
        return result

    def _hex_sign(self, message):
        return self.sign(int(message, 16))

    def verify(self, message, ciphertext, e, n):
        message_check = pow(ciphertext, e, n)
        return message_check == message

    def _hex_verify(self, message, ciphertext, e, n):
        return self.verify(int(message, 16), int(ciphertext, 16), int(e, 16), int(n, 16))

    def public_str(self):
        return f"Modulus = {hex(self.n)}\n; E = {hex(self.e)}\n"

    def key_send(self, key, e, n):

        if self.n > n:
            print("!!!Incompatible keys!!!\nReGen keys")
            return 0

        enc_key = self.encrypt(key, e, n)
        sign = self.sign(key)
        enc_sign = self.encrypt(sign, e, n)

        return enc_key, enc_sign

    def _hex_key_send(self, key, e, n):
        enc_key, enc_sign = self.key_send(int(key, 16), int(e, 16), int(n, 16))
        return hex(enc_key), hex(enc_sign)

    def key_recv(self, key_enc, sign_enc, e, n):

        key = self.decrypt(key_enc)
        sign = self.decrypt(sign_enc)

        if self.verify(key, sign, e, n) == True:
            print("key exchange succeeded")
        else:
            print("exchange finished unsuccessfuly")

    def _hex_key_recv(self, key_enc, sign_enc, e, n):
        return self.key_recv(int(key_enc, 16), int(sign_enc, 16), int(e, 16), int(n, 16))


min, max = RSA.pairs_gen(rmin_recommended, rmax_recommended)

A = ABconversation(min[0], min[1])
B = ABconversation(max[0], max[1])

msg = randint(1, 2 ** 30)
print(f"Message: {msg}\n")

msg_enc = A.encrypt(msg, B.e, B.n)
sign = A.sign(msg)
print(B.e, "\n", B.n, "\n")

print(f'Encrypted msg: {msg_enc}')
print(f'Signature: {sign}\n\n')

msg_dec = B.decrypt(msg_enc)
s_verify = B.verify(msg_dec, sign, A.e, A.n)

print(f'Decrypted msg: {msg_dec}')
print(f'Verify: {s_verify}')

# k = randint(1, 2 ** 30)
# print(f'key: {k}\n')
#
# k_enc, s_enc = A.key_send(k, B.e, B.n)
# B.key_recv(k_enc, s_enc, A.e, A.n)
# print(A.public_str())

# server_n_hex = "0xB7DEF59947A69C9BA986030952D7D7C9D7902F5B143E6C1241ABAA567F178C35"
# server_e_hex = "0x10001"
# key = "XYZC"

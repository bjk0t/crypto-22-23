import random as rand
import math as m

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


class RSA():
    def __init__(self):
        pass

    @staticmethod
    def miller_test(p):
        if p < 2:
            return False
        if p in PRIMES:
            return True
        if p % 2 == 0:
            return False

        d = p - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(18):
            a = rand.randint(2, p - 2)
            x = pow(a, d, p)
            if x == 1 or x == p - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, p)
                if x == p - 1:
                    break
            else:
                return False

        return True

    @staticmethod
    def generate_prime(bits=256):
        while True:
            p = rand.getrandbits(bits)
            if p % 2 != 0 and RSA.miller_test(p):
                return p

    @staticmethod
    def generate_keys():
        keys = []
        while len(keys) < 4:
            keys.append(RSA.generate_prime(256))
            if len(keys) == 4 and keys[0] * keys[1] > keys[2] * keys[3]:
                keys = []
        return keys

    @staticmethod
    def extended_euclidean(a, b):
        if b != 0:
            gcd, x, y = RSA.extended_euclidean(b, a % b)
            return (gcd, y, x - (a // b) * y)
        return (a, 1, 0)

    @staticmethod
    def reverse(a, b):
        gcd = m.gcd(a, b)
        if gcd != 1:
            return None
        else:
            gcd, x, y = RSA.extended_euclidean(b, a % b)
            return y

    @staticmethod
    def generate_key_pair_rsa(p, q):
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = rand.randrange(2, phi_n - 1)
        while m.gcd(e, phi_n) != 1:
            e = rand.randrange(2, phi_n - 1)
        d = RSA.reverse(e, phi_n)
        return {'e': e, 'n': n, 'd': d}

    #   #   #   #   #   #   #   #   #

    @staticmethod
    def encrypt(message, public_key, modulus):
        return pow(message, public_key, modulus)

    @staticmethod
    def decrypt(ciphertext, private_key, modulus):
        return pow(ciphertext, private_key, modulus)

    @staticmethod
    def sign(message, private_key, modulus):
        return pow(message, private_key, modulus)

    @staticmethod
    def verify(message, signature, public_key, modulus):
        if message == pow(signature, public_key, modulus):
            return True
        return False

    #   #   #   #   #   #   #   #   #

    @staticmethod
    def send_key(key, private_key, receiver_public_key, receiver_modulus, modulus):
        encrypted_key = RSA.encrypt(key, receiver_public_key, receiver_modulus)
        signature = RSA.sign(key, private_key, modulus)
        encrypted_signature = RSA.encrypt(signature, receiver_public_key, receiver_modulus)
        return encrypted_key, encrypted_signature

    @staticmethod
    def receive_key(encrypted_key, encrypted_signature, private_key, modulus, sender_pub_key, sender_modulus):
        local_signature = RSA.decrypt(encrypted_signature, private_key, modulus)
        local_key = RSA.decrypt(encrypted_key, private_key, modulus)

        if RSA.verify(local_key, local_signature, sender_pub_key, sender_modulus):
            print("[+] Bob got the message")
            print(f"> Decrypted key: {local_key}\n")
            return local_key


keys = RSA.generate_keys()
print(f"""
keys:
{str(keys[0])[:12:]}...
{str(keys[1])[:12:]}...
{str(keys[2])[:12:]}...
{str(keys[3])[:12:]}...
""")

RSA_Alice = RSA.generate_key_pair_rsa(keys[0], keys[1])
RSA_Bob = RSA.generate_key_pair_rsa(keys[2], keys[3])

print("#            INFO")
print(f"""#    _Alice
# Public key: 
> e = {RSA_Alice['e']}
> n = {RSA_Alice['n']}
# Private key:
> p = {keys[0]}
> q = {keys[1]}
> d = {RSA_Alice['d']}
""")

print(f"""#    _Bob
# Public key: 
> e = {RSA_Bob['e']}
> n = {RSA_Bob['n']}
# Private key:
> p = {keys[2]}
> q = {keys[3]}
> d = {RSA_Bob['d']} \n
""")

print("#    Message transfer process")
# Alice creating message
message = rand.randint(1, RSA_Alice['n'])
key = rand.randint(1, RSA_Alice['n'])
print(f"> Generated message: {message}")

# Alice making signature (signature1) and send it to Bob
_key, _signature = RSA.send_key(key, RSA_Alice['d'], RSA_Bob['e'], RSA_Bob['n'], RSA_Alice['n'])
encrypted = RSA.encrypt(message, RSA_Alice['e'], RSA_Alice['n'])
print("> Encrypted message: ", encrypted, end='\n')
# sending...

# Bob receiving message
_key = RSA.receive_key(_key, _signature, RSA_Bob['d'], RSA_Bob['n'], RSA_Alice['e'], RSA_Alice['n'])

if _key:
    print("[+] Bob have received the message.")
    # Bob decrypting message with his private_key
    decrypted = RSA.decrypt(encrypted, RSA_Alice['d'], RSA_Alice['n'])
    if decrypted:
        print("[+] Bob have decrypted the message.")
        print(f"> Decrypted message: {decrypted}\n")
        if message == decrypted:
            print("[+] Decrypted message is equal to original.")
        else:
            print("[+] Decrypted message is not equal to original.")
    else:
        print("[-] Bob have not decrypted the message.")

else:
    print("[-] Bob have not received the message.")

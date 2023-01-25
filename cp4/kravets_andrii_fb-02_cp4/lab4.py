from typing import Tuple
from math import gcd
import random

def is_prime(n, k=5):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    def check_composite(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True
    for _ in range(k):
        if check_composite(random.randint(2, n - 2)):
            return False
    return True

def extended_euclidean_algorithm(a: int, b: int):
    if a == 0: return b, 0, 1
    gcd, x, y = extended_euclidean_algorithm(b % a, a)
    return gcd, y - (b // a) * x, x

def expanded_gcd(a, m):
    gcd, x, _ = extended_euclidean_algorithm(a, m)
    if gcd != 1: return None
    return x % m

def gen_random_prime_num(start, end):
    while True:
        p = random.randint(start, end)
        if p % 2 != 0 and is_prime(p):
            return p

def gen_rsa_pair(p: int, q: int) -> Tuple[int]:
    n =  p*q
    phi = (p-1) * (q-1)
    e = random.randint(2, phi-1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi-1)
    return e, n, expanded_gcd(e, phi) % phi


def encrypt(M: int, e: int, n: int) -> int: return pow(M, e, n)

def decrypt(C: int, d: int, n: int) -> int: return pow(C, d, n)

def signature(M: int, d: int, n: int) -> int: return pow(M, d, n)

def check(M: int, S: int, e: int, n: int) -> bool: return M == pow(S, e, n)

def send_key(key: int, d_sender, n_sender, e_receiver: int, n_receiver: int) -> Tuple[int, int]:
    k_encrypted = encrypt(key, e_receiver, n_receiver)
    s_encrypted = encrypt(signature(key, d_sender, n_sender), e_receiver, n_receiver)
    return k_encrypted, s_encrypted

def receive_key(key: int, sign: int, e_sender: int, n_sender: int, d_receiver: int, n_receiver: int):
    k_decrypted = decrypt(key, d_receiver, n_receiver)
    s_decrypted = decrypt(sign, d_receiver, n_receiver)
		
		
    if check(k_decrypted, s_decrypted, e_sender, n_sender):
        return k_decrypted



#### run all this stuff above

alice_p = gen_random_prime_num(2**255, 2**256)
alice_q = gen_random_prime_num(2**255, 2**256)
alice_e, alice_n, alice_d = gen_rsa_pair(alice_p, alice_q)

bob_p = gen_random_prime_num(2**255, 2**256)
bob_q = gen_random_prime_num(2**255, 2**256)
bob_e, bob_n, bob_d = gen_rsa_pair(bob_p, bob_q)

print(f"""
alice:
    pubkey
        - e -> {alice_e}
        - n -> {alice_n}
    
    secret
        - p -> {alice_p}
        - q -> {alice_q}
        - d -> {alice_d}

bob:
    pubkey
        - e -> {bob_e}
        - n -> {bob_n}
    
    secret
        - p -> {bob_p}
        - q -> {bob_q}
        - d -> {bob_d}
""")


secret_message = 66666666666666666666666666666666666666666
key = random.randint(0, alice_n)

print(f"""
   \033[92mMessage\033[0m ->\t {secret_message}
   \033[92mKey\033[0m     ->\t {key}
""")

encrypted_key, encrypted_signature = send_key(key, alice_d, alice_n, bob_e, bob_n)
print(f"""
    \033[91mEncrypted key\033[0m       ->  {encrypted_key}
    \033[91mEncrypted signature\033[0m ->  {encrypted_signature}
""")

encrypted_message = encrypt(secret_message, alice_e, alice_n)
print(f"""
    \033[91mEncrypted message\033[0m   ->  {encrypted_message}
""")

decrypted_message = decrypt(encrypted_message, alice_d, alice_n)
print(f"   \033[92mDecrypted message\033[0m   ->  {decrypted_message}\n")

decrypted_key = receive_key(encrypted_key, encrypted_signature, alice_e, alice_n, bob_d, bob_n)

if decrypted_key:
    print(f"   \033[92mDecrypted key\033[0m   ->  {decrypted_key}")
else:
    print("   \033[91mError\033[0m")
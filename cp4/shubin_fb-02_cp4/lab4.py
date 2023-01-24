import random
import math
import gmpy2


def small_primes_in_range(n):
    primes = []
    for i in range(2, n + 1):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            primes.append(i)
    return primes


def calculate_r_sequences(b):  # для кожного простого m в інтервалі [2;30] обчислює посл-ть r_i = B^i mod m довжини 20
    r_for_m = {}
    for m in small_primes:
        r = 1
        r_values = [1]
        for i in range(20):
            r = (r * b) % m
            r_values.append(r)
        r_for_m[m] = r_values
    return r_for_m


def pascal_is_divisible(number_as_digits, m):  # ознака подільності Паскаля
    n1 = sum(a_i * r_i for a_i, r_i in zip(reversed(number_as_digits), r_sequences[m]))
    if n1 % m == 0:
        return True
    else:
        return False


def trial_divisions_test(number):  # повертає True якщо число ділиться на якесь з простих
    a_sequence = [int(a_i) for a_i in str(number)]  # розбиваємо число на цифри
    for m in small_primes:
        if pascal_is_divisible(a_sequence, m):
            return True
    return False


def find_d_s(number):
    s = 0
    d = number - 1
    while d % 2 == 0:
        s += 1
        d = int(d // 2)
    return d, s


def gcd(a, b):  # Адгоритм Евкліда. повертає b=НСД(a, b)
    if a == 0:
        return b
    else:
        b = gcd(b % a, a)
        return b


def miller_rabin_test(p):  # повертає True якщо число є сильно псевдопростим, False якщо не є
    if trial_divisions_test(p):  # якщо число ділиться на якесь з простих, повертаємо False
        return False
    k = int(math.log2(p))
    d, s = find_d_s(p)
    for i in range(k):
        x = random.randint(2, p - 1)
        if gcd(x, p) != 1:
            return False
        else:
            # Перевіряємо, чи є p сильно псевдопростим за основою x
            if not gmpy2.powmod(x, d, p) in [1, p - 1]:  # якщо x^d mod p != +-1
                x_r = gmpy2.powmod(x, d * 2, p)
                for r in range(2, s + 1):  # Для всіх послідовних r від 1 до s - 1
                    if x_r == -1:
                        return True
                    elif x_r == 1:
                        return False
                    x_r = gmpy2.powmod(x_r, 2, p)
                return False
            else:
                return True  # якщо x^d mod p = +-1
    return True


def random_prime_of_length(n_bits):  # генерує просте число заданої довжини
    number = random.getrandbits(n_bits)  # генеруємо число заданої довжини з тестом пробних ділень
    while not miller_rabin_test(number):  # поки міллер-рабін не скаже що число просте, генеруємо заново
        number = random.getrandbits(n_bits)
    return number


def generate_p_q(n_bits):
    p = random_prime_of_length(n_bits)
    q = random_prime_of_length(n_bits)
    while p == q:  # якщо раптом згенерувалось p=q
        q = random_prime_of_length(n_bits)
    return p, q


def generate_p_q_pairs(n_bits):
    p, q = generate_p_q(n_bits)
    p1, q1 = generate_p_q(n_bits)
    while gmpy2.mul(p, q) > gmpy2.mul(p1, q1):
        p1, q1 = generate_p_q(n_bits)
    return p, q, p1, q1


def extended_gcd(a, b):  # РАЕ. повертає b=НСД(a, b), u,v -- такі що a*u + b*v = 1
    if a == 0:
        return b, 0, 1
    else:
        g, u1, v1 = extended_gcd(b % a, a)
        u = v1 - (b // a) * u1
        v = u1
        return g, u, v


def modular_inverse(a, n):  # знаходить x = a^-1 (mod n)
    g, u, v = extended_gcd(a, n)
    if g == 1:
        return u % n
    else:
        return None


def generate_rsa_keys(p, q):
    n = gmpy2.mul(p, q)
    fi_n = gmpy2.mul(p - 1, q - 1)
    e = 2 ** 16 + 1
    d = modular_inverse(e, fi_n)
    secret_key = {'d': d, 'p': p, 'q': q}
    public_key = {'n': n, 'e': e}
    return secret_key, public_key


def rsa_encrypt(message, public_key):
    return gmpy2.powmod(message, public_key['e'], public_key['n'])


def rsa_decrypt(ciphertext, secret_key, public_key):
    return gmpy2.powmod(ciphertext, secret_key['d'], public_key['n'])


def rsa_sign(message, secret_key, public_key):
    signature = gmpy2.powmod(message, secret_key['d'], public_key['n'])
    return {'message': message, 'signature': signature}


def rsa_verify(message, signature, public_key):
    if message == gmpy2.powmod(signature, public_key['e'], public_key['n']):
        return True
    else:
        return False


def rsa_send_key(k, sender_publickey, sender_secretkey, receiver_publickey):
    e, n = sender_publickey['e'], sender_publickey['n']
    e1, n1 = receiver_publickey['e'], receiver_publickey['n']
    d = sender_secretkey['d']
    s = gmpy2.powmod(k, d, n)
    k1 = gmpy2.powmod(k, e1, n1)
    s1 = gmpy2.powmod(s, e1, n1)
    return {'k1': k1, 's1': s1}


def rsa_receive_key(k1, s1, receiver_publickey, receiver_secretkey, sender_publickey):
    n1 = receiver_publickey['n']
    d1 = receiver_secretkey['d']
    k = gmpy2.powmod(k1, d1, n1)
    s = gmpy2.powmod(s1, d1, n1)

    # перевірка підпису
    e, n = sender_publickey['e'], sender_publickey['n']
    if k == gmpy2.powmod(s, e, n):
        authentication = True
    else:
        authentication = False
    print("received key:", k)
    print("authentication:", authentication)
    return {'k': k, 'authentication': authentication}


if __name__ == '__main__':
    B = 10
    small_primes = small_primes_in_range(1000)
    r_sequences = calculate_r_sequences(b=B)

    P, Q, P1, Q1 = generate_p_q_pairs(256)

    A_secret, A_public = generate_rsa_keys(P, Q)
    B_secret, B_public = generate_rsa_keys(P1, Q1)

    # Зашифровуємо і розшифровуємо ключами А
    print("\nЗашифровуємо і розшифровуємо ключами А:")
    M1 = random.getrandbits(256)
    M1_encrypted = rsa_encrypt(M1, A_public)
    M1_decrypted = rsa_decrypt(M1_encrypted, A_secret, A_public)
    # print(M1)
    # print(M1_decrypted)
    print("M1 == M1_decrypted:", M1 == M1_decrypted)

    # Зашифровуємо і розшифровуємо ключами В
    print("\nЗашифровуємо і розшифровуємо ключами B:")
    M2 = random.getrandbits(256)
    M2_encrypted = rsa_encrypt(M2, B_public)
    M2_decrypted = rsa_decrypt(M2_encrypted, B_secret, B_public)
    # print(M2)
    # print(M2_decrypted)
    print("M2 == M2_decrypted:", M2 == M2_decrypted)

    # Підписуємо ключем A
    print('\nПідписуємо ключем A:')
    M3 = random.getrandbits(256)
    signed_message = rsa_sign(M3, A_secret, A_public)
    # print("signed_message=", signed_message)
    print('Verification:', rsa_verify(signed_message['message'], signed_message['signature'], A_public))

    # Підписуємо ключем B
    print('\nПідписуємо ключем B:')
    M4 = random.getrandbits(256)
    signed_message = rsa_sign(M4, B_secret, B_public)
    # print("signed_message=", signed_message)
    print('Verification:', rsa_verify(signed_message['message'], signed_message['signature'], B_public))

    # протокол конфіденційного розсилання ключів з підтвердженням справжності по відкритому каналу
    # надсилаємо ключ від А до В
    print('\nПротокол конфіденційного розсилання ключів з підтвердженням справжності по відкритому каналу')
    key = random.getrandbits(200)
    # print("orig key:", key)
    signed_key = rsa_send_key(key, A_public, A_secret, B_public)
    received_key = rsa_receive_key(signed_key['k1'], signed_key['s1'], B_public, B_secret, A_public)
    print("orig_key == received key:", key == received_key['k'])

    # Взаємодія з сайтом
    print('\n================== Взаємодія з сайтом ==================')

    site_n = str(input('Введіть відкритий ключ сайту:')).lower()

    site_public = {'n': int(site_n, 16),
                   'e': int('10001', 16)}

    new_p_q = generate_p_q_pairs(128)[:2]
    our_secret, our_public = generate_rsa_keys(new_p_q[0], new_p_q[1])

    M = random.getrandbits(200)

    print("Наш відкритий ключ:\n",
          'n:', hex(our_public['n'])[2:], '\n',
          'e:', hex(our_public['e'])[2:])
    print("Наш секретний ключ:\n",
          'd:', hex(our_secret['d'])[2:], '\n',
          'p:', hex(our_secret['p'])[2:], '\n',
          'q:', hex(our_secret['q'])[2:])
    print("Відкритий ключ сайту:\n",
          'n:', hex(site_public['n'])[2:], '\n',
          'e:', hex(site_public['e'])[2:])

    print("Повідомлення:", hex(M)[2:])

    print("\n------ Сайт шифрує, ми розшифровуємо: ------")
    site_ciphertext = str(input("введіть шифротекст сайту:"))
    decrypted_site_ciphertext = rsa_decrypt(int(site_ciphertext, 16), our_secret, our_public)
    print("C:", site_ciphertext)
    print("M:", hex(M)[2:])
    print("Правильність повідомлення:", M == decrypted_site_ciphertext)

    print("\n------ Ми шифруємо, сайт розшифровує: ------")
    encrypted_M = rsa_encrypt(M, site_public)
    print("M:", hex(M)[2:])
    print("C:", hex(encrypted_M)[2:])
    site_decrypted_M = str(input("введіть розшифроване повідомлення сайту:")).lower()
    print("Сайт розшифрував:", site_decrypted_M)
    print("Правильність повідомлення:", M == int(site_decrypted_M, 16))

    print("\n------ Сайт підписує, ми перевіряємо: ------")
    print("M:", hex(M)[2:])
    site_signature = str(input('введіть підпис сайту:')).lower()
    print('Verification:', rsa_verify(M, int(site_signature, 16), site_public))

    print("\n------ Ми підписуємо, сайт перевіряє: ------")
    print("M:", hex(M)[2:])
    signature = rsa_sign(M, our_secret, our_public)['signature']
    print("Підпис:", hex(signature)[2:])
    print("Наш відкритий ключ:\n",
          'n:', hex(our_public['n'])[2:], '\n',
          'e:', hex(our_public['e'])[2:])

    print("\n------ Сайт надсилає ключ, ми отримуємо: ------")
    print("Наш відкритий ключ:\n",
          'n:', hex(our_public['n'])[2:], '\n',
          'e:', hex(our_public['e'])[2:])
    site_key = str(input("введіть ключ сайту:")).lower()
    site_sign = str(input("введіть підпис сайту:")).lower()
    result = rsa_receive_key(int(site_key, 16), int(site_sign, 16), our_public, our_secret, site_public)

    print("\n------ Ми надсилаємо ключ, сайт отримує: ------")
    key = random.getrandbits(100)
    sent_key = rsa_send_key(key, our_public, our_secret, site_public)
    print("Ключ:", hex(key)[2:])
    print("K1:", hex(sent_key['k1'])[2:])
    print("S1:", hex(sent_key['s1'])[2:])
    print("Наш відкритий ключ:\n",
          'n:', hex(our_public['n'])[2:], '\n',
          'e:', hex(our_public['e'])[2:])

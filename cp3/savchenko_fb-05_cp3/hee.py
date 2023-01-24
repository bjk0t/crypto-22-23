from math import gcd
import click

abc = "абвгдежзийклмнопрстуфхцчшщьыэюя"
freq_bi = ["ээ", "гн", "гг", "эч", "вд"]
freq_bi_lang = ["ст", "но", "то", "на", "ен"]

aabbcc = []
for i in abc:
    for j in abc:
        aabbcc.append(i+j)

def mod_inv(a, m):
    g, x, _ = extended_euclid(a, m)
    if g != 1:
        return 0
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def extended_euclid(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, y, x = extended_euclid(b, a % b)
        return (g, x, y - (a // b) * x)


def sd_linear_mod_comparison_solver(a, b, n):

    if a == 0:
        if b == 0:
            return []
            raise ValueError("infinite solutions")
        else:
            return []
            raise ValueError("no solution")
    else:
        d = gcd(a, n)
        def_n = n
        if d != 1:
            t = gcd(a, n)
            a = int(a/t)
            n = int(n/t)
            b = int(b/t)
        inv = mod_inv(a, n)
        x = (b * inv) % n
        solutions = [x]
        for i in range(1, d):
            solutions.append((x + i*n) % def_n)
        return solutions

def frequency_bigram(text):
    text = text.lower()
    bigram_counts = {}
    for i in range(len(text)-1):
        if text[i].isalpha() and text[i+1].isalpha():
            bigram = text[i] + text[i+1]
            if bigram in bigram_counts:
                bigram_counts[bigram] += 1
            else:
                bigram_counts[bigram] = 1
    total_bigrams = sum(bigram_counts.values())
    bigram_freqs = {bigram: count/total_bigrams for bigram,
                    count in bigram_counts.items()}
    return bigram_freqs

def linear_mod_comparison_solver(a, b, n):
    gcd_value = gcd(a, n)
    if b % gcd_value != 0:
        return (0, 0)
    else:
        a = a // gcd_value
        b = b // gcd_value
        n = n // gcd_value
        x = (b * mod_inv(a, n)) % n
        return (x, n)


def find_affine_keys(ciphertext_bigrams, language_bigrams):
    key_combinations = []
    keys1 = []
    keys2 = []
    for i in ciphertext_bigrams:
        for j in language_bigrams:
            keys1.append((i, j))
    for i in keys1:
        for j in keys1:
            keys2.append((i, j))
    for i in keys2:
        y1 = aabbcc.index(i[0][0]) % 31**2
        x1 = aabbcc.index(i[0][1]) % 31**2
        y2 = aabbcc.index(i[1][0]) % 31**2  
        x2 = aabbcc.index(i[1][1]) % 31**2

        a = sd_linear_mod_comparison_solver(
            (x1 - x2) % 31**2,
            (y1 - y2) % 31**2, 31**2)
            
            
        for i in a:
            key_b = (y1 - i * x1) % 31**2
            key_combinations.append((i, key_b))
    return key_combinations


def affine_decrypt(ciphertext, a, b):
    plaintext = ""
    a_inv = mod_inv(a, 31**2)
    for i in range(0, len(ciphertext), 2):
        bigram = ciphertext[i:i+2]
        x = aabbcc.index(bigram)
        deciphered_x = ((a_inv * (x - b))) % 31**2
        plaintext += aabbcc[deciphered_x]
    return plaintext

#################################################################### Типа main() ############################################################################################

# print(sd_linear_mod_comparison_solver(111, 75, 321))  # test

with open("09.txt", "r", encoding='utf-8', errors='ignore') as f:
    text = f.read()

bigram_freqs = frequency_bigram(text)

sorted_bigram_freqs = dict(
    sorted(bigram_freqs.items(), key=lambda item: item[1], reverse=True))

aff_key = find_affine_keys(freq_bi, freq_bi_lang)

aff_key[:] = list(set(aff_key))

# print(aff_key)

#print(sorted_bigram_freqs)


for i in range(len(aff_key)):
    dec_text = affine_decrypt(text, find_affine_keys(freq_bi, freq_bi_lang)[
                              i][0], find_affine_keys(freq_bi, freq_bi_lang)[i][1])

    bigram_freqs_text = frequency_bigram(dec_text)

    sorted_bigram_freqs = dict(
        sorted(bigram_freqs_text.items(), key=lambda item: item[1], reverse=True))
    
    com_bi = list(sorted_bigram_freqs.keys())[:5]

    matches = [bi for bi in com_bi if bi in freq_bi_lang]


    if len(matches) >= 4:
        print(matches)
    else:
        continue
    
    print("================================================================================================================================================================")
    print(find_affine_keys(freq_bi, freq_bi_lang)[
        i][0], find_affine_keys(freq_bi, freq_bi_lang)[i][1], i)
    print(dec_text)
    print("================================================================================================================================================================")
    if click.confirm("Сохранить этот текст?"):
        with open("decoded.txt", "w", encoding='utf-8') as f:
            f.write(f"Ключик - [{find_affine_keys(freq_bi, freq_bi_lang)[i][0]}, {find_affine_keys(freq_bi, freq_bi_lang)[i][1]}]. Текст: \n" + dec_text)



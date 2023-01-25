from itertools import product, permutations
from collections import Counter
from math import gcd

alph = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def convert_bg_to_num(bg): return alph.index(bg[0]) * 31 + alph.index(bg[1])

def convert_num_to_bg(num): return alph[num // 31] + alph[num % 31]

def most_common_bgrams():
    """Get 5 most comomn bgrams from encrypted text"""
    with open("12.txt", "r") as file: file = file.read().replace("\n", "").strip()
    return [k[0] for k in Counter(file[k:k+2] for k in range(0,len(file))).most_common(5)]

def extended_euclidean_algorithm(a: int, b: int):
    if a == 0: return b, 0, 1
    gcd, x, y = extended_euclidean_algorithm(b % a, a)
    return gcd, y - (b // a) * x, x

def expanded_gcd(a, m):
    gcd, x, _ = extended_euclidean_algorithm(a, m)
    if gcd != 1: return None
    return x % m

def mod_equation(a, b, m) -> int:
    """Calculate mod equation"""
    if gcd(a, m) == 1: return (extended_euclidean_algorithm(a, m)[1] * b) % m

def system():
    """"Create system of equations to solve them"""
    most_common_bgrams_list = most_common_bgrams()
    bgrams = list(product(["ст", "но", "то", "на", "ен"], most_common_bgrams_list))
    result = list(permutations(bgrams, 2))
    return [x for x in result if x[0] != x[1] and x[0][0] != x[0][1] and x[1][0] != x[1][1]]

def get_all_roots(vars):
    first_y = convert_bg_to_num(vars[0][0]) - convert_bg_to_num(vars[1][0])
    second_y = convert_bg_to_num(vars[0][1]) - convert_bg_to_num(vars[1][1])
    a = mod_equation(first_y, second_y, 31**2)
    if not a: return
    b = (convert_bg_to_num(vars[0][1]) - a * convert_bg_to_num(vars[0][0])) % (31**2)
    return a, b

def key_pairs():
    k = []
    for r in system():
        roots = get_all_roots(r)
        if roots: k.append(roots)
    return k

def check(some_text):
    result_text = []
    for text in some_text:
        if (text.count('о')/len(text) < 0.095 or text.count('а')/len(text) < 0.065): continue
        if (text.count('ф')/len(text) > 0.004 or text.count('щ')/len(text) > 0.005): continue
        result_text = text
    return result_text

def decrypt(keys):
    decrypted = []
    with open("12.txt", "r") as file:
        encrypted_text = file.read().replace("\n", "").strip()
    for k in keys:
        result_bgrams = []
        a = k[0]
        b = k[1]
        a = expanded_gcd(a, 31**2)
        if not a: continue
        for i in range(0, len(encrypted_text), 2):
            x_i = (a * (convert_bg_to_num(encrypted_text[i:i+2]) - b)) % (31**2)
            result_bgrams.append(convert_num_to_bg(x_i))
        decrypted.append("".join(k for k in result_bgrams))
    result_data = check(decrypted)
    return result_data

data = key_pairs()
print(decrypt(data))
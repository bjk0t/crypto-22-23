import re
from collections import Counter
from itertools import permutations, combinations

most_ordinary_bigrams = ['ст', 'но', 'то', 'на', 'ен']
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
cyphered_txt = re.sub(r'[^а-яА-Я]', '', open('V4.txt').read()).lower()

impossible_bigrams = ['аы', 'аь', 'еэ', 'жф', 'жч', 'жш', 'жщ', 'зп', 'зщ', 'йь', 'оы', 'уы', 'уь', 'фц',
                                     'хщ', 'цщ', 'цэ', 'чщ', 'чэ', 'шщ', 'ьы']


def gcd_extended(a, b):
    if b == 0:
        return a
    else:
        return gcd_extended(b, a % b)


def get_most_common_bi(txt):
    bigrams = Counter(txt[bi: bi + 2] for bi in range(0, len(txt) - 1, 2))
    bigrams = list(dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True)).keys())[:5]
    return bigrams


def get_all_bigrams(txt):
    return [txt[idx:idx + 2] for idx in range(0, len(txt) - 1, 2)]


def get_bi_in_int_value(bigram) -> int:
    return alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1])


def get_bi_from_int_value(bigram_int_value) -> str:
    return (alphabet[bigram_int_value // len(alphabet)]) + (alphabet[bigram_int_value % len(alphabet)])


def diversity(first_number, second_number) -> int:
    return first_number - second_number


def permutation(most_comm_ru_bigrams_value, most_comm_txt_bigrams_value):
    permuteted_values = permutations(most_comm_ru_bigrams_value)
    ready_made_permutations = []
    for p in permuteted_values:
        combinations = {}
        for i in range(len(most_comm_txt_bigrams_value)):
            combinations[most_comm_txt_bigrams_value[i]] = p[i]
        ready_made_permutations.append(combinations)
    return ready_made_permutations


def x_calculation(diff_X, diff_Y, mod=len(alphabet) ** 2) -> int:
    try:
        return int((diff_Y * int(pow(int(diff_X), -1, int(len(alphabet) ** 2)))) % mod)
    except Exception as ex:
        pass


def y_calculation(a, value_of_plain_bi, value_of_cipher_bi):
    try:
        return (value_of_cipher_bi - a * value_of_plain_bi) % (len(alphabet) ** 2)
    except Exception as ex:
        pass


def affine_cipher_crack(txt):
    most_comm_bigrams_in_txt = get_most_common_bi(txt)
    most_comm_bigrams_in_txt_value = []
    for bi in most_comm_bigrams_in_txt:
        most_comm_bigrams_in_txt_value.append(get_bi_in_int_value(bi))
    most_comm_bigrams_in_ru_value = []
    for bi in most_ordinary_bigrams:
        most_comm_bigrams_in_ru_value.append(get_bi_in_int_value(bi))

    pairs = permutation(most_comm_bigrams_in_ru_value, most_comm_bigrams_in_txt_value)

    all_pairs = []
    for i in range(len(pairs)):
        for x, y in pairs[i].items():
            all_pairs.append((x, y))
    all_pairs = list(set(all_pairs))
    all_pairs = list(combinations(all_pairs, 2))

    keys = []
    for pair in all_pairs:
        y1, y2 = pair[0][0], pair[1][0]
        x1, x2 = pair[0][1], pair[1][1]

        diff_Y = int(diversity(y1, y2))
        diff_X = int(diversity(x1, x2))

        gcd = gcd_extended(diff_X, (len(alphabet) ** 2))
        if diff_X != 0 or diff_Y != 0:
            if gcd == 1:
                a = x_calculation(diff_X, diff_Y, len(alphabet) ** 2)
                b = y_calculation(a, x1, y1)
                keys.append((a, b))
            elif gcd > 1 and diff_Y % gcd == 0:

                diff_Y /= gcd
                diff_X /= gcd

                mod = len(alphabet) ** 2 / gcd
                a = x_calculation(diff_X, diff_Y, mod)
                if not a: continue
                while a < len(alphabet) ** 2:
                    b = y_calculation(a, x1, y1)
                    keys.append((a, b))
                    a += gcd
    return list(set(keys))


def decode_txt(txt, key_tuple) -> str or None:
    a, b = key_tuple
    bigrams = get_all_bigrams(txt)
    decode_txt: str = ""
    try:
        for bigram in bigrams:
            decrypted_bigram = get_bi_from_int_value(
                (int(get_bi_in_int_value(bigram)) - int(b)) * int(pow(int(a), -1, int(len(alphabet) ** 2))) % (
                        len(alphabet) ** 2))
            decode_txt += decrypted_bigram
        number_of_bad_bi = Counter(decode_txt[bi: bi + 2] for bi in range(0, len(decode_txt) - 1, 2))
        for bigr in number_of_bad_bi.keys():
            if bigr in impossible_bigrams:
                if number_of_bad_bi.get(bigr) >= 3:
                    return
                else:
                    continue
        return decode_txt
    except Exception as ex:
        pass


def find_proper_key(keys):
    for key in keys:
        temp = decode_txt(cyphered_txt, key)
        if temp:
            print("Відкритий текст", "\n", temp)
            print("Отриманий ключ", "\n", key)


print ('Криптографія')
print ("Комп'ютерний практикум №3")
print ('Криптоаналіз афінної біграмної підстановки')
print ('Виконали: Лугінін Богдан та Хаустович Артем')
print ('Перевірила: Байденко П. В.')
print("\n", '-----------------------------------', "\n")
cyphered_txt = "".join([i for i in cyphered_txt if i in alphabet])
keys = affine_cipher_crack(cyphered_txt)
find_proper_key(keys)
print("\n", '-----------------------------------', "\n")
print ('The End')

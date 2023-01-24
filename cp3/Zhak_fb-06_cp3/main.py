from math import gcd

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
common_bigrams = ['ст', 'но', 'то', 'на', 'ен']


'''
1. Реалізувати підпрограми із необхідними математичними операціями:
обчисленням оберненого елементу за модулем із використанням розширеного алгоритму
Евкліда, розв’язуванням лінійних порівнянь. При розв’язуванні порівнянь потрібно
коректно обробляти випадок із декількома розв’язками, повертаючи їх усі.
'''


# розширений алгоритм Евкліда
def extended_euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_euclid(b % a, a)
        return g, y - (b // a) * x, x


# розв'язування лінійних порівнянь
def solve(a, b, mod=31):
    g = gcd(a, mod)
    if g == 1:
        return [(extended_euclid(a, mod)[1] * b) % mod]
    elif g > 1:
        if b % g != 0:
            return None
        x0 = (extended_euclid(a // g, mod // g)[1] * (b // g)) % (mod // g)
        roots = []
        for i in range(g):
            roots.append(x0 + i * (mod // g))
        return roots


'''
2. За допомогою програми обчислення частот біграм, яка написана в ході
виконання комп’ютерного практикуму №1, знайти 5 найчастіших біграм запропонованого
шифртексту (за варіантом).
'''


def bigram_frequency(text, step=2):
    bigrams = {}

    for i in range(0, len(text) - 1, step):
        j = i + 2
        if text[i:j] in bigrams:
            bigrams[text[i:j]] += 1
        else:
            bigrams[text[i:j]] = 1
    counter = sum(bigrams.values())

    for b, n in bigrams.items():
        bigrams[b] = round(n / counter, 5)

    return dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True))


'''
3. Перебрати можливі варіанти співставлення частих біграм мови та частих біграм
шифртексту (розглядаючи пари біграм із п’яти найчастіших). Для кожного співставлення
знайти можливі кандидати на ключ (a,b) шляхом розв’язання системи (1).
'''


# пари біграм із п’яти найчастіших
def create_pairs(b1, b2):
    start_bigrams = []
    pairs = []
    for plain in b1:
        for encrypted in b2:
            start_bigrams.append((plain, encrypted))
    for i in start_bigrams:
        for j in start_bigrams:
            if not i == j and not (j, i) in pairs and i[0] != j[0] and i[1] != j[1]:
                pairs.append((i, j))
    return pairs


# перетворення біграми в число
def get_x(bigram):
    return alphabet.index(bigram[0]) * 31 + alphabet.index(bigram[1])


# перетворення числа в біграму
def get_bigram(value):
    return alphabet[value // 31] + alphabet[value % 31]


# визначення параметру а(атака на афінний шифр)
def find_key(pair):
    x1, y1 = get_x(pair[0][0]), get_x(pair[0][1])
    x2, y2 = get_x(pair[1][0]), get_x(pair[1][1])
    x, y = x1 - x2, y1 - y2
    roots = solve(x, y, 31 ** 2)
    if roots is None:
        return None
    key = []
    for a in roots:
        key.append((a, (y1 - a * x1) % 31 ** 2))
    return key


# знаходження кандидатів на ключ
def get_keys(pairs):
    keys = []
    for pair in pairs:
        key = find_key(pair)
        if key:
            for k in key:
                keys.append(k)
    return keys


'''
4. Для кожного кандидата на ключ дешифрувати шифртекст. Якщо шифртекст не є
змістовним текстом російською мовою, відкинути цього кандидата.
'''


# дешифрування тексту
def decrypt(text, key):
    decrypted_text = ""
    for i in range(0, len(text) - 1, 2):
        y = get_x(text[i: i + 2])
        x = (extended_euclid(key[0], 31 ** 2)[1] * (y - key[1])) % 31 ** 2
        decrypted_text += get_bigram(x)
    return decrypted_text


# автоматична перевірка змістовності тексту
def check(text, keys):
    wrong_bigrams = ['еь', 'юы', 'яы', 'аы', 'оы', 'иы' 'аь', 'оь', 'ыь', 'уь', 'эы', 'ыы', 'уы', 'еы', 'юь', 'яь', 'эь', 'ць']
    meaning = True
    for key in keys:
        decrypted_text = decrypt(text, key)
        for wrong in wrong_bigrams:
            if wrong in decrypted_text:
                meaning = False
        if meaning:
            return key, decrypted_text
        meaning = True


with open('8.txt', 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

common_encrypted_bigrams = list(bigram_frequency(text).keys())[:5]

pairs = create_pairs(common_bigrams, common_encrypted_bigrams)

keys = get_keys(pairs)

key, result = check(text, keys)
print('Ключ:', key)
print('Дешифрований текст:', result)

with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
    file.write(result)
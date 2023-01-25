import matplotlib.pyplot as plt
from collections import Counter


alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def parse():
    """Func to parse all wrong charactres from first lab"""

    wrong_chars = list("abcdefjhigklmnopqrstuvyzswxё")
    wrong_chars += [k.upper() for k in wrong_chars] + list("№;-!><,.?[]}{:@#%^&*()+\||=1234567890\"/'")
    parsed_text: str = ""
    with open("some_text.txt", "r") as bad_file, open("some_parsed_text.txt", "w") as good_file:
        bad_file = bad_file.read().strip().lower()
        for k in bad_file:
            if k in wrong_chars:
                parsed_text += ""
            else:
                parsed_text += k

        result_parsed_text: str = "".join(parsed_text.split())
        good_file.write(result_parsed_text)


def encrypt_v(text, key):
    # gen key here repeating until len(key) != len(text)
    while len(key) < len(text):
        key += key
    else:
        key = key[:len(text)]

    # encryption part Ci = (Mi + Ki) mod N
    encrypted = ""

    for k in range(len(text)):
        encrypted += alph[(alph.index(text[k]) + alph.index(key[k])) % len(alph)]
    
    return encrypted

def decrypt_v(text, key):
    # gen key here
    while len(key) < len(text):
        key += key
    else:
        key = key[:len(text)]
    
    # decryption (just reversed encryption alg)
    decrypted = ""
    for k in range(len(text)):
        decrypted += alph[(alph.index(text[k]) - alph.index(key[k])) % len(alph)]

    return decrypted

def index(text):
    c, i = Counter(text), 0
    for k in c.values():
        i += k * (k - 1)
    return i / (len(text) * (len(text) - 1))
    

def key_attack(text, kl, d=2):
    a, b = [], [""] * d 
    
    [a.append("".join(text[k::kl])) for k in range(kl)]

    for k in a:
        c = {}
        data = sorted(Counter(k).items(), key=lambda item: item[1], reverse=True)
        for k, v in data:
            c[k] = v
        for i in range(d):
            b[i] += alph[(alph.index(list(c.keys())[i]) - alph.index("о")) % len(alph)]
    
    return b 

def p1():
    key_len_based_dict = dict()
    with open("some_parsed_text.txt", "r") as file:
        file = file.read()
        l = {k: file[:k] for k in [*range(2, 6), *range(10, 21)]}
        for k in l.values():
            key_len_based_dict[k] = encrypt_v(file, k)


    print(f"-\tDEFAULT TEXT\t{index(file)}")

    for k, v in key_len_based_dict.items():
        print(f"{len(k)}\t{k}\t\t{index(v)}")
        key_len_based_dict[k] = index(v)

    key_len_based_dict[""] = index(file)

    ### some hard transformations here, just for building the plot
    x, y = list(map(lambda j: len(j), key_len_based_dict.keys())), key_len_based_dict.values()
    fig, ax = plt.subplots()
    xx = range(len(x))

    ax.bar(xx, y, 0.5)
    ax.set_xticks(xx)
    _ = ax.set_xticklabels(x)

    plt.show()

def p2():
    key_len_based_dict, result_dict= dict(), dict()

    with open("encrypted.txt", "r") as file:
        encrypted = file.read().replace("\n", "").strip()
    
    key_length = list(range(2, 32))

    key_len_based_dict = {length: "".join(encrypted[::length]) for length in key_length}
    result_dict = {k: index(v) for k, v in key_len_based_dict.items()}
    
    # buld the plot to get the key length
    x, y = result_dict.keys(), result_dict.values()
    fig, ax = plt.subplots()
    xx = range(len(x))

    ax.bar(xx, y, 0.5)
    ax.set_xticks(xx)
    _ = ax.set_xticklabels(x)

    plt.show()

    # attack the encrypted text
    print(key_attack(encrypted, 14, d=3))

    # decrypt text based on guessed key
    print(decrypt_v(encrypted, "чугунныенебеса"))



p1()
p2()
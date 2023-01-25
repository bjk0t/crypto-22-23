from math import log2
from collections import Counter


def parse():
    """Func to parse all wrong charactres"""

    wrong_chars = list("abcdefjhigklmnopqrstuvyzswxё")
    wrong_chars += [k.upper() for k in wrong_chars] + list("№;-!><,.?[]}{:@#%^&*()+\||=1234567890\"/'")
    parsed_text: str = ""
    with open("bad_file.txt", "r") as bad_file, open("good_file.txt", "w") as good_file:
        bad_file = bad_file.read().strip().lower()
        for k in bad_file:
            if k in wrong_chars:
                parsed_text += ""
            else:
                 parsed_text += k

        result_parsed_text: str = " ".join(parsed_text.split())
        good_file.write(result_parsed_text)


def freq_m(is_space=True):
    """Count monogram частота з пробілами та зout"""

    with open("good_file.txt", "r") as file:
        file = file.read()
    
    if not is_space: 
        # replacing the пробілами
        file = file.replace(" ", "")

    dict_ = dict()

    for key, value in Counter(file).items():
        dict_[key] = value / len(file)

    return dict_


def freq_calc(dict_: dict):
    total = sum(dict_.values())
    return {bg: num / total for bg, num in dict_.items()}
    
    
def freq_bg(is_space, is_intersection):
    """Count bgram frequency with all possible different combinations"""

    with open("good_file.txt", "r") as file:
        file = file.read()
    
    if not is_space:

        if not is_intersection:
            file = file.replace(" ", "")
            res = Counter(file[k:k+2] for k in range(0, len(file), 2))

        elif is_intersection:
            file = file.replace(" ", "")
            res = Counter(file[k:k+2] for k in range(0, len(file)))

    elif is_space:

        if not is_intersection:
            res = Counter(file[k:k+2] for k in range(0, len(file), 2))

        elif is_intersection:
            res = Counter(file[k:k+2] for k in range(0, len(file)))

    return freq_calc(res)


def entr(dict_: dict, n: int):
    """Count Entropy"""

    data = dict_.values()
    e = -sum(p * log2(p) for p in data)
    e *= 1 / n

    return e


def red(h: float, n: int):
    """Count redunadncy for Entropy"""

    return 1 - (h / log2(n))


#### run all this stuff

parse()
#### 34 -- alph length with spaces, 33 - without
print(f"""
H1 монограм з пробілом {entr(freq_m(is_space=True), 1)}
надлишковість монограм з пробілом {red(entr(freq_m(is_space=True), 1), 34)}

H1 монограм без пробілів {entr(freq_m(is_space=False), 1)}
надлишковість монограм без пробілів {red(entr(freq_m(is_space=False), 1), 33)}


H2 біграм з пробілами та з перетинами {entr(freq_bg(is_space=True, is_intersection=True), 2)}
надлишковість біграм з пробілами та з перетинами {red(entr(freq_bg(is_space=True, is_intersection=True), 2), 34)}

H2 біграм з пробілами та без перетинів {entr(freq_bg(is_space=True, is_intersection=False), 2)}
надлишковість біграм з пробілами та без перетинів {red(entr(freq_bg(is_space=True, is_intersection=False), 2), 34)}

H2 біграм без пробілів та з перетинами {entr(freq_bg(is_space=False, is_intersection=True), 2)}
надлишковість біграм без пробілів та з перетинами {red(entr(freq_bg(is_space=False, is_intersection=True), 2), 33)}

H2 біграм без пробілів та без перетинів {entr(freq_bg(is_space=False, is_intersection=False), 2)}
надлишковість біграм без пробілів та без перетинів {red(entr(freq_bg(is_space=False, is_intersection=False), 2), 33)}

""")
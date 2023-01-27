import re

def read_file(filename):
    file = open(filename, 'r', encoding='utf-8')
    data_str = file.read().replace('\n', ' ')
    data_str = data_str.lower().replace('ё', 'е')
    data_str = data_str.replace('ъ', 'ь')
    data_str = re.sub('[^а-я]', '', data_str)
    return data_str

def calc_freq(string):
    text_len = len(string)
    freq_chars = {}
    for i in string:
        if i in freq_chars:
            freq_chars[i] += 1
        else:
            freq_chars[i] = 1
    rel_freq_chars = {}
    for letter in freq_chars.keys():
        rel_freq_chars[letter] = round((freq_chars[letter]) / text_len, 4)
    return rel_freq_chars

def check_vowels(freq_):
    freq = freq_.copy()
    print(freq)
    freq_l = list(freq.values())
    freq_l.sort()
    most_freq = freq_l[-3:]
    print(most_freq)

    del freq['а']
    del freq['о']
    del freq['е']

    print(freq)
    freq_l = list(freq.values())
    freq_l.sort()
    most_freq_2 = freq_l[-3:]
    print(most_freq_2)
    ans = True
    for i in most_freq_2:
        if i in most_freq:
            ans = False
    return ans

def check_cons(freq_):
    freq = freq_.copy()
    freq_l = list(freq.values())
    freq_l.sort()
    most_freq = freq_l[:3]
    print(freq)
    print(most_freq)

    del freq['ф']
    del freq['щ']
    del freq['ь']

    freq_l = list(freq.values())
    freq_l.sort()
    most_freq_2 = freq_l[:3]
    print(freq)
    print(most_freq_2)
    ans = True
    for i in most_freq_2:
        if i in most_freq:
            ans = False
    return ans

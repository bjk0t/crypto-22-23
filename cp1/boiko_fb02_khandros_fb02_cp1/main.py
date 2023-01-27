import math
import re

alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
alphabet_sp = "абвгдежзийклмнопрстуфхцчшщыьэюя "

# spaces -- bool; true - remove spaces in text
def clear_file(filename, spaces=True):
    file = open(filename, "r", encoding='utf-8')
    text = file.read()
    text = text.replace("\n", " ").replace("\r", "").lower().replace("ё", "е").replace("ъ", "ь")
    text = re.sub(r"[^а-я ]", "", text)
    if spaces:
        text = text.replace(" ", "");
    return text

def freq_lett(text):
    letters = {}
    for i in text:
        try:
            letters[i] += 1
        except:
            letters[i] = 1
    freq = {}
    for i in letters:
        freq[i] = letters[i]/len(text)
    return freq

# crossed -- bool; true -- using crossing bigrams
def freq_bi(text, crossed):
    birgams = {}
    len_t = len(text) if crossed else len(text)*2
    for i in range(0,len(text)-1, 2 if crossed else 1):
        try:
            birgams[text[i]+ text[i+1]] += 1
        except:
            birgams[text[i]+ text[i+1]] = 1
    freq_bigrams = {}
    for i in birgams:
        freq_bigrams[i] = birgams[i]/len_t
    return freq_bigrams

# len_t -- len of text 
def entropy(freq):
    entropy = 0
    for i in freq:
        entropy -= freq[i] * math.log2(freq[i])
    return entropy


filename = "data.txt"
text_sp = clear_file(filename, spaces=False)
text = clear_file(filename)

H1_no_sp = entropy(freq_lett(text))
R1_no_sp = 1 - H1_no_sp/math.log2(31)
print("Ентропія H1 без пробілів",H1_no_sp)
print("Надлишковість R1 без пробілів", R1_no_sp)

H1_sp = entropy(freq_lett(text))
R1_sp = 1 - H1_sp/math.log2(32)
print("Ентропія H1 з пробілами",H1_sp)
print("Надлишковість R1 з пробілами", R1_sp)


freq_lett_no_sp = freq_lett(text_sp)
print("Ентропія H1 без пробілів",entropy(freq_lett_no_sp))

H2_no_sp_cross = entropy(freq_bi(text, 1))
R2_no_sp_cross = 1 - H2_no_sp_cross/math.log2(31)
print("Ентропія H2 без пробілів, біграми пересікаються", H2_no_sp_cross)
print("Надлишковість R2 без пробілів, біграми пересікаються", R2_no_sp_cross)

H2_sp_cross = entropy(freq_bi(text_sp, 1))
R2_sp_cross = 1 - H2_sp_cross/math.log2(32)
print("Ентропія H2 з пробілами, біграми пересікаються", H2_sp_cross)
print("Надлишковість R2 з пробілами, біграми пересікаються", R2_sp_cross)

H2_no_sp_no_cross = entropy(freq_bi(text, 0))
R2_no_sp_no_cross = 1 - H2_no_sp_no_cross/math.log2(31)
print("Ентропія H2 без пробілів, біграми не пересікаються", H2_no_sp_no_cross)
print("Надлишковість R2 без пробілів, біграми не пересікаються", R2_no_sp_no_cross)

H2_sp_no_cross = entropy(freq_bi(text_sp, 0))
R2_sp_no_cross = 1 - H2_sp_no_cross/math.log2(32)
print("Ентропія H2 з пробілами, біграми пересікаються", H2_sp_no_cross)
print("Надлишковість R2 з пробілами, біграми пересікаються", R2_sp_no_cross)

print("1.752 < H10 < 2.356")
print( (1-(1.752/math.log2(32))), "> R >", (1-(2.356/math.log2(32))))
print("1.784 < H20 < 2.492")
print( (1-(1.784/math.log2(32))), "> R >", (1-(2.492/math.log2(32))))
print("1.437 < H30 < 2.18")
print( (1-(1.437/math.log2(32))), "> R >", (1-(2.18/math.log2(32))))
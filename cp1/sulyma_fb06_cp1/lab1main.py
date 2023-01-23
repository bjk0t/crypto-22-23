import math
from io import open
import pandas as pd
import string

x = open('text.txt', encoding='utf-8')
text = x.read()
x.close()
text = text.lower()
text = ' '.join(text.split())

alphabet_with_space = 'а,б,в,г,д,е,ё,ж,з,и,й,к,л,м,н,о,п,р,с,т,у,ф,х,ц,ч,щ,ъ,ы,ь,э,ю,я, '

new_text = ''
for i in text:
    if i in alphabet_with_space:
        new_text = new_text + i

new_text = new_text.translate(str.maketrans('', '', string.punctuation))

freq_char = {}
for i in new_text:
    keys = freq_char.keys()
    if i in keys:
        freq_char[i] = freq_char[i] + 1
    else:
        freq_char[i] = 1

final_char = {key: freq_char[key] / len(new_text) for key in freq_char.keys()}
h1ws = sum(list(map(lambda y: -y * math.log2(y), final_char.values())))

freq_bigram = {}
for i in range(len(new_text)-1):
    bigram = (new_text[i], new_text[i+1])
    if bigram not in freq_bigram:
        freq_bigram[bigram] = 0
    freq_bigram[bigram] = freq_bigram[bigram] + 1

final_bigram = {key: freq_bigram[key] / sum(freq_bigram.values()) for key in freq_bigram.keys()}
h2ws = 1/2 * sum(list(map(lambda y: -y * math.log2(y), final_bigram.values())))

no_space_alphabet = 'а#б#в#г#д#е#ё#ж#з#и#й#к#л#м#н#о#п#р#с#т#у#ф#х#ц#ч#щ#ъ#ы#ь#э#ю#я'.split('#')

new_text1 = ''
for i in text:
    if i in no_space_alphabet:
        new_text1 = new_text1 + i

freqs_char = {}
for i in new_text1:
    keys = freqs_char.keys()
    if i in keys:
        freqs_char[i] = freqs_char[i] + 1
    else:
        freqs_char[i] = 1

final_chars = {key: freqs_char[key] / len(new_text1) for key in freqs_char.keys()}
h1ns = sum(list(map(lambda y: -y * math.log2(y), final_chars.values())))

freqs_bigram = {}
for i in range(len(new_text1)-1):
    bigram = (new_text1[i], new_text1[i+1])
    if bigram not in freqs_bigram:
        freqs_bigram[bigram] = 0
    freqs_bigram[bigram] = freqs_bigram[bigram] + 1

final_bigrams = {key: freqs_bigram[key] / sum(freqs_bigram.values()) for key in freqs_bigram.keys()}
h2ns = 1/2 * sum(list(map(lambda y: -y * math.log2(y), final_bigrams.values())))

redundancy1 = (1 - h1ws/math.log2(len(alphabet_with_space)))
redundancy2 = (1 - h2ws/math.log2(len(alphabet_with_space)))
redundancy3 = (1 - h1ns/math.log2(len(no_space_alphabet)))
redundancy4 = (1 - h2ns/math.log2(len(no_space_alphabet)))
print('surplus H2 without spaces:', redundancy4)
print('surplus H1 without spaces:', redundancy3)
print('surplus H2 with spaces:', redundancy2)
print('surplus H1 with spaces:', redundancy1)

print('H1 with spaces:', h1ws)
print('H2 with spaces:', h2ws)
print('H1 without spaces:', h1ns)
print('H2 without spaces:', h2ns)

df = pd.DataFrame(final_char.items(), columns=['Key', 'Value'])
df.to_excel('freq_letters_w_space.xlsx', 'Data', index=False)
x.close()

df = pd.DataFrame(final_bigram.items(), columns=['Key', 'Value'])
df.to_excel('freq_bigrams_w_space.xlsx', 'Data', index=False)
x.close()

df = pd.DataFrame(final_chars.items(), columns=['Key', 'Value1'])
df.to_excel('freq_letters_no_space.xlsx', 'Data', index=False)
x.close()

df = pd.DataFrame(final_bigrams.items(), columns=['Key', 'Value'])
df.to_excel('freq_bigrams_no_space.xlsx', 'Data', index=False)
x.close()

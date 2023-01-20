import re
import collections
import unicodedata
import pandas as pd

def clean_text(string):
    return re.sub(r'[^а-яА-Я]+', '', string)

textfile = 'text.txt'
with open(textfile, mode='r', encoding='utf-8') as file:
    content = file.read()
    lowercase_content = content.lower()
    withoutspace = clean_text(lowercase_content)
    with open("text_withoutspace.txt", "w") as out_file:
        out_file.write(withoutspace)
print(withoutspace)


from collections import Counter

def count_letters(string):
    return Counter(string.lower())

letter_count = count_letters(withoutspace)
print(letter_count)

def count_letters(string):
    return Counter(string.lower())

letter_count = count_letters(withoutspace)
total_letters = sum(letter_count.values())
data = {'letter': [], 'frequency': []}
for letter, count in letter_count.items():
    frequency = count/total_letters
    data['letter'].append(letter)
    data['frequency'].append(frequency)
freq = pd.DataFrame(data)
freq.to_excel("letter_frequencies.xlsx",index=False)

def count_bigrams_cyrillic(string):
    string = re.sub('[^а-яА-Я]', '', string)
    return Counter(zip(string, string[1:]))


bigram_count = count_bigrams_cyrillic(withoutspace)
for bigram, count in bigram_count.items():
    print(f"{bigram}: {count}")

def count_bigrams_step2(string):
    return Counter(zip(string[::2], string[1::2]))


bigram_count = count_bigrams_step2(withoutspace)
for bigram, count in bigram_count.items():
    print(f"{bigram}: {count}")

text = withoutspace
bigram = []
bigramtwo = []
for j in range(0, len(text)-1):
    bigram.append(text[j]+text[j+1])
    
for j in range(0, len(text)-2,2):
    bigramtwo.append(text[j]+text[j+1])

from collections import Counter
bigramcount = dict(Counter(bigram))

freqbigram = {k: bigramcount[k] / len(bigram) for k in bigramcount}

bigramtwocount = dict(Counter(bigramtwo))
freqbigramtwo = {k: bigramtwocount[k] / len(bigramtwo) for k in bigramtwocount}

print(freqbigram[bigram[1]])
print(bigram[1])

import math

def entropy(text):
    text_len = len(text)
    char_freq = {}
    for char in text:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    entropy = 0
    for char in char_freq:
        probability = char_freq[char] / text_len
        entropy -= probability * math.log2(probability)
    return entropy

print(entropy(withoutspace))

import math

def entropy(text, n=2):
    text_len = len(text) - n + 1
    bigram_freq = {}
    for i in range(text_len):
        bigram = text[i:i+n]
        if bigram in bigram_freq:
            bigram_freq[bigram] += 1
        else:
            bigram_freq[bigram] = 1
    entropy = 0
    for bigram in bigram_freq:
        probability = bigram_freq[bigram] / text_len
        entropy -= probability * math.log2(probability)
    return entropy

print(entropy(withoutspace))

from collections import defaultdict
from operator import itemgetter
import pandas as pd

def bigram_freq(text):
    text_len = len(text) - 1
    bigram_freq = defaultdict(int)
    for i in range(text_len):
        bigram = text[i:i+2]
        bigram_freq[bigram] += 1
    return bigram_freq

bigram_freq = bigram_freq(withoutspace)

bigram_freq_table = pd.DataFrame(list(bigram_freq.items()), columns=['bigram', 'frequency'])
bigram_freq_table = bigram_freq_table.sort_values(by='frequency', ascending=False)
print(bigram_freq_table)

from collections import defaultdict
from operator import itemgetter
import pandas as pd

def bigram_freq(text):
    text_len = len(text) - 1
    bigram_freq = defaultdict(int)
    for i in range(text_len):
        bigram = text[i:i+2]
        bigram_freq[bigram] += 1
    return bigram_freq

bigram_freq = bigram_freq(withoutspace)

bigram_freq_table = pd.DataFrame(list(bigram_freq.items()), columns=['bigram', 'frequency'])
bigram_freq_table = bigram_freq_table.sort_values(by='frequency', ascending=False)

bigram_freq_table['percentage'] = bigram_freq_table['frequency']/bigram_freq_table['frequency'].sum()*100

bigram_freq_table.to_excel("bigram_frequency.xlsx")

from collections import defaultdict
from operator import itemgetter
import pandas as pd

def bigram_freq(text, step=2):
    text_len = len(text) - step + 1
    bigram_freq = defaultdict(int)
    for i in range(text_len):
        bigram = text[i:i+step]
        bigram_freq[bigram] += 1
    return bigram_freq

bigram_freq = bigram_freq(withoutspace, step=2)

bigram_freq_table = pd.DataFrame(list(bigram_freq.items()), columns=['bigram', 'frequency'])
bigram_freq_table = bigram_freq_table.sort_values(by='frequency', ascending=False)

print(bigram_freq_table)

print(freqbigram['аа'])

data_2= pd.DataFrame.from_dict(freqbigramtwo,'index').stack().reset_index(level=0)  
data_2 = data_2.sort_values(by=0, ascending=False)
data_2 = data_2.rename(columns = {'level_0': 'bigram2', 0: 'freq2'})
data_2

Alp = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж',' з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
df = pd.DataFrame(index = Alp, columns=Alp)

bg = []

for i in Alp:
    for j in Alp:
        bg.append(i+j)
 
n = 0
for i in range(0,len(Alp)):
    df[Alp[i]] = bg[n:len(Alp)+n]
    n = len(Alp)+n
df = df.T

import numpy as np

for b in list(freqbigram.keys()):
    a,c = np.where(df == b)
    df.iloc[a,c] = freqbigram[b]
    
for b in bg:
    a,c = np.where(df == b)
    df.iloc[a,c] = 0

print(df)
df.to_excel("freqbigram_withoutspace.xlsx")

df = pd.DataFrame(index = Alp, columns=Alp)

bg = []

for i in Alp:
    for j in Alp:
        bg.append(i+j)
 
n = 0
for i in range(0,len(Alp)):
    df[Alp[i]] = bg[n:len(Alp)+n]
    n = len(Alp)+n
df = df.T

for b in list(freqbigramtwo.keys()):
    a,c = np.where(df == b)
    df.iloc[a,c] = freqbigramtwo[b]
    
for b in bg:
    a,c = np.where(df == b)
    df.iloc[a,c] = 0
    
print(df.head())
df.to_excel("freqbigram2_withoutspace.xlsx")



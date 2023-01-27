from collections import Counter
import re 
import math
from pprint import pprint

alfavit_p = len('абвгдеёжзийклмнопрстуфхцчшщъыьэюя ')
alfavit = len('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

text = open('ourText.txt', mode = 'r', encoding="utf8").read()
text = text.lower()
obrob_text_p = re.sub( r'[^а-яё ]', '',text)
obrob_text = re.sub( r'[^а-яё]', '',text)
obrob_text_p = ' '.join(obrob_text_p.split())
obrob_text = ' '.join(obrob_text.split())


with open("obrob_text_probels.txt", mode = "w") as text_p:
    text_p.write(obrob_text_p)
text_with_probels = obrob_text_p


with open("obrob_text.txt", mode = "w") as text_without_probels:
    text_without_probels.write(obrob_text)
text_without_probels = obrob_text

h1_p_chastota = []
h1_p_letter_name = []

dovzhyna_p = len(text_with_probels)
dictionary_p = dict(Counter(text_with_probels))

h1_chastota = []
h1_letter_name = []

dovzhyna = len(text_without_probels)
dictionary = dict(Counter(text_without_probels))


def bigGramCouple(ourText, crossing):  # Підрахунок частоти біграм
    objectCoupleAmount = {}  # {біграма: кількість}
    if crossing:  
        for i in range(0, len(ourText)):
            if ourText[i:i+2] in objectCoupleAmount:
                objectCoupleAmount[ourText[i:i+2]] += 1
            else:
                objectCoupleAmount[ourText[i:i+2]] = 1
    else:  # Пари букв, що не перетинаються
        for i in range(0, len(ourText), 2):  # з кроком 2
            if ourText[i:i+2] in objectCoupleAmount:
                objectCoupleAmount[ourText[i:i+2]] += 1
            else:
                objectCoupleAmount[ourText[i:i+2]] = 1
                
    generalSum = sum(objectCoupleAmount.values())
    for couple in objectCoupleAmount:
    # частотf біграм
        objectCoupleAmount[couple] = objectCoupleAmount[couple]/generalSum
    return objectCoupleAmount

######################################################################################################

print("---------------------------------------------------------------")
print ('Частота букв з пробілом:')
for key in dictionary_p:
    h1_p_letter_name.append(key)
    h1_p_chastota.append(dictionary_p[key] / dovzhyna_p)
    print(key,":",dictionary_p[key] / dovzhyna_p)

print("---------------------------------------------------------------")
first_bigram_p = []
for x in range(0, len(text_with_probels) - 1):
    first_bigram_p.append(text_with_probels[x] + text_with_probels[x + 1])

print('Першна біграма з пробілами:')

dictionary_first_bigram_p = dict(Counter(first_bigram_p))
dovzhyna_first_bigram_p = sum(dictionary_first_bigram_p.values())
h2_chastota_first_p = []
h2_letter_name_first_p = []
for key in dictionary_first_bigram_p:
    h2_letter_name_first_p.append(key)
    h2_chastota_first_p.append(dictionary_first_bigram_p[key] / dovzhyna_first_bigram_p)
pprint(bigGramCouple(obrob_text_p, True))


second_bigram_p = []    
for x in range(0, len(text_with_probels) - 2, 2):
    second_bigram_p.append(text_with_probels[x] + text_with_probels[x + 1])

print('Друга біграма з пробілами:')

dictionary_second_bigram_p = dict(Counter(second_bigram_p))
dovzhyna_second_bigram_p = sum(dictionary_second_bigram_p.values())
h2_chastota_second_p = []
h2_letter_name_second_p = []
for key in dictionary_second_bigram_p:
    h2_letter_name_second_p.append(key)
    h2_chastota_second_p.append(dictionary_second_bigram_p[key] / dovzhyna_second_bigram_p)
pprint(bigGramCouple(obrob_text_p, False))

#///////////////////

print("---------------------------------------------------------------")
print ('Частота букв без пробілів:')
for key in dictionary:
    h1_letter_name.append(key)
    h1_chastota.append(dictionary[key] / dovzhyna)
    print(key,":",dictionary[key] / dovzhyna)

print("---------------------------------------------------------------")
first_bigram = []
for x in range(0, len(text_without_probels) - 1):
    first_bigram.append(text_without_probels[x] + text_without_probels[x + 1])
print('Перша біграма без пробілів:')

dictionary_first_bigram = dict(Counter(first_bigram))
dovzhyna_first_bigram = sum(dictionary_first_bigram.values())
h2_chastota_first = []
h2_letter_name_first = []
for key in dictionary_first_bigram:
    h2_letter_name_first.append(key)
    h2_chastota_first.append(dictionary_first_bigram[key] / dovzhyna_first_bigram)
pprint(bigGramCouple(obrob_text, True))

second_bigram = []    
for x in range(0, len(text_without_probels) - 1, 2):
    second_bigram.append(text_without_probels[x] + text_without_probels[x + 1])

print('Друга біграма без пробілів:')

dictionary_second_bigram = dict(Counter(second_bigram))
dovzhyna_second_bigram = sum(dictionary_second_bigram.values())
h2_chastota_second = []
h2_letter_name_second = []
for key in dictionary_second_bigram:
    h2_letter_name_second.append(key)
    h2_chastota_second.append(dictionary_second_bigram[key] / dovzhyna_second_bigram)
pprint(bigGramCouple(obrob_text, False))

#//////////Top 15//////////#
print("---------------------------------------------------------------")
print('>>>TOP 15:<<<')
 
dictionary_H1_top10_p = sorted(dictionary_p.items(), key=lambda item: item[1], reverse=True)
s = dictionary_H1_top10_p[:15]
print("Топ 15 H1 з пробілами:",s)

dictionary_H1_top10 = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
s = dictionary_H1_top10[:15]
print("Топ 15 H1 без пробілів:",s)

dictionary_wp_h2_first_top10 = sorted(dictionary_first_bigram_p.items(), key=lambda item: item[1], reverse=True)
s = dictionary_wp_h2_first_top10[:15]
print("Топ 15 H2 з пробілами:",s)

dictionary_h2_first_top10 = sorted(dictionary_first_bigram.items(), key=lambda item: item[1], reverse=True)
s = dictionary_h2_first_top10[:15]
print("Топ 15 H2 без пробілів:",s)

dictionary_wp_h2_second_top10 = sorted(dictionary_second_bigram_p.items(), key=lambda item: item[1], reverse=True)
s = dictionary_wp_h2_second_top10[:15]
print("Топ 15 H2 з пробілами_крк2:",s)

dictionary_h2_second_top10 = sorted(dictionary_second_bigram.items(), key=lambda item: item[1], reverse=True)
s = dictionary_h2_second_top10[:15]
print("Топ 15 H2 без пробілів_крк2:",s)

#////////////////////ENTROPIA////////////////////#
print("---------------------------------------------------------------")
print("ЕНТРОПІЯ:")

entropia_h1_p = map(lambda x: -x * math.log2(x), h1_p_chastota) 
entropia_h1_p_final = sum(list(entropia_h1_p))
nadlysh_h1_p = 1 - (entropia_h1_p_final / math.log2(alfavit_p))
print("Ентропія H1 з пробілами:",entropia_h1_p_final,' \nНадлишковість:',nadlysh_h1_p)

entropia_h1 = map(lambda x: -x * math.log2(x), h1_chastota) 
entropia_h1_final = sum(list(entropia_h1))
nadlysh_h1= 1 - (entropia_h1_final / math.log2(alfavit))
print("Ентропія H1 без пробів:",entropia_h1_final,'  \nНадлишковість:',nadlysh_h1)

entropia_h2_p = map(lambda y: -y * math.log2(y), h2_chastota_first_p) 
entropia_h2_first_final_p = sum(list(entropia_h2_p)) / 2
nadlysh_h2_first_p = 1 - (entropia_h2_first_final_p / math.log2(alfavit_p))
print("Ентропія H2 з пробілами :",entropia_h2_first_final_p,'  \nНадлишковість:',nadlysh_h2_first_p)

entropia_h2_first = map(lambda x: -x * math.log2(x), h2_chastota_first) 
entropia_h2_first_final = sum(list(entropia_h2_first)) / 2
nadlysh_h2_first = 1 - (entropia_h2_first_final / math.log2(alfavit))
print("Ентропія H2 без пробілів :",entropia_h2_first_final,'  \nНадлишковість:',nadlysh_h2_first)

entropia_h2_second_p = map(lambda y: -y * math.log2(y), h2_chastota_second_p) 
entropia_h2_second_final_p = sum(list(entropia_h2_second_p)) / 2
nadlysh_h2_second_p = 1 - (entropia_h2_second_final_p / math.log2(alfavit_p))
print("Ентропія H2 з пробілами_крк2:",entropia_h2_second_final_p,'  \nНадлишковість:',nadlysh_h2_second_p)

entropia_h2_second = map(lambda x: -x * math.log2(x), h2_chastota_second) 
entropia_h2_second_final = sum(list(entropia_h2_second)) / 2
nadlysh_h2_second = 1 - (entropia_h2_second_final / math.log2(alfavit))
print("Ентропія H2 без пробілів_крк2:",entropia_h2_second_final,'  \nНадлишковість:',nadlysh_h2_second)
 

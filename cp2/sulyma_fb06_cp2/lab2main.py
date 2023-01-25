from collections import Counter
from io import open

x = open('data.txt', 'r', encoding='utf-8')
data = x.read()
x.close()
data = data.lower()
data = ' '.join(data.split())

no_space_alphabet = 'абвгдежзийклмнопрстуфхцчщъыьэюя'
text = ''
y = ['за', 'нер', 'гром', 'чинов', 'ойквартире', 'иласовсеммо', 'черезпорогвт', 'старухинаквар', 'этотнемецтепер', 'жестианеизмедив', 'толькооднастарух', 'зщелиприедегосвид', 'ечахнесмотрянажару', 'нилвстарухинукварти', 'человекпереступилчер']

for i in data:
    if i in no_space_alphabet:
        text = text + i

x = open('text.txt', 'w', encoding='utf-8')
x.write(text)
x.close()


def encryption(data, key):
    newtext = ''
    for i in range(len(data)):
        n = no_space_alphabet.find(data[i])
        k = no_space_alphabet.find(key[i % len(key)])
        newtext = newtext + no_space_alphabet[(n + k) % len(no_space_alphabet)]
    return newtext


for i in range(len(y)):
    x = open('r' + str(len(y[i])) + '.txt', 'w', encoding='utf-8')
    x.write(encryption(text, y[i]))
    x.close()


#x = open('ciphertext.txt', 'r', encoding='utf-8')
#ciphertext = x.read()
#x.close()

def index(data):
    counter = Counter(data)
    n = 0
    for i in counter:
        counter[i] = counter[i] / len(data)
        n = n + counter[i]**2
    return n


for i in range(15):
    x = open('r' + str(len(y[i])) + '.txt', 'r', encoding='utf-8')
    data = x.read()
    x.close()
    x = open('index.txt', 'a', encoding='utf-8')
    x.write('index' + ' r' + str(len(y[i])) + ' = ' + str(index(data)) + '\n')
    x.close()

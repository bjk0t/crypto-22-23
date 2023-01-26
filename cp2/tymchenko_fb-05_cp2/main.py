from itertools import cycle

o = open('fable.txt', 'r', encoding='utf-8')
text1 = o.read()
k = open('var8.txt', 'r', encoding='utf-8')
var8=k.read()

alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

keys = ['ро', 'выа','пара','рлапр','макпаойцук','прйцитмьваполимсчван']

def encode(text, key):
    f = lambda arg: alph[(alph.index(arg[0])+alph.index(arg[1])%32)%32]
    return ''.join(map(f, zip(text, cycle(key))))



def decode(deсodedtext, key):
    f = lambda arg: alph[alph.index(arg[0])-alph.index(arg[1])%32]
    return ''.join(map(f, zip(deсodedtext, cycle(key))))



def coincidence_index(text):

    index = 0
    for i in range(len(alph)):
        iter = text.count(alph[i])
        index += iter * (iter - 1)
    index *= 1/(len(text)*(len(text)-1))

    return index



def main(text):

    for key in keys:
        encoded = encode(text, key)
        indices = coincidence_index(encoded)
        open_text = coincidence_index(text)
        print("Довжина ключа = ", len(key))
        print("Зашифрований текст -", encoded)
        print("Індекс відповідності -", indices,"\n")
    print("Індекс відповідності відкритого тексту",open_text,"\n")

main(text1)



def blocks(text, length):

        start_block = []
        for element in range(length):
            start_block.append(text[element::length])
        return start_block

def indices_of_blocks(text, size):
        index = 0
        start_block = blocks(text, size)

        for element in range(len(start_block)):
            index = index + coincidence_index(start_block[element])
        index = index / len(start_block)

        return index

for x in range(1,len(alph)):
    indices2 = str(indices_of_blocks(var8,x))
    x = str(x)
    print('Довжина ключа '+ x + ' - ' + indices2)



def getKey(text, size, letter):

    block = blocks(text, size)
    key = ""
    for element in range(len(block)):
        frequent = max(block[element], key=lambda count_: block[element].count(count_))
        key += alph[(alph.index(frequent) - alph.index(letter)) % len(alph)]

    return key


for letter in 'оеаитнслвр':
    print(getKey(var8, 20, letter))
print(decode(var8,'улановсеребряныепули'))




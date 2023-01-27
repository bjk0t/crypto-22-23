import pandas as pd

with open("text.txt", encoding='utf-8') as f:
    text = f.read().replace("\n", "")

Letters = [chr(i) for i in range(ord('а'), ord('я')+1)]

def ToNum(t):
    return [Letters.index(i) for i in t]

def ToLet(t):
    return ''.join([Letters[i] for i in t])

def ToBlock(text, lenBlock):
    blocks = [text[i] for i in range(lenBlock)]
    for j in range(lenBlock, len(text)):
        blocks[j%lenBlock] += text[j]
    return blocks

def Index(text):
    s = sum(text.count(i)*(text.count(i)-1) for i in Letters)
    index = (1/(len(text)*(len(text)-1))) * s
    return index

def SumIndex(list):
    return sum(Index(i) for i in list)/len(list)

def get_key(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key

def find_key_len():
    I_teor = 0.055
    indexes = {i: SumIndex(ToBlock(text, i)) for i in range(2,32)}
    pd.DataFrame(indexes, index=["index"]).to_excel("indexes.xlsx")
    keys = [index for index in indexes.values() if index > I_teor]
    lenKey = get_key(min(keys), indexes)
    return lenKey

KeyLen = find_key_len()
print("Довжина ключа: ", KeyLen)

freq_letters = ['о', 'е', 'а']

def fr(text):
    freq = {i: text.count(i)/len(text) for i in text}
    k = dict(sorted(freq.items()))
    return k

def key_search(blocks):
    Y_list = [get_key(max(fr(block).values()), fr(block)) for block in blocks]
    keys = [(Letters.index(i) - Letters.index(freq_letters[0]))% len(Letters) for i in Y_list]
    final_key = ToLet(keys)
    return final_key

print('Отриманий ключ - ', key_search(ToBlock(text, KeyLen)))
print('Змістовний ключ - делолисоборотней')


def VigenerD(text,key):
    text = ToNum(text)
    key = ToNum(key)
    PairsLet = {}
    iter = 0
    NumL = 0

    for i in text:
        PairsLet[NumL] = [i, key[iter]]
        NumL += 1
        iter += 1
        if (iter >= len(key)):
            iter = 0
    
    l = []
    for v in PairsLet:
        go = (PairsLet[v][0] - PairsLet[v][1] + len(PairsLet))%32
        l.append(go)
    DecText = ToLet(l)  
    return DecText
print(VigenerD(text, 'делолисоборотней'))

f = open('deciphered.txt', 'w')
f.write(VigenerD(text, 'делолисоборотней'))
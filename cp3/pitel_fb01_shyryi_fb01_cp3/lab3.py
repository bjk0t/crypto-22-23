from collections import Counter
with open("text.txt", 'r', encoding="utf-8") as file:
    text = file.read()

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']


text = text.replace(' ', '').replace('ъ', 'ь').replace('ё', 'е').replace('.', '').replace(',', '').replace('-', '').replace('\n','').lower()

def remove(list):
    new = []
    for i in list:
        if i not in new:
            new.append(i)
    return new

def gcd(a, b):
    if (b == 0):
        return a
    return gcd(b, a % b)

def func(a, b):
    if (b == 0):
        d = [a, 1, 0]
        return d
    else:
        d = func(b, a % b)
        y = d[1]
        x = d[2]
    #    print(a,b)
        return (d[0], x, y - (a // b) * x)

def revers(a, b):
    if (gcd(a, b)!= 1):
        return None
    else:
        return func(a, b)[1]

def line(a, b, n):
    if (gcd(a, n) == 1):
        #print('1')
        h = revers(a, n)  # h це наше а у -1 степень
        return (h * b) % n
    elif (gcd(a, n) > 1):
       # print('2')
        d = gcd(a, n)
        if (b % d == 0):  # то у нас всё хорошо, gcd(a,n) это наше d
            h1 = revers(a / d, n / d)
            x0 = (h1 * b / d) % (n / d)
            i = 0
            l = []
            while i < d:
                l.append(x0 + i * n / d)
                i = i + 1
            return l
        else:
            return 'Error!'

def bigram(text):#возвращает 5 самых популярных биграмм текста OK
    bigram = []
    for j in range(0, len(text) - 1):
        bigram.append(text[j] + text[j + 1])
    #bigramcount = dict(Counter(bigram))  # проверка правильности подсчёта биграм
    #print(bigramcount)
    temp = Counter(bigram).most_common(5) #самые популярные биграммы
    temp=[temp[0][0],temp[1][0],temp[2][0],temp[3][0],temp[4][0]]
    #print(temp)
    print("\n\n\n 5 найпоширеніших біграм у тексті - ", temp)
    return temp

def encrypt(a,b,text):#работает ок
    i = 0
    Cipher_text = ''
    while i < len(text) - 1:
        X = alphabet.index(text[i]) * 31 + alphabet.index(text[i + 1])
        D = (a*X+b)%(31*31)
        y2 = D%31
        y1 = (D - y2) // 31
        Cipher_text = Cipher_text + alphabet[y1] + alphabet[y2]
        i += 2
    return Cipher_text

def decrypt(a,b,text):#работает ок
    i=0
    Plain_text = ''
    while i<len(text)-1:
        Y = alphabet.index(text[i]) * 31 + alphabet.index(text[i + 1])
        a1 = revers(a, 31*31)
        D = (a1*(Y-b)) % (31*31)
        x2 = D % 31
        x1 = (D-x2)//31
        Plain_text = Plain_text+alphabet[x1] + alphabet[x2]
        i += 2
    return Plain_text

def all_possible(bigrams):#ОК
    rus_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    #print(bigrams, rus_bigrams)
    combinations = []
    for i in bigrams:
        for j in rus_bigrams:
            for x in bigrams:
                if x != i:
                    for k in rus_bigrams:
                        if k != j:
                            combinations.append([[i, j], [x, k]])
    #print(combinations)
    return combinations

def keys(bigrams):#работает ок
    all_keys=[]
   # print(bigrams)
    for i in bigrams:
        y1 = alphabet.index(i[0][0][0]) * 31 + alphabet.index(i[0][0][1])  # считаю биграммы
        x1 = alphabet.index(i[0][1][0]) * 31 + alphabet.index(i[0][1][1])
        y2 = alphabet.index(i[1][0][0]) * 31 + alphabet.index(i[1][0][1])
        x2 = alphabet.index(i[1][1][0]) * 31 + alphabet.index(i[1][1][1])
        # print(i) # проверка правильности определения
        #print(y1, x1, y2, x2)
        a = line((x2 - x1), (y2 - y1), 31 * 31)
        if a == 'Error!':
            continue
        if type(a) == list:
            for i in a:
                b = (y1 - i * x1) % (31 * 31)
                if i != int(i) or i <= 0 or gcd(i, 31 * 31) != 1 or i >= 31 * 31 or b < 0 or b >= 31 * 31:
                    continue
                all_keys.append([int(i), int(b)])
        elif type(a) == int:
            b = (y1 - a * x1) % (31 * 31)
            if a != int(a) or a <= 0 or gcd(a, 31 * 31) != 1 or a >= 31 * 31 or b < 0 or b >= 31 * 31:
                continue
            all_keys.append([int(a), int(b)])
        else:
            print('Error, a = ', a)
    all_keys = remove(all_keys)
    return all_keys

def true_keys(keys,text):#ищу ключи от шифротекста ОК
    most = []
    for i in keys:
       # print(i,i[0],i[1])
        a = i[0]
        b = i[1]
        plain_text = decrypt(a, b, text)
        #print(plain_text)
        temp = Counter(plain_text).most_common(3)
        temp = [temp[0][0], temp[1][0], temp[2][0]]
        temp1 = Counter(plain_text).most_common()[:-4:-1]
        temp1 = [temp1[0][0], temp1[1][0], temp1[2][0]]
        for j in temp:
            if j in ['о', 'а', 'е']:
                for k in temp1:
                    if k in ['ф', 'щ', 'ь']:
                        l = str(i[0]) + ' ' + str(i[1])
                        most.append(l)
                        #print(l)
    a = Counter(most).most_common(3)
    list = []
    for i in a:
        list.append([int(i[0].split(' ')[0]),  int(i[0].split(' ')[1])])
    print("Ключ від ШТ, k = [a, b] = ", list[0], "\n\n")
    ki = 0
    for i in list:
        a = i[0]
        b = i[1]
        plain_text = decrypt(a, b, text)
        
        if ki == 0:
            print("Розшифрований текст : \n", plain_text)
            ki = ki + 1




kk =keys(all_possible(bigram(text)))
true_keys(kk, text)

print('\n Хм, ;)  текст схожий на слова з твору "Накануне" автора Івана Сергійовича Тургенева\n')

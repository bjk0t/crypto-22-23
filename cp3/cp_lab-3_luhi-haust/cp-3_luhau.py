import collections
import numpy as np

print ('Криптографія')
print ("Комп'ютерний практикум №3")
print ('Криптоаналіз афінної біграмної підстановки')
print ('Виконали: Лугінін Богдан та Хаустович Артем')
print ('Перевірила: Байденко П. В.')
print ('Waiting...')
print ('Start')
print("\n", '-----------------------------------', "\n")

#під'єднаємо наші файлики до програмки

with open("/home/kali/cr3/04.txt", 'r', encoding='utf-8') as ofile:
	note = ofile.read()
	note = note.replace("\n","")

symbols = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
populare_bigrams = ['ст','но','то','на','ен']

def gcd(num1, num2):
    if num2 == 0:
        return abs(num1)
    return gcd(num2, num1%num2)

def evkl(a, b): #розширений алгоритм евкліда
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = evkl(b, a % b)
        return d, y, x - y * (a // b)
        
def obern(a, b): #обернене 
    if (gcd(a, b)!= 1):
        return None
    else:
    	d, x, y = evkl(b, a % b)
    	return y
    	
    	
def rivne(a, b, n): #знайти а з рівняння афінного шифру
    sp = []
    if (gcd(a, n) == 1):
        o = obern(a, n)   #обернене до а
        sp.append((o * b) % n)
    elif (gcd(a, n) > 1):
        d = gcd(a, n)
        if (b % d == 0):  
            o_1 = obern(a / d, n / d)
            x_0 = (o_1 * b / d) % (n / d)
            i = 0
            while i < d:
                sp.append(x_0 + i * n / d)
                i = i + 1
        else:
            sp.append(-1)  
    return sp
       
    
def bigram(text):
	bigram_cross = []
	for i in range(0, len(text)-2, 2):
		bigram_cross.append(text[i]+text[i+1])
	return bigram_cross

def frequency(text): #5 найчастіших біграм тексту
	bigram1 = bigram(text)
	bg_q = dict(collections.Counter(bigram1))
	period = {l: bg_q[l] / len(bigram1) for l in bg_q}
	speriod =  sorted(period, key=lambda l: period[l], reverse=1 )
	pop_bigram = []
	for i in range(0,5):
    		pop_bigram.append(speriod[i])
	return pop_bigram

def bg_index(bg): #переведення біграми у індекс
    index = symbols.index(bg[0])*31 + symbols.index(bg[1])
    return index

def index_tobg(n): #переведення індексу в біграму
	y = n%31
	x = (n-y)//31
	bg = ''
	bg+=(symbols[x]+symbols[y])
	return bg

pb = frequency(note)


def all_bg(): #всі можливі пари біграм
    pary = []
    for i in pb:
        for j in populare_bigrams:
            for x in pb:
                if x != i:
                    for y in populare_bigrams:
                        if y != j:
                            pary.append([[i, j], [x, y]])            
    return pary
 

def kluchi(bigrams): #всі можливі ключі
    kluch=[]
    #d=list()
    #print(bigrams)
    for i in bigrams:
        y1, x1 = bg_index(i[0][0]), bg_index(i[0][1]) 
        y2, x2 = bg_index(i[1][0]), bg_index(i[1][1])
        #print(y1, x1, y2, x2)
        a = rivne((x2 - x1), (y2 - y1), pow(len(symbols),2))
        #d.append(a)
        if a == -1 :
            continue
        for i in a:
                b = (y1 - i * x1) % pow(len(symbols),2)
                if i != int(i) or i <= 0 or gcd(i, pow(len(symbols),2)) != 1 or b < 0:
                    continue
                kluch.append([int(i), int(b)])    
    #print(kluch)
    #print(np.unique(d))
    return kluch


def rozshyfr(text, a, b):
	a_1 = obern(a,pow(len(symbols),2))
	vt = ''
	bigr = []
	for i in range(0, len(text) - 2, 2):
		bigr.append(text[i] + text[i + 1])
	for j in bigr:
		x_i = ( a_1 * (bg_index(j) - b) ) % pow(len(symbols),2)
		vt+=index_tobg(x_i)
	return vt
	
def perevirka(text):
	if (text.count('о')/len(text) < 0.095 or text.count('а')/len(text) < 0.065):
		return False
	if (text.count('ф')/len(text) > 0.004 or text.count('щ')/len(text) > 0.005):
		return False
	return True

	
print('------------------------------------*Реалізація*------------------------------------')
print(pb)
keys = kluchi(all_bg())
r=[]
[r.append(x) for x in keys if x not in r]
#print(r)
print("Amount of keys:",len(r))
print("-------------------*Keys*--------------------")
for k in r:
    vt = rozshyfr(note, k[0], k[1])
    if perevirka(vt):
        print(str(k))

print("-------------------*Text*--------------------")
print(rozshyfr(note, 390, 10))


    


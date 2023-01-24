import random


def GCD(a, b):
    if (b == 0):
        return a
    return GCD(b, a % b)


def extended_euclid(a, b):
        if (b == 0):
            return a, 1, 0
        
        d, x, y = extended_euclid(b, a % b)
        return d, y, x - (a // b) * y


def inverse_modulo(a, b):
    if (GCD(a, b) != 1):
        return None
    
    return extended_euclid(a, b)[1]


def horners_method(x, a, n):
    aBinary = bin(a)[2:][::-1]
    listOfSquares = [x]
    for i in range(1, len(aBinary)):
        listOfSquares.append((listOfSquares[i-1]**2) % n)
    multiplicationOfSquares = 1
    for i in range(len(aBinary)):
        if aBinary[i] == '1':
            multiplicationOfSquares = (multiplicationOfSquares * listOfSquares[i]) % n
    return multiplicationOfSquares


s = 0
d = 0
def decomposition(number):
    if ((number) // 2) % 2 == 0:
        number = (number) // 2
        global s
        global d
        s+= 1
        decomposition(number)
    
    else:
        d = (number) // 2
        s+= 1


def generate_simple_number():
    isSimpleNumber = 0
    simpleNumbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    
    while isSimpleNumber == 0:
        isSimpleNumber = 1     
        p = int(random.getrandbits(256))
        print("Можливе просте число: \n", p)
        print('______________________________________\n') 
        
        for simpleNumber in simpleNumbers:
            if p % simpleNumber == 0:
                isSimpleNumber = 0
                continue
        
        #Крок 0
        decomposition(p - 1)
        
        #Крок 1
        for k in range(8):
            x = random.randint(2, p - 1)
            
            if GCD(x, p) > 1:
                isSimpleNumber = 0
                break
            
            #Крок 2.1
            hornResult = horners_method(x, d, p)
            if hornResult == 1 or hornResult == p - 1:
                continue
            
            #Крок 2.2
            else:
                for i in range(1, s):
                    x = horners_method(x, 2, p)
                    
                    if x == p - 1:
                        isSimpleNumber = 1
                        break
                    
                    elif x == 1:
                        isSimpleNumber = 0
                        break
                    
                    isSimpleNumber = 0
    return p



def generate_key_pair():
    keys = []
    
    for i in range(4):
        keys.append(generate_simple_number())
    
    keys.sort()
    return keys


def generate_e_and_d(p, q):
    euler = (p - 1) * (q - 1)
    e = 2 ** 16 + 1
    d = inverse_modulo(e, euler) % euler
    return e, d


secretKeyA = []
openKeyA = []
secretKeyB = []
openKeyB = []


def deploy_rsa():
    p, q, p1, q1 = generate_key_pair()
    print('p = ', p)
    print('______________________________________\n') 
    print('q = ', q)
    print('______________________________________\n') 
    print('p1 = ', p1)
    print('______________________________________\n') 
    print('q1 = ', q1)
    print('______________________________________\n') 
    n = p * q
    e, d = generate_e_and_d(p, q)
    e1, d1 = generate_e_and_d(p1, q1)
    n1 = p1 * q1
    print('n = ', n)
    print('______________________________________\n') 
    print('e = e1 = ', e)
    print('______________________________________\n') 
    print('n1 = ', n1)
    print('______________________________________\n') 
    openKeyA.extend([n, e])
    secretKeyA.extend([p, q, d])
    openKeyB.extend([n1, e1])
    secretKeyB.extend([p1, q1, d1])

    

def encrypt(m, e, n):
    return horners_method(m, e, n)


def decrypt(c, d, n):
    return horners_method(c, d, n)


def sign(plaintext, d, e1, n1, n):
    S = horners_method(plaintext, d, n)
    S1 = horners_method(S, e1, n1)
    ciphertext = encrypt(plaintext, e1, n1)
    return ciphertext, S1


def verify(ciphertext, S1, d1, n1, e, n):
    S = decrypt(S1, d1, n1)
    plaintext = decrypt(ciphertext, d1, n1)
    authentication = horners_method(S, e, n)
    
    if plaintext == authentication:
        print("Автентифікація пройшла успішно")
    else:
        print("Помилка під час автентифікації")
    return plaintext


deploy_rsa()
print("Секретний ключ абонента A: ", secretKeyA[2])
print('______________________________________\n') 
print("Відкритий ключ абонента A: ", openKeyA)
print('______________________________________\n') 
print("Секретний ключ абонента B: ", secretKeyB[2])
print('______________________________________\n') 
print("Відкритий ключ абонента B: ", openKeyB)
print('______________________________________\n') 
plaintext = random.randint(0, openKeyA[0] - 1)
print("Відкритий текст: ", plaintext)
print('______________________________________\n') 
ciphertext, SS1 = sign(plaintext, secretKeyA[2], openKeyB[1], openKeyB[0],  openKeyA[0])
print("Зашифрований текст: ", ciphertext)
print('______________________________________\n') 
verify(ciphertext, SS1, secretKeyB[2], openKeyB[0], openKeyA[1], openKeyA[0])
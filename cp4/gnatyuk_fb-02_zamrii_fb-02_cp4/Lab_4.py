from random import randint
import math

#Generate random number
def Gen_random_number():
    number = randint(((2**255) + 1), ((2**256) - 1))
    while not Miller_Rabin(number):
        number = randint(((2**255) + 1), ((2**256) - 1))
    return number


#Miller-Rabin test
def Miller_Rabin(rand):
    Pr_Num_List = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    counter, lk = 0, rand - 1
    if 0 in list(map(lambda x: rand % x, Pr_Num_List)): return False
    if rand == 2: return True
    while lk % 2 == 0:
        counter = counter + 1
        lk = lk // 2
    for i in range(1000):
        x = rand-1
        n = randint(2, x)
        k = pow(n, lk, rand)

        if k == x or k == 1: continue
        c = counter - 1
        for j in range(c):
            b = pow(k, 2)
            k = b % rand
            if k == x: break
        else: return False
    return True



def GenerateKeyPair(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = randint(2, phi_n)
    while math.gcd(e, phi_n) != 1:
        e = randint(2, phi_n)
    d = pow(e, -1, phi_n)
    return (d, p, q), (n, e)

def Encrypt(item, n, e):
    return pow(item, e, n)

def Decrypt(encrypt, d, p, q):
    return pow(encrypt, d, p * q)

def Sign(item, d, p, q):
    return pow(item, d, p * q)

def Verify(item, s, Key2):
    n = Key2[0]
    e = Key2[1]
    if pow(s, e, n) == item: return True

def RecieveKey(EncMsg, sign, Key2, Key1):
    d = Key1[0]
    p = Key1[1]
    q = Key1[2]
    if Verify(Decrypt(EncMsg, d, p, q), sign, Key2): return Decrypt(EncMsg, d, p, q)

def SendKey(item, Key2, Key1):
    n = Key2[0]
    e = Key2[1]
    d = Key1[0]
    p = Key1[1]
    q = Key1[2]
    return Encrypt(item, n, e), Sign(item, d, p, q)
text = 'Hooray, we are done it!'
print('🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻')
print('Text to encrypt: ', text)
print('🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻')

item = 6937922844103314290512452137955752102268078293860840481
def From_Inreger(msg):
    return bytes.fromhex(hex(msg)[2:]).decode('ASCII')
msg = From_Inreger(6937922844103314290512452137955752102268078293860840481)



p, q, p1, q1 = Gen_random_number(), Gen_random_number(), Gen_random_number(), Gen_random_number()
while p1*q1<p*q:
    p, q = Gen_random_number(), Gen_random_number()

RSA_A = GenerateKeyPair(p, q)
RSA_B = GenerateKeyPair(p1, q1)
print('')
print('🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻')
print('p and q find for abonent A and abonent B')
print('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
print('For abonent A')
print('p:', p)
print('q:', q)
print('For abonent B')
print('p1:', p1)
print('q1:', q1)
print('🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻')

Encrypt_item, signature = SendKey(item, RSA_B[1], RSA_A[0])
print('Encrypt_item: ', Encrypt_item)
print('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
print('Text to int:', RecieveKey(Encrypt_item, signature, RSA_A[1], RSA_B[0]))
print('------------------------------------------------------------------------------------------------------------------------------------------------------------------')
print('The message received by subscriber B: ', msg)
print('🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻🔺🔻')







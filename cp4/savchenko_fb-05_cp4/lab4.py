import random

def gen_prim(len_p):
    p = random.randrange(int(2**(len_p-1)), int(2**len_p))
    while not is_prime(p):
        p = random.randrange(int(2**(len_p-1)), int(2**len_p))
    return p

def is_prime(n, k=4):
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_two_pair():
    while True:
        keys = [(gen_prim(256), gen_prim(256)), (gen_prim(256), gen_prim(256))]
        if (keys[0][0]*keys[0][1]<=keys[1][0]*keys[1][1]):
            return keys


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inv(a, m):
    g, x, _ = extended_euclid(a, m)
    if g != 1:
        return False
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m


def extended_euclid(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, y, x = extended_euclid(b, a % b)
        return (g, x, y - (a//b)*x)


def rsa_gen_key(p, q):
    n = p*q
    oi = (p-1)*(q-1)
    while True:
        e = random.randrange(2, oi)
        while not (gcd(e, oi)):
            e = random(2, oi)
        d = mod_inv(e, oi)
        if d:
            break
    return ((e, n), (d, p, q))

def Encrypt(m, pub_key):
    (e, n) = pub_key
    c = pow(m, e, n)
    return c

def Decrypt(c, sec_key):
    (d, p, q) = sec_key
    m =  pow(c, d, p*q)
    return m

def Sign(text, sec_key):
    (d, p, q) = sec_key
    s = pow(text, d, p*q)
    return (text, s)

def Verify(sig_text, pub_key):
    (e, n) = pub_key
    (text, s) = sig_text
    if pow(s, e, n) == text:
        return True
    else:
        return False

def SendKey(k, key_a, open_key_b):
    _, s = Sign(k, key_a[1])
    s1 = Encrypt(s, open_key_b)
    k1 = Encrypt(k, open_key_b)
    return k1, s1


def ReceiveKey(r_k, key_b, open_key_a):
    (k1, s1) = r_k
    k = Decrypt(k1, key_b[1])
    s = Decrypt(s1, key_b[1])
    return Verify((k, s), open_key_a)



    

# p_pair = gen_two_pair()
# print("p = " + str(p_pair[0][0]))
# print("q = " + str(p_pair[0][1]))
# print("p1 = " + str(p_pair[1][0]))
# print("q1 = " + str(p_pair[1][1]))
print("========================================================================")
p_pair = [
    [
        96461904010644145815056134002109100188233814667859705403760289267209968487171,
        67836484867032579895555977474809008008402137806270827977469114918298828181999
    ],
    [
        104599226489937365286746720599879809914658043025933087234726124778379279925851,
        83855362685772713535351725362007282424132200413075315847016749708743567646243
    ]
]

# key_a = rsa_gen_key(p_pair[0][0], p_pair[0][1])
# key_b = rsa_gen_key(p_pair[1][0], p_pair[1][1])

# print("Dlya A")
# print("e = " + str(key_a[0][0]))
# print("n = " + str(key_a[0][1]))
# print("d = " + str(key_a[1][0]))
# print("p = " + str(key_a[1][1]))
# print("q = " + str(key_a[1][2]))
# print("Dlya B")
# print("e = " + str(key_b[0][0]))
# print("n = " + str(key_b[0][1]))
# print("d = " + str(key_b[1][0]))
# print("p = " + str(key_b[1][1]))
# print("q = " + str(key_b[1][2]))

key_a = [
    [
        1286703187130306547411584022937342928579376175667791652733057844072551243967857574640280108978148112178607385018442839217700486312418173269599624675595571,
        6543636491663210923262994325949724193420476654657570522201719242781130797694906503367433311507935809093404378533223754059877160338819514523009390284634829
    ],
    [
        1674832595352593078357870084825849886626005282155600700036560852460166161921488965964935664642952779496747703269379217494818388830240265665261956441317191,
        96461904010644145815056134002109100188233814667859705403760289267209968487171,
        67836484867032579895555977474809008008402137806270827977469114918298828181999
    ]
]

key_b = [
    [
        3729987443220244214247463398815233288821137123839120487457072700787954034885560336891095924483582897829600959018572425946696242389492272146867698549240933,
        8771206073964982507149570623899445520020906584868332149226622176972242559689799879472089066782191573537772647116117311465277677167005467092294247638727793
    ],
    [
        5170491599282747278183166900796686568093857572649585638798361513209743126261110004445232215369590222096030861896920955578902051101826446117727789239499397,
        104599226489937365286746720599879809914658043025933087234726124778379279925851,
        83855362685772713535351725362007282424132200413075315847016749708743567646243
    ]
]

message = 2184177184939192293246173556898914585115086776689114285231284257074523364114733245197023224581804199886656220946035970851004286993403266077687782759057322
h_message = hex(message)[2:]
h_e = hex(key_a[0][0])[2:]
h_n = hex(key_a[0][1])[2:]
c_message = Encrypt(message, key_a[0])
# print(h_message)
# print(h_e)
# print(h_n)
# print("==========================")
# print(c_message)
# print("==========================")
# print(hex(c_message)[2:])

d_message = Decrypt(c_message, key_a[1])
# print (d_message)
# print("==========================")
# print (hex(d_message)[2:])

sign_message = Sign(message, key_a[1])
# print (sign_message[1])
# print(Verify(sign_message, key_a[0]))
# print(Verify(sign_message, key_b[0]))

k = 2481650355533096972177972895618997361984905643871087799614217012101111927059789788217719335856475553461418506314992162487950999365752660655142630791743192

key_message = SendKey(k, key_a, key_b[0])
print(ReceiveKey(key_message, key_b, key_a[0]))

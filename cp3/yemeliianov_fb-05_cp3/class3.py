import collections
import re
from itertools import product, groupby
class Class_for_Bigram:
    def __init__(self):
        self.alpha = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
        self.clearString = self.c_f("text.txt")

    
    def extended_euclid(self,a, b):
        if (b == 0):
            return a, 1, 0
        d, x, y = self.extended_euclid(b, a % b)
        return d, y, x - (a // b) * y
    def GCD(self,a, b):
        if (b == 0):
            return a
        return self.GCD(b, a % b)
    def inverse_modulo(self,a, b):
        if (self.GCD(a, b) != 1):
            return None
        return self.extended_euclid(a, b)[1]
    def c_f(self,f):
        f = open(f, mode="r", encoding="utf-8").read().replace("\n", "").replace('ё', 'е').replace('ъ', 'ь').lower()
        clearString = re.sub(r'[\W\s]+|[\d]+|_+', '', f).strip()
        return clearString
    def calc_linear_equation(self,a, b, m):
        if (self.GCD(a, m) == 1):
            aInversed = self.inverse_modulo(a, m)
            return (aInversed * b) % m
        elif (self.GCD(a, m) > 1):
            d = self.GCD(a, m)
            if (b % d == 0):
                a1 = a / d
                b1 = b / d
                m1 = m / d
                a1Inversed = self.inverse_modulo(a1, m1)
                x0 = (a1Inversed * b1) % (m1)
                solutions = []
                i = 0
                while i < d:
                    solutions.append(x0 + i * m1)
                    i += 1
                return solutions
            return "R_n_m_r"
    def find_frequent_bigrams(self,string):
        bigrams = []
        for letter in range(0, len(string) - 2, 2):
            bigrams.append(string[letter] + string[letter + 1])
        bigramsAmount = dict(collections.Counter(bigrams))
        mFB = collections.Counter(bigramsAmount).most_common(5)
        print(mFB)
        return [mFB[0][0],
                mFB[1][0],
                mFB[2][0],
                mFB[3][0],
                mFB[4][0]]
    def bigrams_comparison(self,bigrams):
        frequentTerroristBigrams = ['ст', 'но', 'то', 'на', 'ен']
        combinations = []
        for i, j, n, k in product(bigrams, frequentTerroristBigrams, bigrams, frequentTerroristBigrams):
            if n != i and j != k:
                combinations.append([[i, j], [n, k]])
        return combinations
    def find_possible_keys(self,bigrams):
        allKeys = []
        m = 31
        for letters in bigrams:
            Y1 = self.alpha.index(letters[0][0][0]) * m + self.alpha.index(letters[0][0][1])
            X1 = self.alpha.index(letters[0][1][0]) * m + self.alpha.index(letters[0][1][1])
            Y2 = self.alpha.index(letters[1][0][0]) * m + self.alpha.index(letters[1][0][1])
            X2 = self.alpha.index(letters[1][1][0]) * m + self.alpha.index(letters[1][1][1])

            a = self.calc_linear_equation((X1 - X2), (Y1 - Y2), m ** 2)
            if a == "R_n_m_r":
                continue
            elif type(a) == list:
                for i in a:
                    b = (Y1 - i * X1) % (m ** 2)
                    if self.GCD(i, m ** 2) != 1:
                        continue
                    allKeys.append([int(i), int(b)])
            elif type(a) == int:
                b = (Y1 - a * X1) % (m ** 2)
                if self.GCD(a, m ** 2) != 1:
                    continue
                allKeys.append([int(a), int(b)])
        allKeys.sort()
        allKeys = list(i for i, _ in groupby(allKeys))
        return allKeys
    def decode(self,a, b, ciphertext):
        m = 31
        plaintext = ''
        for letter in range(0, len(ciphertext) - 2, 2):
            Y = self.alpha.index(ciphertext[letter]) * m + self.alpha.index(ciphertext[letter + 1])
            a1 = self.inverse_modulo(a, m ** 2)
            X = (a1 * (Y - b)) % (m ** 2)
            x2 = X % m
            x1 = (X - x2) // m
            plaintext = plaintext + self.alpha[x1] + self.alpha[x2]
        return plaintext
    def correct_keys(self,keys, text):
        frequentTerroristLetter = ['о', 'а', 'е']
        unrealBigrams = ['аь', 'уь', 'яь', 'юь', 'еь', 'оь', 'йь', 'ыь', 'иь', 'эь']
        keyVariants = []

        for key in keys:
            a = key[0]
            b = key[1]
            plainText = self.decode(a, b, text)
            bigrams = [plainText[i] + plainText[i + 1] for i in range(len(plainText) - 1)]
            if all(bigram not in unrealBigrams for bigram in bigrams):
                mostFrequentLetters = [letter[0] for letter in collections.Counter(plainText).most_common(6)]
                if all(letter in mostFrequentLetters for letter in frequentTerroristLetter):
                    keyVariants.append(key)
        print(keyVariants)
        print(self.decode(keyVariants[0][0], keyVariants[0][1], self.clearString))
        f=open('answer.txt', 'w')
        f.write(str(self.decode(keyVariants[0][0], keyVariants[0][1], self.clearString)))

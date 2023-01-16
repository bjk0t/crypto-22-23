import collections
class Text:
    def __init__(self, file_name):
        self.note = self.r_T(file_name)
        self.symbols = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                        'у', 'ф', 'х',
                        'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
        self.populare_bgs = ['на', 'но', 'об', 'нн', 'ен']

    def r_T(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as ofile:
            note = ofile.read()
            note = note.replace("\n", "")
        return note
    def gcd(self, num1, num2):
        return num1 if num2 == 0 else self.gcd(num2, num1 % num2)
    def evkl(self, a, b):
        if b == 0:
            return a, 1, 0
        else:
            d, x, y = self.evkl(b, a % b)
            return d, y, x - y * (a // b)
    def obratn(self, a, b):
        if (self.gcd(a, b) != 1):
            return None
        else:
            d, x, y = self.evkl(b, a % b)
            return y
    def srav(self, a, b, n):
        sp = []
        if self.gcd(a, n) == 1:
            sp.append((self.obratn(a, n) * b) % n)
        elif self.gcd(a, n) > 1 and b % self.gcd(a, n) == 0:
            for i in range(self.gcd(a, n)):
                sp.append((self.obratn(a / self.gcd(a, n), n / self.gcd(a, n)) * b / self.gcd(a, n) + i * n / self.gcd(a,
                                                                                                                      n)) % (
                                      n / self.gcd(a, n)))
        else:
            sp.append(-1)
        return sp
    def bg(self, text):
        return [text[i] + text[i + 1] for i in range(0, len(text) - 2, 2)]
    def frequency(self, text):
        bg1 = self.bg(text)
        bg_q = collections.Counter(bg1)
        speriod = sorted(bg_q, key=lambda l: bg_q[l], reverse=1)
        pop_bg = speriod[:5]
        return pop_bg
    def bg_index(self, bg):
        index = self.symbols.index(bg[0]) * 31 + self.symbols.index(bg[1])
        return index
    def index_tobg(self, n): 
        y = n % 31
        x = (n - y) // 31
        bg = ''
        bg += (self.symbols[x] + self.symbols[y])
        return bg
    def all_bg(self):
        pary = []
        for i in self.pb:
            for j in self.populare_bgs:
                for x, y in [(x, y) for x in self.pb if x != i for y in self.populare_bgs if y != j]:
                    pary.append([[i, j], [x, y]])
        return pary
    def kluchi(self, bgs):
        kluch = []
        for i in bgs:
            y1, x1 = self.bg_index(i[0][0]), self.bg_index(i[0][1])
            y2, x2 = self.bg_index(i[1][0]), self.bg_index(i[1][1])
            a = self.srav((x2 - x1), (y2 - y1), pow(len(self.symbols), 2))
            if a == -1:
                continue
            for i in a:
                b = (y1 - i * x1) % pow(len(self.symbols), 2)
                if i != int(i) or i <= 0 or self.gcd(i, pow(len(self.symbols), 2)) != 1 or b < 0:
                    continue
                kluch.append([int(i), int(b)])
        return kluch
    def rozshyfr(self, text, a, b):
        a_1 = self.obratn(a, pow(len(self.symbols), 2))
        vt = ''
        for i in range(0, len(text) - 1, 2):
            x_i = (a_1 * (self.bg_index(text[i] + text[i + 1]) - b)) % pow(len(self.symbols), 2)
            vt += self.index_tobg(x_i)
        return vt
    def perevirka(self, text):
        if (text.count('о') / len(text) < 0.095 or text.count('а') / len(text) < 0.065):
            return False
        if (text.count('ф') / len(text) > 0.004 or text.count('щ') / len(text) > 0.005):
            return False
        return True
    def main(self):
        self.pb = self.frequency(self.note)
        keys = self.kluchi(self.all_bg())
        r = []
        [r.append(x) for x in keys if x not in r]
        print("Keys all:", len(r))
        print("Ключ")
        for k in r:
            vt = self.rozshyfr(self.note, k[0], k[1])
            if self.perevirka(vt):
                print(str(k))
        print("Текст")
        print(self.rozshyfr(self.note, 27, 211))
        print( self.populare_bgs)
text = Text("02.txt")
text.main()
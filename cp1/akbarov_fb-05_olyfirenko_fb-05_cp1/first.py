import math
from collections import Counter
class Text:
    def __init__(self, path):
        self.path = path
        self.alphabet = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
                         "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я", " "]
        self._probel = []
        self._say_no_to_probel = []
        self.load_file()
    def load_file(self):
        with open(self.path, 'r', encoding='UTF-8') as f:
            file = f.read()
            file = file.lower()
            file.replace("ё", "е").replace("ъ", "ь")
            prbl = False
            for i in range(len(file)):
                if file[i] in self.alphabet:
                    if file[i] == " ":
                        if prbl == True:continue
                        else:
                            self._probel.append(" ")
                            prbl = True
                    else:
                        self._probel.append(file[i])
                        self._say_no_to_probel.append(file[i])
                        prbl = False
                else:
                    if prbl == False:
                        self._probel.append(" ")
                        prbl = True

    @staticmethod
    def redundancy_checkon(n, m):
        return 1 - (n / math.log(m, 2))

    def entropy_bigr(self, txt, touch_point):
        distance = len(txt)
        if distance % 2 == 1 and touch_point == 0:
            distance -= 1
        bigr = []
        for i in range(0, distance - 1, 2 - touch_point):
            bigr.append(txt[i] + txt[i + 1])
        count = len(bigr)
        frequency = Counter(bigr)
        for i in frequency:
            frequency[i] /= count
        result = sum(frequency[k] * math.log(frequency[k], 2) for k in frequency) / (-2)
        frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
        for key, value in frequency:
            print(key, ':', value)
        print("Redundancy", self.redundancy_checkon(result, len(''.join(set(txt)))))
        return result
    def entropy_lett(self, txt):
        distance = len(txt)
        frequency = Counter(txt)
        for i in frequency:
            frequency[i] /= distance
        result = -1 * sum(frequency[k] * math.log(frequency[k], 2) for k in frequency)
        frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
        for key, value in frequency:
            print(key, ':', value)
        print("Redundancy", self.redundancy_checkon(result, len(frequency)))
        return result
    def show_entropy(self):
        print("H2 з пробілами без", self.entropy_bigr(self._probel, 0))
        print("H1 з пробілами з", self.entropy_bigr(self._probel, 1))
        print("H2 без пробілами без", self.entropy_bigr(self._say_no_to_probel, 0))
        print("H1 без пробілами з", self.entropy_bigr(self._say_no_to_probel, 1))
        print("letters з пробілами", self.entropy_lett(self._probel))
        print("letters без пробілами", self.entropy_lett(self._say_no_to_probel))

text = Text("text.txt")
text.show_entropy()

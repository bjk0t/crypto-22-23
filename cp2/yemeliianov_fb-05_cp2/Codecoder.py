from itertools import cycle
class cp:
    ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    KEY_LIST = ['аб', 'ира', 'сома', 'писар', 'здукящуаубцыхыгхж']
    LETTERS = 'оеаитнслвр'

    def __init__(self):
        self.text1, self.text2 = self.r_f()
        self.data = {}
        for key in self.KEY_LIST:
            encoded_text = self.e_d(self.text1, key)
            self.data[len(key)] = [key + ' : ' + ''.join(encoded_text)]

    @staticmethod
    def r_f():
        with open('text_to_code.txt', 'r', encoding='utf-8') as file1:
            text1 = file1.read()
        with open('text_to_decode.txt', 'r', encoding='utf-8') as file2:
            text2 = file2.read()
        return text1, text2
    @staticmethod
    def e_d(our_text, key):
        result = lambda argument: cp.ALPHABET[
            (cp.ALPHABET.index(argument[0]) + cp.ALPHABET.index(argument[1]) % 32) % 32]
        return ''.join(map(result, zip(our_text, cycle(key))))

    @staticmethod
    def decode_data(de_coded_text, key):
        result = lambda argument: cp.ALPHABET[
            (cp.ALPHABET.index(argument[0]) - cp.ALPHABET.index(argument[1]) % 32) % 32]
        return ''.join(map(result, zip(de_coded_text, cycle(key))))

    @staticmethod
    def c_i(our_text):
        index = 0
        length = len(our_text)
        for i in range(len(cp.ALPHABET)):
            count_letter = our_text.count(cp.ALPHABET[i])
            index += count_letter * (count_letter - 1)
        index *= 1 / (length * (length - 1))
        return index

    def f_t(self):
        print("\nІндекс відповідності = ", self.c_i(self.text1), "\n")
        for key in self.KEY_LIST:
            print("Довжина ключа = ", len(key))
            encoded_text = self.e_d(self.text1, key)
            print("- Зашифрований текст: ", encoded_text)
            print("- Розшифрований текст: ", self.decode_data(encoded_text, key))
            print("Індекс відповідності: ", self.c_i(encoded_text), "\n")

    @staticmethod
    def split_blocks(our_text, length):
        our_block = []
        for i in range(length):
            our_block.append(our_text[i::length])
        return our_block

    @staticmethod
    def each_index_block(our_text, size):
        our_block = cp.split_blocks(our_text, size)
        index = 0
        for i in range(len(our_block)):
            index += cp.c_i(our_block[i])
        index /= len(our_block)
        return index

    def print_blocks_index(self):
        for i in range(1, len(cp.ALPHABET)):
            print('Довжина ключа=' + str(i) + ' => Індекс відповідності=' + str(self.each_index_block(self.text2, i)))

    @staticmethod
    def creation_key(our_text, size, letter):
        our_block = cp.split_blocks(our_text, size)
        key = ""
        for i in range(len(our_block)):
            frequent = max(our_block[i], key=lambda count_: our_block[i].count(count_))  # выводич что чаще всего используется
            key += cp.ALPHABET[
                (cp.ALPHABET.index(frequent) - cp.ALPHABET.index(letter)) % len(cp.ALPHABET)]
        return key

    def main(self):
        for letter in self.LETTERS:
            print(self.creation_key(self.text2, 17, letter))
        print("\n")
        decoded_text = self.decode_data(self.text2, 'возвращениеджинна')
        print("Зашифрований текст: ", self.text2)
        print("Розшифрований текст: ", decoded_text)
        with open(f'fin_text.txt', 'w', encoding='UTF-8') as f:
            f.write(decoded_text)

from itertools import cycle
class Cipher:
    def __init__(self):
        self.ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        self.key_list = ['аб', 'ира', 'сома', 'писар', 'рнарпнгоир', 'рнпыогиртны', 'рнйгыяхзгрпм', 'вдзхьзужбъгяш',
                    'квххсьпириуктж', 'ннвпосшайфздомн', 'жшпеиезэщфчбщнзй', 'здукящуаубцыхыгхж', 'юпйсимяяшяшзломмзш',
                    'щыййгскфвэслнуьрсхщ', 'зцюрйонпхбяжткщсюсцъ']
        self.text1, self.text2 = self.read_files()
        self.data = {}
        for key in self.key_list:
            encoded_text = self.encode_data(self.text1, key)
            self.data[len(key)] = [key + ' : ' + ''.join(encoded_text)]

    def read_files(self):
        with open('text_to_test.txt', 'r', encoding='utf-8') as file1:
            text1 = file1.read()
        with open('text_to_decode.txt', 'r', encoding='utf-8') as file2:
            text2 = file2.read()
        return text1, text2

    def encode_data(self, our_text, key):
        result = lambda argument: self.ALPHABET[(self.ALPHABET.index(argument[0]) + self.ALPHABET.index(argument[1]) % 32) % 32]
        return ''.join(map(result, zip(our_text, cycle(key))))

    def decode_data(self, de_coded_text, key):
        result = lambda argument: self.ALPHABET[(self.ALPHABET.index(argument[0]) - self.ALPHABET.index(argument[1]) % 32) % 32]
        return ''.join(map(result, zip(de_coded_text, cycle(key))))

    def coincidence_index(self, our_text):
        index = 0
        length = len(our_text)
        for i in range(len(self.ALPHABET)):
            count_letter = our_text.count(self.ALPHABET[i])
            index += count_letter * (count_letter - 1)
        index *= 1 / (length * (length - 1))
        return index

    def first_task(self):
        print("\nІндекс совпадения start = ", self.coincidence_index(self.text1), "\n")
        for key in self.key_list:
            print("Длина ключа = ", len(key))
            encoded_text = self.encode_data(self.text1, key)
            print("- Зашифрованный текст: ", encoded_text)
            print("- Расшифрованный текст: ", self.decode_data(encoded_text, key))
            print("Индекс совпадения: ", self.coincidence_index(encoded_text), "\n")


    def split_blocks(self, our_text, length):
        our_block = []
        for i in range(length):
            our_block.append(our_text[i::length])
        return our_block

    def each_index_block(self, our_text, size):
        our_block = self.split_blocks(our_text, size)
        index = 0
        for i in range(len(our_block)):
            index += self.coincidence_index(our_block[i])
        index /= len(our_block)
        return index

    def print_blocks_index(self):
        for i in range(1, len(self.ALPHABET)):
            print('Длина ключа=' + str(i) + ' => Индекс совпадения=' + str(self.each_index_block(self.text2, i)))

    def creation_key(self, our_text, size, letter):
        our_block = self.split_blocks(our_text, size)
        key = ""
        for i in range(len(our_block)):
            frequent = max(our_block[i], key=lambda count_: our_block[i].count(count_))  # выводич что чаще всего используется
            key += self.ALPHABET[(self.ALPHABET.index(frequent) - self.ALPHABET.index(letter)) % len(self.ALPHABET)]
        return key

    def main(self):
        for letter in 'оеаитнслвр':
            print(self.creation_key(self.text2, 14, letter))
        print("\n")
        decoded_text = self.decode_data(self.text2, 'последнийдозор')  # жосвеыдиадозор - тут становится понятно какой ключ
        print("Зашифрованный текст: ", self.text2)
        print("Расшифрованный текст: ", decoded_text)
        with open(f'vid.txt', 'w', encoding='UTF-8') as f:
            f.write(decoded_text)

if __name__ == '__main__':
    cipher = Cipher()
    cipher.first_task()
    cipher.print_blocks_index()
    cipher.main()
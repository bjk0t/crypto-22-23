import string
from collections import Counter

with open("task3.txt", "r", encoding='utf-8', errors='ignore') as f:
    text = f.read()


def coincidence_index(text):
    letter_counts = Counter(text)
    n = len(text)
    if len(text) < 2:
        return 0.0
    IC = 0
    for count in letter_counts.values():
        IC += count * (count - 1)
    IC = IC / (n * (n - 1))
    return IC
    

def block_text(text, len_key):
    blocks = []
    for i in range(0, len_key):
        blocks.append(text[i::len_key])
    return blocks

def find_coincidence_index(ciphertext):
    cis = {}
    for len_key in range(2, 32):
        ci = 0
        blocks = block_text(ciphertext, len_key)

        for block in blocks:
            ci += coincidence_index(block)
        ci /= len_key
        cis[len_key] = ci
        #print(f"for {len_key} = " + str(cis[len_key]))
    return cis


def frequency_letter(text):
    text = text.lower()
    letter_counts = {}
    for letter in text:
        if letter.isalpha():
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
    total_letters = sum(letter_counts.values())
    letter_freqs = {letter: count/total_letters for letter,
                    count in letter_counts.items()}
    return letter_freqs

def find_key(ciphertext, len_key, common_chars):
    output = {}
    ciphertext_int = [ord(i) for i in ciphertext]
    blocks = block_text(ciphertext, len_key)
    for letter in common_chars:
        result = ""
        shift = ord(letter)
        for block in blocks:
            most_letter = max(frequency_letter(block), key=frequency_letter(block).get)
            result += chr((ord(most_letter) - shift) % 32 + ord('а'))
        output[letter] = result
    return output


def decrypt_vigenere(ciphertext, key):
    plaintext = ""
    key_len = len(key)
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            shift = ord(key[i % key_len].upper()) - ord('а')
            char = chr((ord(char) - shift - ord('а')) % 32 + ord('а'))
        plaintext += char
    return plaintext

    


# print(coincidence_index(text))

common_chars = "оеиант" # вычислили это в первой лабе
#print("Results:", find_coincidence_index(text))
#print(find_key(text, 17, common_chars))
text_res = decrypt_vigenere(text, "войнамагаэндшпиль")

print(text_res)


with open("task3_res.txt", "w", encoding='utf-8') as f:
    f.write(f"Наш ключик \"войнамагаэндшпиль\" и исходный текст:\n" + text_res)



# print(decrypt_vigenere(text, 17))

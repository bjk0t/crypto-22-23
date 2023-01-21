from collections import Counter

def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.lower()
    plaintext_filtered = ""
    for letter in plaintext:
        if letter.isalpha():
            plaintext_filtered += letter
    
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    plaintext_int = [ord(i) for i in plaintext_filtered]
    ciphertext = ''
    for i in range(len(plaintext_int)):
        shift = key_as_int[i % key_length]
        ciphertext += chr((plaintext_int[i] + shift) % 32 + ord('а'))
    return ciphertext


def coincidence_index(text):
    letter_counts = Counter(text)
    n = len(text)
    IC = 0
    for count in letter_counts.values():
        IC += count * (count - 1)
    IC = IC / (n * (n - 1))
    return IC



with open("text.txt", "r", encoding='utf-8', errors='ignore') as f:
    text = f.read()

key = input("Натыкай ключик для шифровки: ")

ciphertext = vigenere_encrypt(text, key)
ic = coincidence_index(ciphertext)

with open(key+".txt", "w", encoding='utf-8') as f:
    f.write(f"Наш ключик \"{key}\" и шифртекст:\n" + ciphertext +
            "\nА так же индекс соответсвия: " + str(ic))

print("А вот и наш зашифрованый текст:\n" + ciphertext)
print("А ещё не забудь посмотреть на индекс соответсвия: " + str(ic))

meow_ic = coincidence_index(text)
print("А тут я видимо проспал что нужно сделать: " + str(meow_ic))

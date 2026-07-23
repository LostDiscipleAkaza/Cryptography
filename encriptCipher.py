alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

plaintext = input("Enter name (CAPITAL LETTERS): ")
key = int(input("Enter key: "))

ciphertext = ""

for ch in plaintext:
    if ch in alphabet:
        x = alphabet.index(ch)
        y = (x + key) % 26
        ciphertext += alphabet[y]
    else:
        ciphertext += ch

print("Cipher Text:", ciphertext)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

plaintext = input("Enter Plaintext: ")
key = int(input("Enter Key: "))

ciphertext = ""

for ch in plaintext:
    if ch in alphabet:
        x = alphabet.index(ch)

        if x < 26:                  # Uppercase letters
            y = (x + key) % 26
        else:                       # Lowercase letters
            y = 26 + ((x - 26 + key) % 26)

        ciphertext += alphabet[y]
    else:
        ciphertext += ch

print("Cipher Text:", ciphertext)

def encrypt(text, key):
    result = ""
 
    for ch in text.upper():
        if ch.isalpha():
            result += chr((ord(ch) - 65 + key) % 26 + 65)
        else:
            result += ch
    return result
 
 
def decrypt(text, key):
    return encrypt(text, -key)
 
 
text = input("Enter message: ")
key = int(input("Enter key: "))
 
cipher = encrypt(text, key)
print("Encrypted:", cipher)
print("Decrypted:", decrypt(cipher, key))

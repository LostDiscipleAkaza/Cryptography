def encrypt(text, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
 
    for ch in text.upper():
        if ch.isalpha():
            result += key[alphabet.index(ch)]
        else:
            result += ch
    return result
 
 
def decrypt(text, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
 
    for ch in text.upper():
        if ch.isalpha():
            result += alphabet[key.index(ch)]
        else:
            result += ch
    return result
 
key = "QWERTYUIOPASDFGHJKLZXCVBNM"
text = input("Enter message: ")
 
cipher = encrypt(text, key)
print("Encrypted:", cipher)
print("Decrypted:", decrypt(cipher, key))

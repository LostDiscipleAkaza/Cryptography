def columnar_encrypt(text, key):
    text = text.replace(" ", "")
    n = len(key)
 
    while len(text) % n != 0:
        text += "X"
 
    rows = [text[i:i+n] for i in range(0, len(text), n)]
    order = sorted(range(n), key=lambda x: key[x])
 
    result = ""
 
    for col in order:
        for row in rows:
            result += row[col]
 
    return result
 
 
def columnar_decrypt(cipher, key):
    n = len(key)
    rows = len(cipher) // n
    order = sorted(range(n), key=lambda x: key[x])
 
    matrix = [[""] * n for _ in range(rows)]
    index = 0
 
    for col in order:
        for row in range(rows):
            matrix[row][col] = cipher[index]
            index += 1
 
    result = ""
 
    for row in matrix:
        result += "".join(row)
 
    return result
 
 
text = input("Enter message: ")
key1 = input("Enter first key: ")
key2 = input("Enter second key: ")
 
step1 = columnar_encrypt(text.upper(), key1.upper())
cipher = columnar_encrypt(step1, key2.upper())
 
print("Encrypted:", cipher)
 
step1 = columnar_decrypt(cipher, key2.upper())
plain = columnar_decrypt(step1, key1.upper())
 
print("Decrypted:", plain)

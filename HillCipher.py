import math
 
def inverse_matrix(key):
    a, b = key[0]
    c, d = key[1]
 
    det = (a * d - b * c) % 26
 
    if math.gcd(det, 26) != 1:
        return None
 
    inv_det = pow(det, -1, 26)
 
    return [
        [(d * inv_det) % 26, (-b * inv_det) % 26],
        [(-c * inv_det) % 26, (a * inv_det) % 26]
    ]
 
 
def process(text, key):
    result = ""
    text = text.upper().replace(" ", "")
 
    if len(text) % 2 != 0:
        text += "X"
 
    for i in range(0, len(text), 2):
        x = ord(text[i]) - 65
        y = ord(text[i + 1]) - 65
 
        a = (key[0][0] * x + key[0][1] * y) % 26
        b = (key[1][0] * x + key[1][1] * y) % 26
 
        result += chr(a + 65)
        result += chr(b + 65)
 
    return result
 
 
key = [[5, 3], [17, 9]]
text = input("Enter message: ")
 
cipher = process(text, key)
inverse = inverse_matrix(key)
plain = process(cipher, inverse)
 
print("Encrypted:", cipher)
print("Decrypted:", plain)

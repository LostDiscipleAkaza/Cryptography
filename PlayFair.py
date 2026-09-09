def create_matrix(key):
    key = key.upper().replace("J", "I")
    letters = ""
 
    for ch in key + "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if ch.isalpha() and ch not in letters:
            letters += ch
 
    return [letters[i:i+5] for i in range(0, 25, 5)]
 
 
def position(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j
 
 
def prepare(text):
    text = text.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())
 
    result = ""
    i = 0
 
    while i < len(text):
        a = text[i]
 
        if i + 1 == len(text):
            result += a + "X"
            i += 1
        elif text[i] == text[i + 1]:
            result += a + "X"
            i += 1
        else:
            result += a + text[i + 1]
            i += 2
 
    return result
 
 
def process(text, matrix, decrypt=False):
    result = ""
    shift = -1 if decrypt else 1
 
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
 
        r1, c1 = position(matrix, a)
        r2, c2 = position(matrix, b)
 
        if r1 == r2:
            result += matrix[r1][(c1 + shift) % 5]
            result += matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:
            result += matrix[(r1 + shift) % 5][c1]
            result += matrix[(r2 + shift) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]
 
    return result
 
 
key = input("Enter key: ")
text = input("Enter message: ")
 
matrix = create_matrix(key)
 
print("Matrix:")
for row in matrix:
    print(row)
 
prepared = prepare(text)
cipher = process(prepared, matrix)
plain = process(cipher, matrix, True)
 
print("Encrypted:", cipher)
print("Decrypted:", plain)


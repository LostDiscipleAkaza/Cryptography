def encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    row = 0
    direction = 1
 
    for ch in text:
        fence[row].append(ch)
 
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
 
        row += direction
 
    return "".join("".join(row) for row in fence)
 
 
def decrypt(cipher, rails):
    pattern = []
    row = 0
    direction = 1
 
    for i in range(len(cipher)):
        pattern.append(row)
 
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1
 
        row += direction
 
    result = [""] * len(cipher)
    index = 0
 
    for r in range(rails):
        for i in range(len(cipher)):
            if pattern[i] == r:
                result[i] = cipher[index]
                index += 1
 
    return "".join(result)
 
 
text = input("Enter message: ")
rails = int(input("Enter number of rails: "))
 
cipher = encrypt(text, rails)
print("Encrypted:", cipher)
print("Decrypted:", decrypt(cipher, rails))

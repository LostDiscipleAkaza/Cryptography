import hashlib

# User inputs
p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))
g = int(input("Enter generator g: "))
x = int(input("Enter private key x: "))
k = int(input("Enter nonce k: "))
m = input("Enter message: ")

# Key generation
y = pow(g, x, p)
print("Public key:", y)

# Signature generation
r = pow(g, k, p)
e = int(hashlib.sha256((str(r) + m).encode()).hexdigest(), 16) % q
s = (k + x * e) % q

print("Signature (e, s):", e, s)

# Signature verification
v = (pow(g, s, p) * pow(y, -e, p)) % p
e2 = int(hashlib.sha256((str(v) + m).encode()).hexdigest(), 16) % q

if e == e2:
    print("Signature is VALID")
else:
    print("Signature is INVALID")

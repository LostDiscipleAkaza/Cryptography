"""DSS using the ElGamal signature scheme, implemented from scratch."""
import sys
import hashlib
from math import gcd


# Public parameters: 512-bit safe prime p (p = 2q + 1) and generator g = 2
P = int("9e2bb78dbe15c1bd03684275217375fa645e49e7babea380e83f8246a57296e1"
        "0a684b308679218c54ad57004d053a82c9b0d022c42e5a715c5f8767eaff0eab", 16)
G = 2


def h(data):
    # Message digest H(m) as an integer (SHA-256)
    return int.from_bytes(hashlib.sha256(data).digest(), "big")


def derive(key_text, label):
    # Deterministic number in [2, P-2] derived from the key text
    return int.from_bytes(hashlib.sha512(label + key_text.encode()).digest(),
                          "big") % (P - 3) + 2


def key_generation(key_text):
    x = derive(key_text, b"private")      # private key
    y = pow(G, x, P)                      # public key y = g^x mod p
    return x, y


def sign(message, x, key_text):
    m = h(message)
    k = derive(key_text, b"nonce")        # per-message secret, gcd(k, p-1) = 1
    while gcd(k, P - 1) != 1:
        k += 1
    r = pow(G, k, P)                      # r = g^k mod p
    s = (pow(k, -1, P - 1) * (m - x * r)) % (P - 1)   # s = k^-1 (m - xr)
    return m, k, r, s


def verify(message, r, s, y):
    if not (0 < r < P):
        return False
    m = h(message)
    v1 = pow(G, m, P)                     # g^m mod p
    v2 = (pow(y, r, P) * pow(r, s, P)) % P  # y^r * r^s mod p
    return v1 == v2


if __name__ == "__main__":
    message = b"GITAMUNIVERSITYISDEEMEDTOBEUNIVERSITY"
    key = sys.argv[1] if len(sys.argv) > 1 else input("Enter key: ")
    x, y = key_generation(key)
    m, k, r, s = sign(message, x, key)
    print("Input      :", message.decode())
    print("Key        :", key)
    print("Hash H(m)  :", format(m, "064X"))
    print("Private x  :", format(x, "X"))
    print("Public y   :", format(y, "X"))
    print("Signature r:", format(r, "X"))
    print("Signature s:", format(s, "X"))
    ok = verify(message, r, s, y)
    print("Verify     :", "VALID" if ok else "INVALID")
    bad = verify(message + b"X", r, s, y)
    print("Tampered   :", "VALID" if bad else "INVALID")

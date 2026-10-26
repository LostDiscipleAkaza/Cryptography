"""DSS (Digital Signature Algorithm, FIPS 186-4) implemented from scratch."""

import sys
import random
import hashlib

L, N = 2048, 256          # sizes of p and q in bits (FIPS 186-4: L=2048, N=256)

# ======================= Prime generation =======================
SMALL_PRIMES = [p for p in range(2, 2000) if all(p % d for d in range(2, int(p ** 0.5) + 1))]

def is_prime(n, rng, rounds=40):
    # Miller-Rabin probabilistic primality test
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gen_prime(bits, rng):
    while True:
        c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(c, rng):
            return c

# ======================= Domain parameters (p, q, g) =======================
def generate_parameters(seed="GITAM-DSS"):
    rng = random.Random(seed)                  # fixed seed -> same p, q, g every run
    q = gen_prime(N, rng)                      # N-bit prime
    while True:
        X = rng.getrandbits(L) | (1 << (L - 1))
        p = X - (X % (2 * q) - 1)              # p = 1 (mod 2q)
        if p.bit_length() == L and is_prime(p, rng):
            break
    h = 2
    while pow(h, (p - 1) // q, p) == 1:        # g = h^((p-1)/q) mod p, g > 1
        h += 1
    g = pow(h, (p - 1) // q, p)
    return p, q, g

# ======================= Keys =======================
def hash_int(data):
    return int.from_bytes(hashlib.sha256(data).digest(), "big")

def generate_keys(key_text, p, q, g):
    x = hash_int(key_text.encode()) % (q - 1) + 1     # private key, 0 < x < q
    y = pow(g, x, p)                                  # public key  y = g^x mod p
    return x, y

# ======================= Sign / Verify =======================
def sign(message, x, p, q, g):
    z = hash_int(message)                             # z = leftmost N bits of H(m)
    ctr = 0
    while True:
        # per-message secret k (deterministic here so the output is repeatable)
        k = hash_int(x.to_bytes(32, "big") + z.to_bytes(32, "big") + bytes([ctr])) % (q - 1) + 1
        r = pow(g, k, p) % q                          # r = (g^k mod p) mod q
        s = pow(k, -1, q) * (z + x * r) % q           # s = k^-1 (z + x*r) mod q
        if r != 0 and s != 0:
            return r, s
        ctr += 1

def verify(message, r, s, y, p, q, g):
    if not (0 < r < q and 0 < s < q):
        return False
    z = hash_int(message)
    w = pow(s, -1, q)                                 # w  = s^-1 mod q
    u1 = z * w % q                                    # u1 = z*w mod q
    u2 = r * w % q                                    # u2 = r*w mod q
    v = (pow(g, u1, p) * pow(y, u2, p) % p) % q       # v  = ((g^u1 * y^u2) mod p) mod q
    return v == r

if __name__ == "__main__":
    message = b"GITAMUNIVERSITYISDEEMEDTOBEUNIVERSITY"
    key = sys.argv[1] if len(sys.argv) > 1 else input("Enter key: ")
    p, q, g = generate_parameters()
    x, y = generate_keys(key, p, q, g)
    r, s = sign(message, x, p, q, g)
    print("Input      :", message.decode())
    print("Key        :", key)
    print("q (256-bit):", format(q, "X"))
    print("Public y   :", format(y, "X")[:64] + "...")
    print("Hash       :", hashlib.sha256(message).hexdigest().upper())
    print("Signature r:", format(r, "064X"))
    print("Signature s:", format(s, "064X"))
    print("Verify     :", "VALID" if verify(message, r, s, y, p, q, g) else "INVALID")
    tampered = b"GITAMUNIVERSITYISDEEMEDTOBEUNIVERSITx"
    print("Tampered   :", "VALID" if verify(tampered, r, s, y, p, q, g) else "INVALID")

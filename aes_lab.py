"""AES-128 (ECB) implemented from scratch."""
import sys

# ======================= AES-128 =======================
def build_sbox():
    # Generate the AES S-box from GF(2^8) inverse + affine transform
    def xtime(a):
        a <<= 1
        return (a ^ 0x11B) & 0xFF if a & 0x100 else a
    def gmul(a, b):
        r = 0
        while b:
            if b & 1:
                r ^= a
            a = xtime(a)
            b >>= 1
        return r
    sbox = [0] * 256
    for x in range(256):
        inv = 0
        if x:
            for y in range(1, 256):
                if gmul(x, y) == 1:
                    inv = y
                    break
        s = inv
        for i in range(1, 5):
            s ^= ((inv << i) | (inv >> (8 - i))) & 0xFF
        sbox[x] = s ^ 0x63
    return sbox, gmul

SBOX, gmul = build_sbox()
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def prepare_key(key_text):
    k = key_text.encode()[:16]
    return k.ljust(16, b"\x00")            # zero-pad key to 16 bytes

def pkcs7_pad(data, size=16):
    n = size - len(data) % size
    return data + bytes([n]) * n

def key_expansion(key):
    w = [list(key[4 * i:4 * i + 4]) for i in range(4)]
    for i in range(4, 44):
        t = w[i - 1][:]
        if i % 4 == 0:
            t = t[1:] + t[:1]                       # RotWord
            t = [SBOX[b] for b in t]                # SubWord
            t[0] ^= RCON[i // 4 - 1]                # Rcon
        w.append([w[i - 4][j] ^ t[j] for j in range(4)])
    return [sum(w[4 * r:4 * r + 4], []) for r in range(11)]   # 11 round keys

def add_round_key(s, rk):
    return [a ^ b for a, b in zip(s, rk)]

def sub_bytes(s):
    return [SBOX[b] for b in s]

def shift_rows(s):
    # state is column-major: index = 4*col + row
    return [s[4 * ((c + r) % 4) + r] for c in range(4) for r in range(4)]

def mix_columns(s):
    out = []
    for c in range(4):
        a = s[4 * c:4 * c + 4]
        out += [gmul(a[0], 2) ^ gmul(a[1], 3) ^ a[2] ^ a[3],
                a[0] ^ gmul(a[1], 2) ^ gmul(a[2], 3) ^ a[3],
                a[0] ^ a[1] ^ gmul(a[2], 2) ^ gmul(a[3], 3),
                gmul(a[0], 3) ^ a[1] ^ a[2] ^ gmul(a[3], 2)]
    return out

def aes_encrypt_block(block, round_keys):
    s = add_round_key(list(block), round_keys[0])
    for r in range(1, 10):
        s = add_round_key(mix_columns(shift_rows(sub_bytes(s))), round_keys[r])
    s = add_round_key(shift_rows(sub_bytes(s)), round_keys[10])
    return bytes(s)

def aes_encrypt(plaintext, key_text):
    rks = key_expansion(prepare_key(key_text))
    data = pkcs7_pad(plaintext)
    return b"".join(aes_encrypt_block(data[i:i + 16], rks)
                    for i in range(0, len(data), 16))


if __name__ == "__main__":
    plaintext = b"GITAMUNIVERSITYISDEEMEDTOBEUNIVERSITY"
    key = sys.argv[1] if len(sys.argv) > 1 else input("Enter key: ")
    ct = aes_encrypt(plaintext, key)
    print("Input      :", plaintext.decode())
    print("Key        :", key)
    print("Ciphertext :", ct.hex().upper())

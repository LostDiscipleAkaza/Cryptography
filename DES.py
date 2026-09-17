"""
des.py - DES block cipher (educational) with alphanumeric
string input/output for key and plaintext.
"""

# ---------- Permutation and selection tables (standard DES) ----------

IP = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25,
]

E = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1,
]

P = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4,
]

PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32,
]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]

# ---------- Bit helpers (bit 1 = most significant) ----------


def permute(value: int, table: list, in_bits: int) -> int:
    out = 0
    for bit in table:
        out = (out << 1) | ((value >> (in_bits - bit)) & 1)
    return out


def rotl28(value: int, n: int) -> int:
    value &= 0x0FFFFFFF
    return ((value << n) | (value >> (28 - n))) & 0x0FFFFFFF


def generate_subkeys(key: int) -> list:
    permuted = permute(key, PC1, 64)
    c = (permuted >> 28) & 0x0FFFFFFF
    d = permuted & 0x0FFFFFFF

    subkeys = []
    for shift in SHIFTS:
        c = rotl28(c, shift)
        d = rotl28(d, shift)
        cd = (c << 28) | d
        subkeys.append(permute(cd, PC2, 56))
    return subkeys


def feistel(r: int, subkey: int) -> int:
    expanded = permute(r, E, 32) ^ subkey
    sbox_out = 0
    for i in range(8):
        block = (expanded >> (42 - i * 6)) & 0x3F
        row = ((block & 0x20) >> 4) | (block & 0x01)
        col = (block >> 1) & 0x0F
        sbox_out = (sbox_out << 4) | S_BOXES[i][row][col]
    return permute(sbox_out, P, 32)


def des_crypt_block(block: int, subkeys: list, decrypt: bool = False) -> int:
    ip = permute(block, IP, 64)
    l_half = (ip >> 32) & 0xFFFFFFFF
    r_half = ip & 0xFFFFFFFF

    order = reversed(subkeys) if decrypt else subkeys
    for subkey in order:
        l_half, r_half = r_half, l_half ^ feistel(r_half, subkey)

    preoutput = (r_half << 32) | l_half
    return permute(preoutput, FP, 64)


class DES:
    def __init__(self, key: int):
        self.subkeys = generate_subkeys(key)

    def encrypt_block(self, plaintext: int) -> int:
        return des_crypt_block(plaintext, self.subkeys, decrypt=False)

    def decrypt_block(self, ciphertext: int) -> int:
        return des_crypt_block(ciphertext, self.subkeys, decrypt=True)


# ============================================================
#  NEW: string <-> block conversion, padding, and I/O handling
# ============================================================

BLOCK_SIZE = 8  # bytes (64 bits)


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")


def int_to_bytes(n: int, length: int = BLOCK_SIZE) -> bytes:
    return n.to_bytes(length, byteorder="big")


def normalize_key(key_str: str) -> int:
    """Convert a user-supplied alphanumeric key into a 64-bit integer.
    Pads with spaces if shorter than 8 chars, truncates if longer."""
    key_bytes = key_str.encode("utf-8")
    if len(key_bytes) < BLOCK_SIZE:
        key_bytes = key_bytes.ljust(BLOCK_SIZE, b" ")
    else:
        key_bytes = key_bytes[:BLOCK_SIZE]
    return bytes_to_int(key_bytes)


def pkcs5_pad(data: bytes) -> bytes:
    """Pad data to a multiple of BLOCK_SIZE using PKCS5/7 padding."""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len


def pkcs5_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]


def des_encrypt_text(plaintext_str: str, key_str: str) -> bytes:
    key_int = normalize_key(key_str)
    cipher = DES(key_int)

    padded = pkcs5_pad(plaintext_str.encode("utf-8"))
    ciphertext = b""
    for i in range(0, len(padded), BLOCK_SIZE):
        block = padded[i:i + BLOCK_SIZE]
        block_int = bytes_to_int(block)
        enc_int = cipher.encrypt_block(block_int)
        ciphertext += int_to_bytes(enc_int)
    return ciphertext


def des_decrypt_text(ciphertext: bytes, key_str: str) -> str:
    key_int = normalize_key(key_str)
    cipher = DES(key_int)

    plaintext = b""
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        block_int = bytes_to_int(block)
        dec_int = cipher.decrypt_block(block_int)
        plaintext += int_to_bytes(dec_int)
    return pkcs5_unpad(plaintext).decode("utf-8")


# ---------- Interactive driver ----------

if __name__ == "__main__":
    plaintext_input = input("Enter plaintext (alphanumeric): ")
    key_input = input("Enter key (up to 8 alphanumeric characters): ")

    ciphertext_bytes = des_encrypt_text(plaintext_input, key_input)
    print(f"Ciphertext (hex): {ciphertext_bytes.hex().upper()}")

    decrypted_text = des_decrypt_text(ciphertext_bytes, key_input)
    print(f"Decrypted text:   {decrypted_text}")
    print("Round-trip", "SUCCESS" if decrypted_text == plaintext_input else "FAILED")
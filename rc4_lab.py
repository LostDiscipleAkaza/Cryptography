"""RC4 stream cipher implemented from scratch."""
import sys

def rc4(data, key_text):
    key = key_text.encode()
    # Key Scheduling Algorithm (KSA)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)
    return bytes(out)

if __name__ == "__main__":
    plaintext = b"GITAMUNIVERSITYISDEEMEDTOBEUNIVERSITY"
    key = sys.argv[1] if len(sys.argv) > 1 else input("Enter key: ")
    ct = rc4(plaintext, key)
    print("Input      :", plaintext.decode())
    print("Key        :", key)
    print("Ciphertext :", ct.hex().upper())
    print("Decrypted  :", rc4(ct, key).decode())

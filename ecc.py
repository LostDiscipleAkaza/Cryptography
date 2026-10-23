from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

def main():
    print("=== Elliptic Curve Cryptography (ECDSA) Interactive Program ===")
    
    # 1. Generate private and public keys using SECP256R1
    print("\nGenerating private and public key pair...")
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    print("Keys generated successfully.")

    # 2. Get user input message to sign
    user_message = input("\nEnter the message you want to sign: ")
    message_bytes = user_message.encode('utf-8')

    # 3. Sign the message
    signature = private_key.sign(
        message_bytes,
        ec.ECDSA(hashes.SHA256())
    )
    print("\nMessage signed.")
    print(f"Signature (Hex): {signature.hex()}")

    # 4. Verify signature with original message
    verify_choice = input("\nVerify signature with original message? (y/n): ").strip().lower()
    if verify_choice == 'y':
        try:
            public_key.verify(
                signature,
                message_bytes,
                ec.ECDSA(hashes.SHA256())
            )
            print("Verification Result: SUCCESS. The signature is valid.")
        except InvalidSignature:
            print("Verification Result: FAILED. The signature is invalid.")

    # 5. Test verification with a modified message
    tamper_choice = input("\nTest verification with a tampered message? (y/n): ").strip().lower()
    if tamper_choice == 'y':
        tampered_message = message_bytes + b"_tampered"
        print(f"Tampered message: {tampered_message.decode('utf-8', errors='ignore')}")
        try:
            public_key.verify(
                signature,
                tampered_message,
                ec.ECDSA(hashes.SHA256())
            )
            print("Verification Result: SUCCESS. The signature is valid.")
        except InvalidSignature:
            print("Verification Result: FAILED. The signature is invalid.")

if __name__ == "__main__":
    main()

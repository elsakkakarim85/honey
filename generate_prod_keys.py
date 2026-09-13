import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

PRIVATE_KEY_FILE = ".apiary_private_key.pem"
PUBLIC_KEY_FILE = "apiary_public_key.pem"

def generate_prod_keys():
    print("Generating Production Ed25519 Cryptographic Keys...")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    print(f"Success! Private Key securely saved to {PRIVATE_KEY_FILE}")
    print(f"Public Key exported to {PUBLIC_KEY_FILE}")

if __name__ == "__main__":
    generate_prod_keys()

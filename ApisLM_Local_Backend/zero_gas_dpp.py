import os
import json
import base64
import hashlib
import qrcode
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

PRIVATE_KEY_FILE = "apiary_private_key.pem"
PUBLIC_KEY_FILE = "apiary_public_key.pem"

def generate_keypair():
    """Generates and saves persistent Ed25519 keys for the local apiary."""
    if os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE):
        print("Keys already exist. Loading...")
        with open(PRIVATE_KEY_FILE, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None
            )
        with open(PUBLIC_KEY_FILE, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        return private_key, public_key

    print("Generating new Ed25519 Keypair for Zero-Gas DPP...")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Save Private Key
    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save Public Key
    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    return private_key, public_key

def sign_payload(private_key, payload_dict: dict):
    """Hashes the payload via SHA-256 and signs it using Ed25519."""
    # Ensure consistent ordering for hashing
    payload_str = json.dumps(payload_dict, sort_keys=True, separators=(',', ':'))
    payload_bytes = payload_str.encode('utf-8')
    
    # SHA-256 Hash
    payload_hash = hashlib.sha256(payload_bytes).digest()
    
    # Ed25519 Signature
    signature = private_key.sign(payload_hash)
    
    # Base64 encode for URL transfer
    encoded_payload = base64.urlsafe_b64encode(payload_bytes).decode('utf-8')
    encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8')
    
    return encoded_payload, encoded_signature

def create_dpp_qrcode(payload_dict: dict):
    """Creates the GS1 Digital Link with Cryptographic Seal and outputs a QR code."""
    private_key, public_key = generate_keypair()
    
    encoded_payload, encoded_signature = sign_payload(private_key, payload_dict)
    
    # Extract public key as base64 for mobile verification demo
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pub_b64 = base64.urlsafe_b64encode(pub_bytes).decode('utf-8')
    
    # Construct GS1 Digital Link Mock
    gs1_link = f"https://apislm.local/dpp?p={encoded_payload}&s={encoded_signature}&pk={pub_b64}"
    
    print(f"Cryptographic Seal Generated. GS1 Link: {gs1_link}")
    
    # Generate QR Code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(gs1_link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("batch_qrcode.png")
    print("-> QR Code saved as batch_qrcode.png")
    
    return gs1_link

if __name__ == "__main__":
    honey_batch = {
        "weight_kg": 25.5,
        "harvest_date": "2026-08-27",
        "floral_source": "Wildflower & Clover",
        "foraging_score": 92
    }
    create_dpp_qrcode(honey_batch)

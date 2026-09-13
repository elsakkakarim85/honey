import pytest
import os
import json
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from zero_gas_dpp import sign_payload, generate_keypair, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE

@pytest.fixture
def fresh_keys():
    # Setup
    if os.path.exists(PRIVATE_KEY_FILE): os.remove(PRIVATE_KEY_FILE)
    if os.path.exists(PUBLIC_KEY_FILE): os.remove(PUBLIC_KEY_FILE)
    
    priv, pub = generate_keypair()
    yield priv, pub
    
    # Teardown
    if os.path.exists(PRIVATE_KEY_FILE): os.remove(PRIVATE_KEY_FILE)
    if os.path.exists(PUBLIC_KEY_FILE): os.remove(PUBLIC_KEY_FILE)

def test_dpp_signature_validity(fresh_keys):
    """Verify that a generated Zero-Gas DPP signature is mathematically valid."""
    private_key, public_key = fresh_keys
    
    payload = {"weight_kg": 10, "floral_source": "Lavender"}
    encoded_payload, encoded_sig = sign_payload(private_key, payload)
    
    # Decode
    payload_bytes = base64.urlsafe_b64decode(encoded_payload)
    sig_bytes = base64.urlsafe_b64decode(encoded_sig)
    
    # Re-hash and verify
    import hashlib
    payload_hash = hashlib.sha256(payload_bytes).digest()
    
    # Should not raise exception
    public_key.verify(sig_bytes, payload_hash)
    
def test_dpp_signature_forgery(fresh_keys):
    """Verify that altering the payload breaks the cryptographic seal."""
    private_key, public_key = fresh_keys
    
    payload = {"weight_kg": 10, "floral_source": "Lavender"}
    encoded_payload, encoded_sig = sign_payload(private_key, payload)
    
    sig_bytes = base64.urlsafe_b64decode(encoded_sig)
    
    # Forged payload
    forged_payload = {"weight_kg": 50, "floral_source": "Lavender"}
    forged_bytes = json.dumps(forged_payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
    import hashlib
    forged_hash = hashlib.sha256(forged_bytes).digest()
    
    from cryptography.exceptions import InvalidSignature
    with pytest.raises(InvalidSignature):
        public_key.verify(sig_bytes, forged_hash)

import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_agent_key() -> str:
    """Generate a random 256-bit AES key for an agent."""
    key = AESGCM.generate_key(bit_length=256)
    return base64.b64encode(key).decode('utf-8')

def encrypt_payload(key_str: str, data: bytes) -> str:
    """Encrypt payload using AES-GCM."""
    key = base64.b64decode(key_str.encode('utf-8'))
    aesgcm = AESGCM(key)
    # 96-bit (12 bytes) nonce is standard for AES-GCM
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    
    # Prepend the nonce to the ciphertext
    encrypted_data = nonce + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_payload(key_str: str, encrypted_payload: str) -> bytes:
    """Decrypt payload using AES-GCM."""
    key = base64.b64decode(key_str.encode('utf-8'))
    encrypted_data = base64.b64decode(encrypted_payload.encode('utf-8'))
    
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

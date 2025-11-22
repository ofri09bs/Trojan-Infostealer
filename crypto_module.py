from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

KEY = b"whereismymoney67"  # 16 bytes key for AES-128

backend = default_backend()

def encrypt_data(data_bytes: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    padded_data = padder.update(data_bytes) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(encrypted_data)


def decrypt_data(encrypted_data_b64: bytes) -> bytes:
    encrypted_data = base64.b64decode(encrypted_data_b64)

    cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypt_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypt_data
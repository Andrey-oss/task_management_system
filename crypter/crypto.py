'''Text Enc/Decrypter

Salt - uses for making secure key from given password

IV (Initialization Vector) - Adds entropy/randomization for encryption
Uses in AES-CBC, must have the same size as salt
'''

import os
import hashlib
import hmac
import base64
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class PasswordHasher:
    '''Password Encryptor'''

    def __init__(self, password):
        self.iterations = 260_000
        self.salt_length = 16
        self.algo = 'sha256'
        self.password = password

    def hash_password(self) -> str:
        '''Hash password with random salt'''

        salt = os.urandom(self.salt_length)
        hash_bytes = hashlib.pbkdf2_hmac(
            self.algo,
            self.password.encode(),
            salt,
            self.iterations
        )
        return f"{self.algo}${self.iterations}${base64.b64encode(salt).decode()}${base64.b64encode(hash_bytes).decode()}"

    def verify_password(self, hashed: str) -> bool:
        '''Verify password'''

        try:
            algo, iterations, salt_b64, hash_b64 = hashed.split('$')
            salt = base64.b64decode(salt_b64)
            stored_hash = base64.b64decode(hash_b64)

            new_hash = hashlib.pbkdf2_hmac(
                algo,
                self.password.encode(),
                salt,
                int(iterations)
            )
            return hmac.compare_digest(stored_hash, new_hash)
        except Exception as e:
            return False

class TextHasher:
    '''AES Encryptor'''

    def __init__(self, password):
        self.iterations = 100_000
        self.password = password.encode()

    def derive_key(self, salt) -> bytes:
        '''Generate key from password using salt'''

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
        )
        return kdf.derive(self.password)

    def encrypt(self, plaintext: str) -> str:
        '''Encrypt text'''

        salt = os.urandom(16)
        key = self.derive_key(salt)
        iv = os.urandom(16)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize() # ciphertext

        return base64.b64encode(salt + iv + ct).decode()

    def decrypt(self, token: str) -> str:
        '''Decrypt text'''

        data = base64.b64decode(token)
        salt = data[:16] # First 16 symbols is salt
        iv = data[16:32] # Between 16 and 32 Symbols inclusive is IV
        ct = data[32:] # The rest is text

        key = self.derive_key(salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ct) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode()

'''Text Enc/Decrypter

Salt - uses for making secure key from given password

IV (Initialization Vector) - Adds entropy/randomization for encryption
Uses in AES-CBC, must have the same size as salt
'''

import os
import base64
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class HandleText:
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

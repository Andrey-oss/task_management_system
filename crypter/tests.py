"""Tests for self-written crypto library"""

import base64
import unittest
import binascii
from crypter.crypto import PasswordHasher, CryptoText

class PasswordHasherTest(unittest.TestCase):
    """Test PasswordHasher class"""

    def test_hash_format(self):
        """
        Test for output hash format

        Output data should be: algo$iterations$salt$hash
        """

        hasher = PasswordHasher('mysecret')
        result = hasher.hash_password()

        parts = result.split('$')
        self.assertEqual(parts[0], 'sha256')
        self.assertEqual(parts[1], '260000')
        self.assertEqual(len(parts), 4)

        # Validate salt and hash with base64
        try:
            base64.b64decode(parts[2])
            base64.b64decode(parts[3])
        except binascii.Error:
            self.fail("Salt or hash is not valid base64")

    def test_correct_password_verification(self):
        """
        Test if password correct by hashing and de-hashing
        """

        password = 'mysecret'
        hasher = PasswordHasher(password)
        hashed = hasher.hash_password()

        verifier = PasswordHasher(password)
        self.assertTrue(verifier.verify_password(hashed))

    def test_wrong_password_verification(self):
        """
        Test with wrong password verification:

        'wrong_password' hash checks with hash of 'correct_password'
        """

        hasher = PasswordHasher('correct_password')
        hashed = hasher.hash_password()

        wrong_verifier = PasswordHasher('wrong_password')
        self.assertFalse(wrong_verifier.verify_password(hashed))

    def test_invalid_hash_string(self):
        """
        Test hash with invalid hash
        """

        hasher = PasswordHasher('somepass')
        invalid_hash = 'not$a$valid$hash$string'

        self.assertFalse(hasher.verify_password(invalid_hash))

class CryptoTextTest(unittest.TestCase):
    """Test CryptoText class"""

    def test_valid_data_verify(self):
        """
        Test class with valid data
        """

        password = '123'
        data = 'test'

        #self.assertTrue(CryptoText(password=password).decrypt(encoded_text))

        encoded_text = CryptoText(password=password).encrypt(data)
        decrypted = CryptoText(password=password).decrypt(encoded_text)
        self.assertEqual(decrypted, data)

    def test_decrypt_returns_str_on_success(self):
        """
        Test for str returning
        """

        password = '123'
        data = 'hello'

        encrypted = CryptoText(password).encrypt(data)
        decrypted = CryptoText(password).decrypt(encrypted)
        self.assertIsInstance(decrypted, str)


    def test_encrypt_with_invalid_types(self):
        """
        Encrypt should raise TypeError on non-str input
        """

        password = '123'
        invalid_data_list = [123, None, {123}, (123, ), {123: 123}, True]

        for data in invalid_data_list:
            with self.subTest(data=data):
                result = CryptoText(password=password).encrypt(data)
                self.assertIn('status', result)


    def test_decrypt_wrong_base64_token(self):
        """
        Ensure decrypt() raises error on malformed base64 token (the whole ciphertext)
        """

        password = '123'
        data = '123'

        result = CryptoText(password=password).decrypt(data)
        self.assertTrue('status' in result)

    def test_decrypt_wrong(self):
        """
        Check decrypt() with wrong base64 token
        """

        # 33 bytes = 16 (salt) + 16 (iv) + 1 byte garbage — should fall to decrypt.finalize()
        data = base64.b64encode(bytes("A"*33, encoding='utf-8'))
        password = '123'

        result = CryptoText(password=password).decrypt(data)
        self.assertTrue('status' in result)

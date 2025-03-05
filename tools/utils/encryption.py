from cryptography.fernet import Fernet
import base64
import os

class PegasusEncryption:
    def __init__(self, key_file="config/security.key"):
        self.key_file = key_file
        self.load_or_generate_key()
        
    def load_or_generate_key(self):
        """Load atau generate kunci enkripsi"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
                
        self.cipher_suite = Fernet(self.key)
        
    def encrypt(self, data):
        """Enkripsi data"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
        
    def decrypt(self, encrypted_data):
        """Dekripsi data"""
        return self.cipher_suite.decrypt(encrypted_data) 
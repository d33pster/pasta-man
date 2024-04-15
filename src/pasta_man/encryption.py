from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode

class Encryption:
    def __init__(self, password: bytes, string: bytes):
        self._kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            iterations=480000,
            salt="pastaman".encode('ascii')
        )
        
        self.str = string
        
        _p = urlsafe_b64encode(self._kdf.derive(password))
        
        self._fernet = Fernet(_p)
    
    def lock(self):
        self.__encryptedstring__ = self._fernet.encrypt(self.str)
    
    def unlock(self):
        self.__unencryptedstring__ = self._fernet.decrypt(self.str)
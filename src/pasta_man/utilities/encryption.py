"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
        - contents:
            base64.urlsafe_b64encode (function)
    - external:
        - description: Needs to be installed using pip.
        -contents:
            cryptography.fernet.Fernet (class)
            cryptography.hazmat.primitives.hashes.SHA256 (class)
            cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC (class)
    - Project Specific
        - description: Modules made for this project.
        - contents:
            pasta_man.exceptions.RestrictedActivity (class)

Hierarchy:
    - encryption.py:
        - contents:
            - Encryption (class)
                - contents:
                    __init__
                    lock
                    unlock

Encryption class:
    - description: Encryption class is made for master key encryption.

__init__:
    - description: This method is called as soon as the Encryption class is initialized.
    - params:
        - masterp:
            - description: A byte type data to be encrypted or decrypted.
            - type: bytes

lock:
    - description: locks the given data.

unlock:
    - description: unlocks the given data.

Working:
    - When the class is initialized, only one operation out of lock or unlock can be performed.
    - To perform multiple tasks, the class needs to be initialized again.
"""

# import all required internal modules
from base64 import urlsafe_b64encode

# import all required external modules
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# import all project specific modules
from pasta_man.utilities.Exceptions.exceptions import RestrictedActivity

# Encryption Class Definition
class Encryption:
    # __init__ function
    def __init__(self, masterp: bytes):
        # define hidden variable
        self.__status = True
        # define a password (default currently)
        password = "pastaman".encode('ascii')
        
        # define a kdf for deriving a password from the above string.
        self._kdf = PBKDF2HMAC(
            algorithm=SHA256(), # algorithm used is SHA256
            length=32,
            iterations=480000,
            salt="pastaman".encode('ascii') # salt is an extra text added to improve protection.
        )
        
        # define class variable so that the masterp can be accessed all through the class
        self.str = masterp
        
        # derive the password using the kdf and encode it using urlsafe_b64encode
        _p = urlsafe_b64encode(self._kdf.derive(password))
        
        # define class fernet object.
        self._fernet = Fernet(_p)
    
    # lock function
    def lock(self) -> bytes:
        """## lock the masterp

        ### Raises:
            - `RestrictedActivity`: the class can be only used once.

        ### Returns:
            - `bytes`: returns locked bytes
        """
        # return locked bytes if status is True.
        if self.__status:
            try:
                return self._fernet.encrypt(self.str)
            finally:
                # after return, change status to False.
                self.__status = False
        # if status is false, raise error.
        else:
            raise RestrictedActivity(RestrictedActivity.RESTRICTEDACTIVITY, 'lock')
    
    # unlock function
    def unlock(self) -> bytes:
        """## unlock the string

        ### Raises:
            - `RestrictedActivity`: the class can be only used once

        ### Returns:
            - `bytes`: return unlocked bytes
        """
        # return unlocked bytes if status is True
        if self.__status:
            try:
                return self._fernet.decrypt(self.str)
            finally:
                # after return, change status ti False.
                self.__status = False
        # if status is False, raise error.
        else:
            raise RestrictedActivity(RestrictedActivity.RESTRICTEDACTIVITY, 'unlock')
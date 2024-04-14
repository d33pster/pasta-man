from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from datetime import datetime
from tabulate import tabulate
import pandas as pd

class targets:
    def __init__(self, masterpassword: bytes, mastersalt: bytes = "passman".encode('ascii')):
        """Initialize targets class.

        Args:
            masterpassword (bytes): master password encoded in 'ascii'
            mastersalt (bytes, optional): master salt encoded in 'ascii'. Defaults to "passman".encode('ascii').
        
        Description:
            masterpassword: The Password to Encrypt All. To encode in bytes, use <password-value>.encode('ascii')
            mastersalt: Salt is addition text to strengthen the password. By default it is set to 'passman'. To encode in bytes, use <salt-text>.encode('ascii')
        """
        # initialize data
        self.data:list[dict] = []
        
        # create kdf object
        _kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            iterations=480000,
            salt=mastersalt,
        )
        
        # derive password digest
        self.passwd = urlsafe_b64encode(_kdf.derive(masterpassword))
        
        # define fernet object
        self.fernet = Fernet(self.passwd)
    
    def add(self, target:str, targettype: str, username: str, password:bytes):
        """Add data in collection.

        Args:
            target (str): _description_
            targettype (str): _description_
            username (str): _description_
            password (bytes): _description_
        """
        data = {
            "target-type":targettype,
            "target":target,
            "username":username,
            "password":self.fernet.encrypt(password),
            "timestamp":datetime.now()
        }
        
        self.data.append(data)
    
    def remove(self, target:str, username: str):
        for dictionary in self.data:
            if dictionary['target']==target and dictionary['username']==username:
                dump = self.data.pop(self.data.index(dictionary))
                dump = None
    
    def authenticate(self, username: str ,password: bytes):
        for dictionary in self.data:
            if dictionary['username']==username and dictionary['password']==self.fernet.encrypt(password):
                return True
        
        return False
    
    def count(self):
        counts:dict = {}
        count_target_types: int = 0
        counted_targets: list[str] = []
        for dictionary in self.data:
            if dictionary['target-type'] not in counted_targets:
                count_target_types += 1
                counted_targets.append(dictionary['target-type'])
        
        count = 0
        for targettype in counted_targets:
            for dictionary in self.data:
                if dictionary['target-type'] == targettype:
                    count += 1
            
            counts[targettype] = count
            count = 0
        
        return counts
    
    def search(self, searchkeyword: str, keywordtype: str = "target") -> dict | None:
        for dictionary in self.data:
            if searchkeyword in dictionary[keywordtype]:
                return dictionary
        
        return None
    
    def export(self, exporttype: str = "csv"):
        self.DataFrame = pd.DataFrame(self.data).drop('timestamp', axis=1)
        
        if exporttype == 'csv':
            self.DataFrame.to_csv(datetime.now()+"-passman-passwords.csv", index = False, header = False)
        elif exporttype == 'xlsx':
            self.DataFrame.to_excel(datetime.now()+"-passman-passwords.xlsx", index=False, header=False)
        
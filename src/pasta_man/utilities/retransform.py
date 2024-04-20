#
# This file is responsible for retransforming imported passwords
#

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from os.path import join as jPath
from datetime import datetime
from pathlib import Path
import pandas as pd

#
# Format of the imported file will be -> 1. masterrow, 2. initrow, 3. data ...
#
class Retransform:
    def __init__(self, datapath: str, ext: str = "csv"):
        if ext==".csv":
            self.__data = pd.read_csv(datapath, header=None, names=['target-type', 'target', 'username', 'password'])
        elif ext==".xlsx":
            self.__data = pd.read_excel(datapath, header=None, names=['target-type', 'target', 'username', 'password'])
        self.__masterrow = self.__data.iloc[0]
        self.__data = self.__data.drop(0) # drop master column,
        self.__data = self.__data.drop(1) # drop init column.
        print(self.__data)
        self.__oldEncryptedMasterPassword:str = self.__masterrow['password']
        __kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt="pastaman".encode('ascii'),
            iterations=480000,
        )
        __password = urlsafe_b64encode(__kdf.derive('pastaman'.encode('ascii')))
        __fernet = Fernet(__password)
        self.__oldDecryptedMasterPassword:bytes = __fernet.decrypt(self.__oldEncryptedMasterPassword.encode('ascii'))
        
        __oldkdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt="pastaman".encode('ascii'),
            iterations=480000,
        )
        __oldpassword = urlsafe_b64encode(__oldkdf.derive(self.__oldDecryptedMasterPassword))
        self.__oldfernet = Fernet(__oldpassword)
        
        __newkdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt="pastaman".encode('ascii'),
            iterations=480000,
        )
        
        with open(jPath(str(Path.home()), '.pastaman', '.m'), 'rb') as mfile:
            __newpassword = urlsafe_b64encode(__newkdf.derive(mfile.read()))
        
        self.__newfernet = Fernet(__newpassword)
        
        self.__newdata:list[dict] = []
        for i in range(len(self.__data)):
            row = self.__data.iloc[i]
            element = {
                "target-type":row['target-type'],
                "target":row['target'],
                "username":row['username'],
                "password":self.__newfernet.encrypt(self.__oldfernet.decrypt(row['password'].encode('ascii'))).decode('ascii'),
                "timestamp":datetime.today().strftime("%Y-%m-%d")
            }
            self.__newdata.append(element)
    
    def __fetchdata(self) -> list[dict]:
        return self.__newdata

    data = property(fget=__fetchdata)
#
# This file is an architecture for all operations
#

# import project specific modules.
from passman.exceptions import InvalidKeyword, InvalidExportType

# import other arguments
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from pathlib import Path
from os import makedirs
from os.path import join as jPath, exists as there
from datetime import datetime
# from tabulate import tabulate
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
        
        # check for pre-existing config files
        # -> if not found, create
        # --> store home path
        home = str(Path.home())
        if not there(jPath(home, '.passman')):
            makedirs(jPath(home, '.passman'))
        
        if there(jPath(home, '.passman', '.passwords')):
            # open passwords file
            with open(jPath(home, '.passman', '.passwords'), 'rb') as p:
                content = p.read()
            # decrypt passwords file
            content = self.fernet.decrypt(content)
            
            # divide content based on lines
            content = content.split('\n')
    
    def add(self, target:str, targettype: str, username: str, password:bytes):
        """Add data in collection.

        Args:
            target (str): target is the place where this data is valid.
            targettype (str): example -> link, app, etc.
            username (str): credential
            password (bytes): password in bytes. Encoding -> 'ascii'
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
        """remove an entry from the collection of all entries.

        Args:
            target (str): target name.
            username (str): username.
        """
        for dictionary in self.data:
            if dictionary['target']==target and dictionary['username']==username:
                dump = self.data.pop(self.data.index(dictionary))
                dump = None
    
    def authenticate(self, username: str ,password: bytes) -> bool:
        """check if the username has the given password

        Args:
            username (str): username 
            password (bytes): password encoded in 'ascii'. To encode in ascii, use -> <password-text>.encode('ascii')

        Returns:
            bool: True if authentication passes, else False.
        """
        for dictionary in self.data:
            if dictionary['username']==username and dictionary['password']==self.fernet.encrypt(password):
                return True
        
        return False
    
    def count(self) -> dict:
        """Dynamic count of all target-types

        Returns:
            dict: returns a dictionary with target-types as keys and their counts as their values.
        
        Description:
            Example Output:
                1. {
                    "target-type_1":23,
                    "target-type_2":10,
                    ...
                }
                
                2. {} -> could be an empty dict.
        """
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
        """search an entry by these keywordtypes -> ['target', 'target-type', 'username']

        Args:
            searchkeyword (str): _description_
            keywordtype (str, optional): _description_. Defaults to "target".

        Returns:
            dict | None: _description_
        """
        valid = ['target', 'target-type', 'username']
        
        if keywordtype not in valid:
            raise InvalidKeyword(f'{keywordtype} cannot be set as keywordtype.')
        
        for dictionary in self.data:
            if searchkeyword in dictionary[keywordtype]:
                return dictionary
        
        return None
    
    def export(self, exporttype: str = "csv") -> None:
        """General purpose Export. Excludes timestamp.

        Args:
            exporttype (str, optional): specify export type. Valid -> ['csv', 'xlsx']. Defaults to "csv".
        """
        valid = ['csv', 'xlsx']
        
        if exporttype not in valid:
            raise InvalidExportType(f'{exporttype} is not supported yet.')
        
        self.DataFrame = pd.DataFrame(self.data).drop('timestamp', axis=1)
        
        if exporttype == 'csv':
            self.DataFrame.to_csv(datetime.now()+"-passman-passwords.csv", index = False, header = False)
        elif exporttype == 'xlsx':
            self.DataFrame.to_excel(datetime.now()+"-passman-passwords.xlsx", index=False, header=False)
    
    # def import(self, )
        
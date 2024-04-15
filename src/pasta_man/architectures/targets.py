#
# This file is an architecture for all operations
#

# import project specific modules.
from pasta_man.exceptions import InvalidKeyword, InvalidExportType

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
from re import match

#
# The format to save the persistent passwords file ==>
# key:value|key:value|...\n
#
#

class targets:
    def __init__(self, masterpassword: bytes, mastersalt: bytes = "pastaman".encode('ascii')):
        """Initialize targets class.

        Args:
            masterpassword (bytes): master password encoded in 'ascii'
            mastersalt (bytes, optional): master salt encoded in 'ascii'. Defaults to "pastaman".encode('ascii').
        
        Description:
            masterpassword: The Password to Encrypt All. To encode in bytes, use <password-value>.encode('ascii')
            mastersalt: Salt is addition text to strengthen the password. By default it is set to 'pastaman'. To encode in bytes, use <salt-text>.encode('ascii')
        """
        # initialize data
        self.data:list[dict] = []
        self.msalt = mastersalt
        self.mpass = masterpassword
    
    def init(self):
        # create kdf object
        _kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            iterations=480000,
            salt=self.msalt,
        )
        
        # derive password digest
        self.passwd = urlsafe_b64encode(_kdf.derive(self.mpass))
        
        # define fernet object
        self.fernet = Fernet(self.passwd)
        
        # check for pre-existing config files => for persistent memory
        # -> if not found, create
        # --> store home path
        home = str(Path.home())
        
        # if config file present, else create an init entry.
        if there(jPath(home, '.pastaman', '.passwords')):
            # open passwords file
            with open(jPath(home, '.pastaman', '.passwords'), 'rb') as p:
                content = p.read()
            # decrypt passwords file
            content = self.fernet.decrypt(content)
            
            # divide content based on lines
            content = content.decode('ascii').split('\n')
            
            # for each line add the data to self.data
            for x in content:
                if x=="":
                    continue
                # split key-value pairs
                x = x.split('|') # [k:v, k:v, ...]
                # for each key-value pair, store key and value
                # -> in data
                data = {}
                for kv in x:
                    # split keys and values
                    kv = kv.split(':')
                    data[kv[0]] = kv[1]
                
                self.data.append(data)
            
            content = None
        else:
            # create a .passwordsfile
            with open(jPath(home, ".pastaman", '.passwords'), 'w') as pfile:
                pfile.write(f"target-type:init|target:init|username:init|password:{self.fernet.encrypt('init'.encode('ascii')).decode('ascii')}|timestamp:{datetime.today().strftime('%Y-%m-%d')}\n")
            
            with open(jPath(home, ".pastaman", '.passwords'), 'rb') as p:
                content = p.read()
            
            content = self.fernet.encrypt(content)
            
            with open(jPath(home, ".pastaman", '.passwords'), 'wb') as pfile:
                pfile.write(content)
            
            content = None
        
    
    def add(self, target:str, targettype: str, username: str, password:bytes):
        """Add data in collection.

        Args:
            target (str): target is the place where this data is valid.
            targettype (str): example -> link, app, etc.
            username (str): credential
            password (bytes): password in bytes. Encoding -> 'ascii'
        """
        # set date time format
        t = datetime.today().strftime("%Y-%m-%d")
        
        # define data instance
        data = {
            "target-type":targettype,
            "target":target,
            "username":username,
            "password":self.fernet.encrypt(password),
            "timestamp":t
        }
        
        # append to self.data for safe keeping
        self.data.append(data)
        
        # create the string to be written in .passwords file
        pstring = "target-type:"+targettype+'|'+"target:"+target+'|'+"username:"+username+'|'+"password:"+self.fernet.encrypt(password).decode('ascii')+"|"+"timestamp:"+t
        
        # decrypt the passwords file
        # -> read it
        with open(jPath(str(Path.home()), ".pastaman", '.passwords'), 'rb') as pfile:
            content = pfile.read()
        
        # decrypt
        content = self.fernet.decrypt(content)
        
        # add entry
        content = content.decode('ascii').split('\n') # split by lines
        content.append(pstring)
        
        pstring = None
        
        # generate the string again
        newcontent = ""
        for x in content:
            newcontent += x + "\n"
        
        content = None
        
        newcontent = self.fernet.encrypt(newcontent.encode('ascii'))
        
        # write it
        with open(jPath(str(Path.home()), '.pastaman', '.passwords'), 'wb') as pfile:
            pfile.write(newcontent)
        
        newcontent = None
    
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
    
    def search(self, searchkeyword: str, keywordtype: str = "target"):
        """search an entry by these keywordtypes -> ['target', 'target-type', 'username']

        Args:
            searchkeyword (str): _description_
            keywordtype (str, optional): _description_. Defaults to "target".
        """
        valid = ['target', 'target-type', 'username']
        
        if keywordtype not in valid:
            raise InvalidKeyword(f'{keywordtype} cannot be set as keywordtype.')
        
        self.__searchresult__ = None
        
        for dictionary in self.data:
            if searchkeyword in dictionary[keywordtype]:
                self.__searchresult__ = dictionary

    def targets(self):
        ts:list[str] = []
        added = []
        for dictionary in self.data:
            if dictionary['target-type']!="init" and dictionary['target-type'] not in added:
                ts.append(dictionary['target-type'])
                added.append(dictionary['target-type'])
        
        self.__target_types__ = ts
    
    def decrypt(self, password: bytes):
        self._dec_ = self.fernet.decrypt(password).decode('ascii')
    
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
            self.DataFrame.to_csv(datetime.now()+"-pastaman-passwords.csv", index = False, header = False)
        elif exporttype == 'xlsx':
            self.DataFrame.to_excel(datetime.now()+"-pastaman-passwords.xlsx", index=False, header=False)
    
    # def import(self, )
        
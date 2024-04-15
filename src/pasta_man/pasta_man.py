#!/usr/bin/env python3

# version info
__version__ = "1.0.4"

# import project specific modules
from pasta_man.architectures.gui import pmanager
from pasta_man.encryption import Encryption
from pasta_man.exceptions import NoneTypeVariable, OptError
from pasta_man.utilities.helptext import helptext

# import libs
from tkinter import *
from tkinter import simpledialog
from termcolor import colored
from pathlib import Path
from os.path import join as jPath, exists as there
from os import makedirs
from optioner import options
import sys
import threading

def locker(masterpassword: str):
    global encb
    enc = Encryption("pastaman".encode('ascii'), masterpassword.encode('ascii'))
    enc.lock()
    encb = enc.__encryptedstring__
    sys.exit(0)

def unlocker(encpassword: str):
    global dencb
    denc = Encryption("pastaman".encode("ascii"), encpassword.encode('ascii'))
    denc.unlock()
    dencb = denc.__unencryptedstring__
    sys.exit(0)

def checkmfile(home = str(Path.home())) -> bytes:
    # --> find out if master password is defined -> .m file
    if not there(jPath(home, '.pastaman', '.m')):
        # ask dialog
        masterpassword = simpledialog.askstring("User Input", "Enter Master Password: ")
        # check if it is empty or non
        if masterpassword=='' or masterpassword==None:
            raise NoneTypeVariable('Aborted.')
        # encode it
        masterpassword = masterpassword.encode('ascii')
        enct = threading.Thread(target=locker, args=(masterpassword.decode('ascii'),))
        enct.start()
        enct.join()
        # -> store it
        with open(jPath(home, '.pastaman', '.m'), 'wb') as m:
            m.write(encb)
    else:
        # if m is present
        # -> read it
        with open(jPath(home, '.pastaman', '.m'), 'rb') as m:
            masterpassword = m.read() # this is encrypted
        
        # -> decrypt it using the Encryption class
        # denc = Encryption("pastaman".encode('ascii'), masterpassword)
        # denc.unlock()
        denct = threading.Thread(target=unlocker, args=(masterpassword.decode('ascii'),))
        denct.start()
        denct.join()
        
        # fetch it again
        masterpassword = dencb
    
    return masterpassword

def main():
    # define global vars
    global encb, dencb
    
    # define arguments
    shortargs = ['h', 'v']
    longargs = ['help', 'version']
    
    optctrl = options(shortargs, longargs, sys.argv[1:], ifthisthennotthat=[['help', 'h'],['v', 'version']])
    args, check, error, falseargs = optctrl._argparse()
    
    if not check:
        raise OptError(error)
    else:
        h = helptext()
        h.__version__ = __version__
        if '-v' in args or '--version' in args:
            h.showver()
        elif '-h' in args or '--help' in args:
            h.helper()
    
    # -> home folder
    home = str(Path.home())
    # -> find out if .pastaman folder is there
    if not there(jPath(home, '.pastaman')):
        makedirs(jPath(home, '.pastaman'))
    
    masterpassword = checkmfile()
    
    # define main root gui window
    rootwindow = Tk()
    
    # create pass manager object.
    pManager = pmanager(rootwindow, masterpassword)
    pManager._makeinitscreen_()
    
    rootwindow.mainloop()

if __name__=="__main__":
    encb:bytes = ''.encode('ascii')
    dencb:bytes = ''.encode('ascii')
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n"+colored("KEYBOARD INTERRUPT", 'red'))
        sys.exit(1)
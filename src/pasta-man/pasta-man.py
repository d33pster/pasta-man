#!/usr/bin/env python3

# import project specific modules
from _class import pmanager
from encryption import Encryption

# import libs
from tkinter import *
from tkinter import ttk, simpledialog
from termcolor import colored
from pathlib import Path
from os.path import join as jPath, exists as there
from os import makedirs
import sys
import threading

def locker(masterpassword: str):
    global encb
    enc = Encryption("passman".encode('ascii'), masterpassword.encode('ascii'))
    enc.lock()
    encb = enc.__encryptedstring__

def unlocker(encpassword: str):
    global dencb
    denc = Encryption("passman".encode("ascii"), encpassword.encode('ascii'))
    denc.unlock()
    dencb = denc.__unencryptedstring__

def checkmfile(home = str(Path.home())) -> bytes:
    # --> find out if master password is defined -> .m file
    if not there(jPath(home, '.passman', '.m')):
        # ask dialog
        masterpassword = simpledialog.askstring("User Input", "Enter Master Password: ")
        # encode it
        masterpassword = masterpassword.encode('ascii')
        # lock it -> store it
        # -> define Encryption object
        # enc = Encryption("passman".encode('ascii'), masterpassword)
        # # -> lock it
        # enc.lock()
        enct = threading.Thread(target=locker, args=(masterpassword.decode('ascii'),))
        enct.start()
        enct.join()
        # -> store it
        with open(jPath(home, '.passman', '.m'), 'wb') as m:
            m.write(encb)
    else:
        # if m is present
        # -> read it
        with open(jPath(home, '.passman', '.m'), 'rb') as m:
            masterpassword = m.read() # this is encrypted
        
        # -> decrypt it using the Encryption class
        # denc = Encryption("passman".encode('ascii'), masterpassword)
        # denc.unlock()
        denct = threading.Thread(target=unlocker, args=(masterpassword.decode('ascii'),))
        denct.start()
        denct.join()
        
        # fetch it again
        masterpassword = dencb
    
    return masterpassword

def main():
    global encb, dencb
    # -> home folder
    home = str(Path.home())
    # -> find out if .passman folder is there
    if not there(jPath(home, '.passman')):
        makedirs(jPath(home, '.passman'))
    
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
        main()
    except KeyboardInterrupt:
        print("\n"+colored("KEYBOARD INTERRUPT", 'red'))
        sys.exit(1)
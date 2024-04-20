#!/usr/bin/env python3
"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
        - contents:
            pathlib.Path (class)
            shutil.rmtree (variable)
            os.makedirs (function)
            os.system (function)
            os.path.abspath (function)
            os.path.join(function):
                - alias: 'jPath'
            os.path.exists (function):
                - alias: 'there'
            threading (module)
            sys (module)
            platform (module)
    - external:
        - description: Needs to be installed using pip.
        -contents:
            tkinter.* (all)
            tkinter.simpledialog (module)
            termcolor.colored (function)
            optioner.options (class)
    - Project Specific
        - description: Modules made for this project.
        - contents:
            pasta_man.architectures.gui.pmanager (class)
            pasta_man.encryption.Encryption (class)
            pasta_man.exceptions.NoneTypeVariable (class)
            pasta_man.exception.OptError (class)
            pasta_man.utilities.helptext.helptext (class)

Hierarchy:
    - pasta_man.py
        - contents:
            locker (function)
            unlocker (function)
            checkmfile (function)
            main (function)

locker:
    - description: lock function to lock master password. This is called as a thread.

unlocker:
    - description: unlock function to unlock master password. This is called as a thread.

checkmfile:
    - description: check for master password file.

main:
    - descripton: main driver function.

Working:
    - catch and analyse arguments if any. If Found, execute it. Else Move on.
    - Check for master password
    - If found, decrypt it and call pmanager class. If not found, ask the user for master password, encrypt and save it and then call pmanager class.
"""

# version info
__version__ = "1.0.10"

# import internal modules
from pathlib import Path
from os.path import join as jPath, exists as there, abspath, splitext
from os import makedirs, system as run, getcwd as pwd
from shutil import rmtree
import sys, threading, platform

# import external modules
from tkinter import *
from tkinter import simpledialog, filedialog
from termcolor import colored
from optioner import options

# import project specific modules
from pasta_man.architectures.gui import pmanager
from pasta_man.architectures.targets import targets
from pasta_man.encryption import Encryption
from pasta_man.exceptions import NoneTypeVariable, OptError
from pasta_man.utilities.helptext import helptext
from pasta_man.utilities.pasta_docs import docstring

# constant
ORIGINAL:list[str] = []

# locker function
def locker(masterpassword: str):
    """
    Function to lock the encryption using a master password.

    Args:
        masterpassword (str): The master password used for encryption.

    Returns:
        None
    """
    global encb
    enc = Encryption(masterpassword.encode('ascii'))
    encb = enc.lock()
    sys.exit(0)

def unlocker(encpassword: str):
    """
    Function to unlock encrypted data using a password.

    Args:
        encpassword (str): The password used to unlock the encrypted data.

    Returns:
        None
    """
    global dencb
    denc = Encryption(encpassword.encode('ascii'))
    dencb = denc.unlock()
    sys.exit(0)


def checkmfile(home = str(Path.home())) -> bytes:
    """
    Check if the master password is defined and retrieve it from a file if it exists.

    Args:
        home (str | optinal): The home directory path. Defaults to the user's home directory.

    Returns:
        bytes: The master password.

    Raises:
        NoneTypeVariable: If the master password is empty or None.

    """
    # --> find out if master password is defined -> .m file
    if not there(jPath(home, '.pastaman', '.m')):
        # ask dialog
        masterpassword = simpledialog.askstring("User Input", "Enter Master Password: ", show='-')
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


def __remove(excpt: list[str]) -> list[str]:
    global ORIGINAL
    without:list[str] = []
    for x in ORIGINAL:
        if x in excpt:
            continue
        else:
            without.append(x)

    return without

def main():
    """
    The main function of the program.
    """
    # -> home folder
    home = str(Path.home())
    # -> find out if .pastaman folder is there
    if not there(jPath(home, '.pastaman')):
        makedirs(jPath(home, '.pastaman'))
    
    masterpassword = checkmfile()
    
    # define global vars
    global encb, dencb, ORIGINAL
    
    # define arguments
    shortargs = ['h', 'v', 'p', 'rmc', 'dwl', 'i', 'e']
    longargs = ['help', 'version', 'path', 'remove-configurations', 'doc-w-list', 'import', 'export']
    
    ORIGINAL = shortargs.copy()
    ORIGINAL.extend(longargs)
    
    # create options class object
    optctrl = options(shortargs, longargs, sys.argv[1:], ifthisthennotthat=[
        ['help', 'h'],__remove(['help', 'h']),
        ['v', 'version'], __remove(['v', 'version']),
        ['p', 'path'], __remove(['p', 'path']),
        ['rmc', 'remove-configurations'], __remove(['rmc', 'remove-configurations']),
        ['dwl', 'doc-w-list'], __remove(['dwl', 'doc-w-list']),
        ['i', 'import'], __remove(['i', 'import']),
        ['e', 'export'], __remove(['export', 'e'])
    ])
    # process args
    args, check, error, falseargs = optctrl._argparse()
    
    # if there is any error
    if not check:
        raise OptError(error)
    else:
        h = helptext()
        h.__version__ = __version__
        if '-v' in args or '--version' in args:
            h.showver()
        elif '-h' in args or '--help' in args:
            h.helper()
        elif '-p' in args or '--path' in args:
            print(abspath(__file__))
            sys.exit(0)
        elif '-rmc' in args or '--remove-configurations' in args:
            rmtree(jPath(str(Path.home()), '.pastaman'))
            sys.exit(0)
        elif '-dwl' in args or '--doc-w-list' in args:
            docs = docstring()
            print(colored('Pasta Man', 'blue'), colored(f'v{__version__}', 'red'))
            print('\n'+colored('Hierarchy:', 'yellow'))
            docs.listRecurseF()
            print('\nExample: pasta_man.architectures.gui')
            userin = input(colored('pasta>>> ', 'yellow'))
            document = docs.fetch(userin)
            if document!=None:
                if platform.system()=='Windows':
                    run('cls')
                else:
                    run('clear')
                print('\n'+colored(f'{userin}', 'yellow'), 'docstring: ')
                print(document)
            else:
                print(colored(f'No docstring defined for {userin}', 'red'))
            
            sys.exit(0)
        elif '-e' in args or '--export' in args:
            path = filedialog.askdirectory(title="Export Path", initialdir=pwd())
            ext = optctrl._what_is_('e')
                
            if path:
                t = targets(masterpassword)
                thread = threading.Thread(target=t.init)
                thread.start()
                thread.join()
                threading.Thread(target=t.export, args=(ext, path)).start()
            
            sys.exit(0)
        elif '-i' in args or '--import' in args:
            path = filedialog.askopenfilename(title="Import", initialdir=pwd(), filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")], defaultextension="*.csv")
            p, ext = splitext(path)
            if path:
                t = targets(masterpassword)
                thread = threading.Thread(target=t.init)
                thread.start()
                thread.join()
                threading.Thread(target=t.importer, args=(ext, path)).start()
            
            sys.exit(0)
            
    
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
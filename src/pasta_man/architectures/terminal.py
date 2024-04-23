#
# This file is responsible for all terminal related activities
#

from pasta_man.utilities.Exceptions.TerminalExceptions import ArgumentError, EmptyArgument
from pasta_man.architectures.targets import targets
from pasta_man.utilities.encryption import Encryption
from pasta_man.utilities.helptext import Helptext
from pasta_man.utilities.pasta_docs import Docstring

from os.path import dirname, abspath, isdir, join as jPath, splitext, isfile
from os import system as run, getcwd as pwd
from pathlib import Path
from optioner import options
from colorama import Fore as f
from shutil import rmtree
from wrapper_bar.wrapper import Wrapper
import sys, platform, threading, pyperclip
from getpass import getpass

class Terminal:
    def __init__(self, __version__:str, globalArgs: list[str], masterpassword: bytes) -> None:
        self.__masterpassword = masterpassword
        self.__argv = globalArgs
        self.__shortargs = ['h', 'v', 'p', 'rmc', 'dwl', 'i', 'e', 's']
        self.__longargs = ['help', 'version', 'path', 'remove-configurations', 'doc-w-list', 'import', 'export', 'search']
        self.__mutex = [
            ['help', 'h'],self.__remFromOriginal(['help', 'h']),
            ['v', 'version'], self.__remFromOriginal(['v', 'version']),
            ['p', 'path'], self.__remFromOriginal(['p', 'path']),
            ['rmc', 'remove-configurations'], self.__remFromOriginal(['rmc', 'remove-configurations']),
            ['dwl', 'doc-w-list'], self.__remFromOriginal(['dwl', 'doc-w-list']),
            ['i', 'import'], self.__remFromOriginal(['i', 'import']),
            ['e', 'export'], self.__remFromOriginal(['export', 'e']),
            ['s', 'search'], self.__remFromOriginal(['s', 'search'])
        ]

        self.__analyze()
        self.__help(__version__)
        self.__readOnlyArgs(__version__)
        self.__permanentEffectArgs()
        
    def __remFromOriginal(self, excpt: list[str]) -> list[str]:
        self.ORIGINAL = self.__shortargs + self.__longargs
        withoutExcept: list[str] = []
        for x in self.ORIGINAL:
            if x in excpt:
                continue
            else:
                withoutExcept.append(x)
        
        return withoutExcept
    
    def __analyze(self) -> None:
        if len(self.__argv) == 0:
            raise EmptyArgument(EmptyArgument.EMPTYARGUMENT)
        
        self.TerminalControl = options(self.__shortargs, self.__longargs, self.__argv, ifthisthennotthat=self.__mutex)
        self.arguments, self.argumentCheck, self.argumentError, self.argumentFalseArgs = self.TerminalControl._argparse()
        
        try:
            if not self.argumentCheck:
                raise ArgumentError(ArgumentError.ARGUMENTERROR, self.argumentError)
        except ArgumentError as e:
            print(e)
            
    
    def __help(self, __version__:str) -> None:
        """If help is asked, print help and exit"""
        if '-h' in self.arguments or '--help' in self.arguments:
            __text = Helptext(__version__)
            __text.helper()
        elif '-v' in self.arguments or '--version' in self.arguments:
            __text = Helptext(__version__)
            __text.showver()
        else:
            pass
    
    def __readOnlyArgs(self, __version__: str) -> None:
        """Arguments that perform readonly tasks"""
        if '-p' in self.arguments or '--path' in self.arguments:
            print(dirname(dirname(abspath(__file__)))) # pasta-man directory
            
        elif '-dwl' in self.arguments or '--doc-w-list' in self.arguments:
            docs = Docstring()
            print(f'{f.BLUE}Pasta Man{f.RESET}', f'{f.RED}v{__version__}{f.RESET}')
            print(f'{f.GREEN}Hierarchy:{f.RESET}')
            docs.listRecurseF()
            print('\nExample: pasta_man.architecures.gui')
            userin = input(f'{f.LIGHTGREEN_EX}pasta-man>{f.RESET} ')
            document = docs.fetch(userin)
            if document and platform.system()=='Windows':
                run("cls")
                print('\n'+f'{f.YELLOW}{userin}{f.RESET}', 'docstring: ')
                print(document)
            elif document:
                run("clear")
                print('\n'+f'{f.YELLOW}{userin}{f.RESET}', 'docstring: ')
                print(document)
            else:
                print(f"{f.RED}No docstring defined for {userin}{f.RESET}")
            
            
        elif '-e' in self.arguments or '--export' in self.arguments:
            try:
                from tkinter import filedialog
                path = filedialog.askdirectory(initialdir=pwd(), title="Export To")
            except ImportError:
                path = abspath(input("Export directory: "))
                while(not isdir(path)):
                    print(f"Not a Directory: {path}. Try Again!")
                    path = abspath(input("Export directory: "))
            
            ext = self.TerminalControl._what_is_('e')
            
            if path:
                target = targets(self.__masterpassword)
                t1 = threading.Thread(target=target.init)
                t1.start()
                t1.join()
                threading.Thread(target=target.export, args=(ext, path)).start()
            
            
        elif '-s' in self.arguments or '--search' in self.arguments:
            if type(self.TerminalControl._what_is_('s', 2)):
                keywordtype, keyword = self.TerminalControl._what_is_('s', 2)
            else:
                print("Error: \'-s\ and \'--search\' arguments require two values.'")
                sys.exit(1)
            
            codes = [
                f"""
target = targets(\'{self.__masterpassword.decode('ascii')}\'.encode('ascii'))
t1 = threading.Thread(target=target.init)
t1.start()
t1.join()
target.searchAll(\'{keyword}\', \'{keywordtype}\')
results = target.searchAllResults
results = pd.DataFrame(results)
"""
            ]
            
            dependencies = [
                """from pasta_man.architectures.targets import targets""",
                """import threading""",
                """import pandas as pd"""
            ]
            
            wrap = Wrapper("searching:")
            wrap.pyShellWrapper(codes, dependencies, 0.001)
            results = wrap.pyShellWrapperResults['results']
            if not results.empty:
                print(results.drop(['password', 'timestamp'], axis=1))
            else:
                print(f"{f.RED}No Match Found{f.RESET}")
                
            index = int(input(f"{f.BLUE}index>{f.RESET} "))
            results = results.iloc[index]
            
            # ask for master pass
            allegedpass = getpass(f"{f.RED}master-password>{f.RESET} ")
            
            # get master password
            with open(jPath(str(Path.home()), '.pastaman', '.m'), 'rb') as m:
                masterpassword = m.read() # this is encrypted.
            
            thread = threading.Thread(target=self.decryptthread, args=(masterpassword.decode('ascii'),))
            thread.start()
            thread.join()
            
            if allegedpass == self.den.decode('ascii'):
                codes = [
                    f"""
target = targets(\'{self.__masterpassword.decode('ascii')}\'.encode('ascii'))
t1 = threading.Thread(target=target.init)
t1.start()
t1.join()
thread = threading.Thread(target=target.decrypt, args=(\'{results['password']}\'.encode('ascii'),))
thread.start()
thread.join()
pyperclip.copy(target.dec)
spam = pyperclip.paste()
"""
                ]
                
                dependencies = [
                    """import threading""",
                    """import pyperclip""",
                    """from pasta_man.architectures.targets import targets"""
                ]
                
                wrap = Wrapper("decrypting:")
                wrap.pyShellWrapper(codes, dependencies, 0.001)
                print(f"{f.GREEN}Password copied to clipboard.{f.RESET}")
            
            
        else:
            pass
    
    def decryptthread(self, masterpassword: str):
        denc = Encryption(masterpassword.encode('ascii'))
        self.den = denc.unlock()
        
    
    def __permanentEffectArgs(self):
        if '-rmc' in self.arguments or '--remove-configurations' in self.arguments:
            rmtree(jPath(str(Path.home()), '.pastaman'))
            
        elif '-i' in self.arguments or '--import' in self.arguments:
            try:
                from tkinter import filedialog
                path = filedialog.askopenfilename(title="Import", initialdir=pwd(), filetypes=[("Excel Files", "*.xlsx"), ("csv Files", "*.csv")], defaultextension="*.csv")
            except ImportError:
                path = abspath(input("Import: "))
                while(not isfile(path)):
                    print(f"Not a File. Try Again!")
                    path = abspath(input("Import: "))
                
            if path:
                p, ext = splitext(path)
                target = targets(masterpassword=self.__masterpassword)
                t1 = threading.Thread(target=target.init)
                t1.start()
                t1.join()
                threading.Thread(target=target.importer, args=(ext, path)).start()
            
            
        else:
            pass
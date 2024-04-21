#
# This file is responsible for all terminal related activities
#

from pasta_man.utilities.Exceptions.TerminalExceptions import ArgumentError, EmptyArgument
from pasta_man.architectures.targets import targets
from pasta_man.utilities.helptext import Helptext
from pasta_man.utilities.pasta_docs import Docstring

from os.path import dirname, abspath, isdir, join as jPath, splitext, isfile
from os import system as run, getcwd as pwd
from pathlib import Path
from optioner import options
from termcolor import colored
from shutil import rmtree
import sys, platform, threading

class Terminal:
    def __init__(self, __version__:str, globalArgs: list[str], masterpassword: bytes) -> None:
        self.__masterpassword = masterpassword
        self.__argv = globalArgs
        self.__shortargs = ['h', 'v', 'p', 'rmc', 'dwl', 'i', 'e']
        self.__longargs = ['help', 'version', 'path', 'remove-configurations', 'doc-w-list', 'import', 'export']
        self.__mutex = [
            ['help', 'h'],self.__remFromOriginal(['help', 'h']),
            ['v', 'version'], self.__remFromOriginal(['v', 'version']),
            ['p', 'path'], self.__remFromOriginal(['p', 'path']),
            ['rmc', 'remove-configurations'], self.__remFromOriginal(['rmc', 'remove-configurations']),
            ['dwl', 'doc-w-list'], self.__remFromOriginal(['dwl', 'doc-w-list']),
            ['i', 'import'], self.__remFromOriginal(['i', 'import']),
            ['e', 'export'], self.__remFromOriginal(['export', 'e'])
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
            sys.exit(0)
    
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
            sys.exit(0)
        elif '-dwl' in self.arguments or '--doc-w-list' in self.arguments:
            docs = Docstring()
            print(colored('Pasta Man', 'blue'), colored(f'v{__version__}', 'red'))
            print(colored('Hierarchy:', 'green'))
            docs.listRecurseF()
            print('\nExample: pasta_man.architecures.gui')
            userin = input(colored('pasta-man> ', 'light_green'))
            document = docs.fetch(userin)
            if document and platform.system()=='Windows':
                run("cls")
                print('\n'+colored(f'{userin}', 'yellow'), 'docstring: ')
                print(document)
            elif document:
                run("clear")
                print('\n'+colored(f'{userin}', 'yellow'), 'docstring: ')
                print(document)
            else:
                print(colored(f"No docstring defined for {userin}", 'red'))
            
            sys.exit(0)
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
            
            sys.exit(0)
        else:
            pass
    
    def __permanentEffectArgs(self):
        if '-rmc' in self.arguments or '--remove-configurations' in self.arguments:
            rmtree(jPath(str(Path.home()), '.pastaman'))
            sys.exit(0)
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
            
            sys.exit(0)
        else:
            pass
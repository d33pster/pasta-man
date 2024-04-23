"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
        - contents:
            sys (module)
    - external:
        - description: Needs to be installed using pip.
        -contents:
            colorama.Fore (variable)
    - Project Specific
        - description: Modules made for this project.

Hierarchy:
    - helptext.py
        - contents:
            - helptext (class):
                - contents:
                    __init__
                    helper
                    showver

helptext class:
    - description: contains all the predefined helptexts

__init__:
    - description: this is called as soon as helptext class is initialized

helper:
    - description: this shows help for entire pasta-man

showver:
    - description: this shows version info of pasta-man

Working:
    - show help whenever asked.
"""


from colorama import Fore as f
import sys

class Helptext:
    def __init__(self, __version__: str):
        self.__version__ = __version__
    
    def helper(self):
        print(f'{f.BLUE}Pasta Man{f.RESET}', f'{f.RED}v{self.__version__}{f.RESET}')
        print("helptext")
        print("  |  -h or --help                     : show this help and exit.")
        print("  |  -v or --version                  : show version and exit.")
        print("  |  -p or --path                     : show install path and exit.")
        print("  |  -rmc or --remove-configurations  : remove existing configs. ["+f'{f.RED}Warning{f.RESET}'+"] This is irreversible.")
        print("  |  -dwl or --doc-w-list             : list all modules of pasta-man. Enter the full-module-name for docstring.")
        print("  |  -i or --import                   : import a passwords file. Only files exported by pasta-man can be imported.")
        print(f"  |                                     {f.RED}Syntax:{f.RESET} pasta-man --import")
        print("  |  -e or --export                   : export passwords.")
        print(f"  |                                     {f.RED}Syntax:{f.RESET} pasta-man --export <export-format>")
        print("  |                                     Available export formats -> [\'csv\', \'xlsx\']")
        print("  |  -s or --search                   : search a keyword in keyword-type.")
        print(f"  |                                     {f.RED}Syntax:{f.RESET} pasta-man --search <keyword-type> <keyword>")
        print("  |                                     Available keyword types -> [\'target\', \'target-type\', \'username\']")
    
    def showver(self):
        print(f'{f.BLUE}Pasta Man{f.RESET}', f'{f.RED}v{self.__version__}{f.RESET}')
        print('author: d33pster', 'GitHub:', f'{f.LIGHTBLUE_EX}https://github.com/d33pster/pasta-man{f.RESET}')
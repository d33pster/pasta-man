"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
        - contents:
            sys (module)
    - external:
        - description: Needs to be installed using pip.
        -contents:
            termcolor.colored (function)
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


from termcolor import colored
import sys

class Helptext:
    def __init__(self, __version__: str):
        self.__version__ = __version__
    
    def helper(self):
        print(colored('Pasta Man', 'blue'), colored(f'v{self.__version__}', 'red'))
        print("helptext")
        print("  |  -h or --help                     : show this help and exit.")
        print("  |  -v or --version                  : show version and exit.")
        print("  |  -p or --path                     : show install path and exit.")
        print("  |  -rmc or --remove-configurations  : remove existing configs. ["+colored('Warning', 'red')+"] This is irreversible.")
        print("  |  -dwl or --doc-w-list             : list all modules of pasta-man. Enter the full-module-name for docstring.")
        sys.exit(0)
    
    def showver(self):
        print(colored('Pasta Man', 'blue'), colored(f'v{self.__version__}', 'red'))
        print('author: d33pster', 'GitHub:', colored('https://github.com/d33pster/pasta-man', 'light_blue'))
        sys.exit(0)
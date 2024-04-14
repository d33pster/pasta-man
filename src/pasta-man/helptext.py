from termcolor import colored
import sys

class helptext:
    def __init__(self):
        self.__version__ = ''
    
    def helper(self):
        print(colored('Pasta Man', 'blue'), colored(f'v{self.__version__}', 'red'))
        print("helptext")
        print("  |  -h or --help     : show this help and exit.")
        print("  |  -v or --version  : show version and exit.")
        sys.exit(0)
    
    def showver(self):
        print(colored('Pasta Man', 'blue'), colored(f'v{self.__version__}', 'red'))
        print('author: d33pster', 'GitHub:', colored('https://github.com/d33pster/pasta-man', 'light_blue'))
        sys.exit(0)
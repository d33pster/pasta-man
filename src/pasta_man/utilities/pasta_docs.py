"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
        - contents:
            pathlib.Path (class)
            os.scandir (function)
            os.path.dirname (function)
            os.path.abspath (function)
            inspect
    - external:
        - description: Needs to be installed using pip.
    - Project Specific
        - description: Modules made for this project.

Hierarchy:
    - pasta_docs.py
        - contents:
            - docstring (class)
                -contents:
                    __init__
                    list_recursive
                    listRecurseF
                    fetch

docstring class:
    - description: docstring class is made to fetch the docstring of a file just for pasta-man.

__init__:
    - description: This method is called as soon as the docstring class is initialized.

list_recursive:
    - description: This method can return a list of all complete module paths of pasta-man.
    - return:
        - type: list[str]

listRecurseF:
    - description: print level wise hierarchy of modules of pasta-man

fetch:
    - description: fetch the main docstring from the module file.
    - params:
        - module:
            - description: the module whose docstring needs to be fetched.
            - type: str

working:
    - This file is responsible for resolving and fetching docstrings defined inside the modules.
"""

# import internal modules
from os.path import dirname, abspath
from os import scandir
from pathlib import Path
import inspect

# class definition
class Docstring:
    # __init__ function
    def __init__(self):
        """## Initialise the docstring class
        """
        self.parentmodule = "pasta_man"
        self.directory = dirname(dirname(abspath(__file__))) # inside pasta_man dir
        # print(self.directory)
    
    def __fetch(self, submod: list[str] = [], daddy:bool = False) -> str | None:
        """## fetch the docstring of the given submodule of pasta-man

        ### Args:
            - `submod (list[str], optional)`: submodule of pasta-man. Defaults to [].
            - `daddy (bool, optional)`: Set this to True if you want to fetch docstring of parent module -> pasta-man. Defaults to False.

        ### Returns:
            - `str | None`: Returns docstring if defined, else None.
        """
        # if parent module is queried.
        if daddy or len(submod)==0:
            try:
                module = __import__(self.parentmodule)
                return inspect.getdoc(module)
            except ImportError:
                return None
        # if a submod is provided.
        else:
            # check the submod if there is more values to it.
            if len(submod)>1:
                submodules = submod
                submodlast = submodules[len(submodules)-1] # last element
                submodulesfirsts = submodules[:len(submodules)-1] # all other element in order.
                
                # merge the first elements to daddy
                dadmod = self.parentmodule
                for x in submodulesfirsts:
                    dadmod += f".{x}"
                
                # find docstring if any
                try:
                    module = __import__(dadmod, fromlist=[submodlast])
                    submodule = getattr(module, submodlast)
                    return inspect.getdoc(submodule)
                except (ImportError, AttributeError):
                    return None
            elif len(submod)==1:
                try:
                    module = __import__(self.parentmodule, fromlist=[submod[0]])
                    submodule = getattr(module, submod[0])
                    return inspect.getdoc(submodule)
                except (ImportError, AttributeError):
                    return None
    
    def __scan_recursive(self, directory: str):
        """## recursively scan a directory to list all paths

        ### Args:
            - `directory (str)`: directory to be scanned.

        ### Yields:
            - `Generator[DirEntry[str] | Any, Any, None]`
        """
        for entry in scandir(directory):
            if entry.is_file():
                yield entry
            else:
                yield from self.__scan_recursive(entry.path)
    
    def list_recursive(self) -> list[str]:
        """## list only pasta-man modules.

        ### Returns:
            - `list[str]`: list of pasta-man modules.
        """
        modules = []
        for item in self.__scan_recursive(self.directory):
            path = str(Path(item))[1:].replace('.py', '').replace('/','.').replace('\\','.')
            if '__pycache__' in path:
                continue
            
            path = self.parentmodule+path.split(self.parentmodule)[1]
            if path==self.parentmodule+".":
                path = self.parentmodule+"."+self.parentmodule
            modules.append(path)
        
        return modules
    
    def __construct_hierarchy(self, strings: list[str]) -> dict:
        """## Construct a hierarchy of all the modules from the list

        ### Args:
            - `strings (list[str])`: list of modules

        ### Returns:
            - `dict`: hierarchy dict
        """
        hierarchy = {}
        for string in strings:
            parts = string.split(".")
            current_level = hierarchy
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        return hierarchy

    def __print_hierarchy(self, hierarchy:dict, indent:str="") -> None:
        """## print hierarchy from hierarchy dict

        ### Args:
            - `hierarchy (dict)`: hierarchy dict
            - `indent (str, optional)`: indent value. Defaults to "".
        """
        for key, value in hierarchy.items():
            print(indent + "->" + key)
            if value:
                self.__print_hierarchy(value, indent + "   ")

    def listRecurseF(self) -> None:
        """## print hierarchy of pasta-man modules
        """
        modules = self.list_recursive()
        self.__print_hierarchy(self.__construct_hierarchy(modules))
    
    def fetch(self, module:str) -> str | None:
        """## fetch the docstring of pasta-man module if any.

        ### Args:
            - `module (str)`: module path

        ### Returns:
            - `str | None`: returns docstring or None
        """
        if len(module.split('.'))==1:
            return self.__fetch(daddy=True)
        elif len(module.split('.'))>1:
            return self.__fetch(submod=module.split('.')[1:])
        else:
            return None
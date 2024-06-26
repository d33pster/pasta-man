"""
Modules:
    - internal:
        - description: Already Comes installed with your python interpreter.
        - contents:
            platdorm.system (function)
            os.system (function)
            os.makedirs (function)
            os.chdir (function)
            os.path.exists (function)
            os.path.join (function)
            os.path.dirname (function)
            os.path.abspath (function)
            pathlib.Path (class)
            sys
            subprocess
    - external:
        - description: Needs to be installed using pip.
    - Project Specific
        - description: Modules made for this project.

Hierarchy:
    - Launcher.py
        - contents:
            checklogfile (function)
            makePasta (function)
            main (function)

checklogfile:
    - description: Check for log file, if not present, create it.

makePasta:
    - description: Creates a .bat file for windows which will be run to setup pasta-man for Windows (one-time)

main:
    - description: checks whether system is windows or others. If others, run pasta-man as an independent process, else run a vbs script in the background for windows to launch an independent pasta-man process.
            
Working:
    - Check system
    - if not windows, run pasta-man as an independent process (no setup required)
    - if windows, run first time setup, where an exe and vbs files are created. From next time, run exe.
"""

from platform import system as os
from os import system as run, makedirs, chdir
from os.path import exists as there, join as jPath, dirname, abspath, basename
from pathlib import Path
from wrapper_bar.wrapper import Wrapper
import sys
from colorama import init as color, Fore as f

def checklogfile():
    """## check for .log file, if not present, create it
    """
    if not there(jPath(str(Path.home()), '.pastaman')):
        makedirs(jPath(str(Path.home()), '.pastaman'))
    
    if not there(jPath(str(Path.home()), '.pastaman', '.log')):
        with open(jPath(str(Path.home()), '.pastaman', '.log'), 'w') as logfile:
            logfile.write("log file init")

def makePasta():
    directory = dirname(dirname(abspath(__file__))) # pasta_man directory
    chdir(directory)
    
    wrap = Wrapper()
    
    codes = [
        f"""subprocess.Popen(['pyinstaller', '--onefile', '--noconsole', 'pasta_man.py'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).wait()""",
    ]
    
    dependencies = [
        """import subprocess"""
    ]
    
    wrap.pyShellWrapper(codes, dependencies, delay=0.2, width=70, label="Making pasta:", timer="ElapsedTime")
    
    codes = [
        """shutil.rmtree(join(pwd(), 'build'))""",
        """remove(join(pwd(), 'pasta_man.spec'))""",
        """shutil.copyfile(join(pwd(), 'dist', 'pasta_man.exe'), join(str(Path.home()), '.pastaman', 'pasta-man.exe'))"""
    ]
    
    dependencies = [
        """import shutil""",
        """from os.path import join""",
        """from os import getcwd as pwd, remove""",
        """from pathlib import Path"""
    ]
    
    wrap.pyShellWrapper(codes, dependencies, delay=0.03, width=62, label="Cleaning up:")
    
    codes = ["""
path = join(str(Path.home()), '.pastaman')
with open(join(path, 'pasta-man.vbs'), 'w') as vbs:
    vbs.write("Set pastashell = WScript.CreateObject(\\"WScript.Shell\\")\\n")
    vbs.write("pastashell.Run \\"%USERPROFILE%\\\\.pastaman\\\\pasta-man.exe\\", 0, False")
"""]
    
    dependencies = [
        """from pathlib import Path""",
        """from os.path import join"""
    ]
    
    wrap.pyShellWrapper(codes, dependencies, delay=0.01, width=60, label="Garnishing:")
    
    print(f"{f.LIGHTGREEN_EX}Serving...{f.RESET}")


def main():
    color()
    checklogfile()
    # check for arguments
    if len(sys.argv[1:])>0:
        sys.argv[0] += sys.argv[0]+'-launcher'
        command = basename(sys.argv[0])
        for i in range(1, len(sys.argv)):
            command += " " + sys.argv[i]
        
        run(command)
        # exit
        sys.exit(0)
    
    # if no arguments run these
    system = os()
    if system=='Darwin' or system=='Linux':
        run('nohup pasta-man-launcher > ~/.pastaman/.log &')
    elif system=='Windows':
        if (not there(jPath(str(Path.home()), '.pastaman', 'pasta-man.exe'))) or (not there(jPath(str(Path.home()), '.pastaman', 'pasta-man.vbs'))):
            print(f'{f.RED}(one-time-setup){f.RESET}')
            print('Operating System: Windows\nsetting up pasta-man...\nThis might take a while.')
            makePasta()
        chdir(jPath(str(Path.home()), '.pastaman'))
        run(f"start /B wscript.exe {jPath(str(Path.home()), '.pastaman', 'pasta-man.vbs')}")
    sys.exit(0)
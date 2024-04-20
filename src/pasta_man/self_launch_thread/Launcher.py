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
import sys, subprocess

def checklogfile():
    """## check for .log file, if not present, create it
    """
    if not there(jPath(str(Path.home()), '.pastaman')):
        makedirs(jPath(str(Path.home()), '.pastaman'))
    
    if not there(jPath(str(Path.home()), '.pastaman', '.log')):
        with open(jPath(str(Path.home()), '.pastaman', '.log'), 'w') as logfile:
            logfile.write("log file init")

def makePasta():
    batdat = """
@REM turn printing of commands off
@echo off

@REM install using pyinstaller.
pyinstaller --onefile --noconsole pasta_man.py > NUL

@REM After this delete .spec file and build folder tree.
del build /s /q
del pasta_man.spec

@REM copy dist/pasta_man.exe to %USERPROFILE%\.pastaman\pasta-man.exe
copy dist\pasta_man.exe %USERPROFILE%\.pastaman\pasta-man.exe

@REM delete dist
del dist /s /q

@REM create vbs script
cd %USERPROFILE%\.pastaman
echo Set pastaShell = WScript.CreateObject("WScript.Shell") > pasta-man.vbs
echo pastaShell.Run "%USERPROFILE%\.pastaman\pasta-man.exe", 0, False >> pasta-man.vbs

@REM copy it 
"""
    directory = dirname(dirname(abspath(__file__))) # pasta_man directory
    chdir(directory)
    print('(one-time)')
    print('Operating System: Windows\nsetting up pasta-man...\nThis might take a while.')
    with open(jPath(directory, 'win-setup.bat'), 'w') as batfile:
        batfile.write(batdat)
    subprocess.Popen([f"{jPath(directory, 'win-setup.bat')}"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).wait()
    print('complete.')

def main():
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
        if not there(jPath(str(Path.home()), '.pastaman', 'pasta-man.vbs')):
            makePasta()
        chdir(jPath(str(Path.home()), '.pastaman'))
        run(f"start /B wscript.exe {jPath(str(Path.home()), '.pastaman', 'pasta-man.vbs')}")
    sys.exit(0)
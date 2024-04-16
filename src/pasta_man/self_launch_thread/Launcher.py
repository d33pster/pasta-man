#
# This file is just for Entry Point Creation
#

from platform import system as os
from os import system as run, makedirs, chdir
from os.path import exists as there, join as jPath, dirname, abspath
from pathlib import Path
import sys, subprocess

def checklogfile():
    if not there(jPath(str(Path.home()), '.pastaman')):
        makedirs(jPath(str(Path.home()), '.pastaman'))
    
    if not there(jPath(str(Path.home()), '.pastaman', '.log')):
        with open(jPath(str(Path.home()), '.pastaman', '.log'), 'w') as logfile:
            logfile.write("log file init")

def makePasta():
    batdat = """
@REM turn printing of commands off
@echo off

@REM print status
echo Operating System: Windows
echo setting up pasta-man
echo This might take a while.

@REM install using pyinstaller.
pyinstaller --onefile --noconsole pasta-man.py > NUL

@REM After this delete .spec file and build folder tree.
del build /s /q
del pasta-man.spec

@REM copy dist/pasta-man.exe to %USERPROFILE%\.pastaman\pasta-man.exe
copy dist\pasta-man.exe %USERPROFILE%\.pastaman\pasta-man.exe

@REM delete dist
del dist /s /q

@REM create vbs script
cd %USERPROFILE%\.pastaman
echo Set pastaShell = WScript.CreateObject("WScript.Shell") > pasta-man.vbs
echo pastaShell.Run "%USERPROFILE%\.pastaman\pasta-man.exe", 0, False >> pasta-man.vbs

@REM status
echo Complete.
"""
    directory = dirname(dirname(abspath(__file__))) # pasta_man directory
    chdir(directory)
    with open(jPath(directory, 'win-setup.bat'), 'w') as batfile:
        batfile.write(batdat)
    subprocess.Popen([f"{jPath(directory, 'win-setup.bat')}"]).wait()

def main():
    checklogfile()
    
    # check for arguments
    if len(sys.argv[1:])>0:
        # convert all args into a string with white spaces between them
        args = sys.argv[1]
        for i in range(len(sys.argv[2:])):
            args += " " + sys.argv[i]
        # run 
        run(f'pasta-man-launcher {args}')
        # exit
        sys.exit(0)
    
    # if no arguments run these
    system = os()
    if system=='Darwin' or system=='Linux':
        run('nohup pasta-man-launcher > ~/.pastaman/.log &')
    elif system=='Windows':
        makePasta()
        chdir(jPath(str(Path.home()), '.pastaman'))
        subprocess.Popen(['start', '\\B', 'wscipt.exe', 'pasta-man.vbs'])
    
    sys.exit(0)
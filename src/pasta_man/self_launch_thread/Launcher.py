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
        if not there(jPath(str(Path.home()), '.pastaman', 'pasta-man.vbs')):
            makePasta()
        chdir(jPath(str(Path.home()), '.pastaman'))
        run(f"start /B wscript.exe {jPath(str(Path.home()), '.pastaman', 'pasta-man.vbs')}")
    sys.exit(0)
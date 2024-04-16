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
    directory = dirname(dirname(abspath(__file__))) # pasta_man directory
    chdir(directory)
    subprocess.Popen(['win-setup.bat'],).wait()

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
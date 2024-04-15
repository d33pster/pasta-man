#
# This file is just for Entry Point Creation
#

from platform import system as os
from os import system as run
import sys

def main():
    system = os()
    if system=='Darwin' or system=='Linux':
        run('nohup pasta-man-launcher > ~/.pastaman/.log &')
    elif system=='Windows':
        run('start \"Pasta Man\" pasta-man-launcher')
    
    sys.exit(0)
#
# This file is just for Entry Point Creation
#

import threading
import sys
from pasta_man.pasta_man import main

def drumroll():
    threading.Thread(target=main()).start()
    sys.exit(0)
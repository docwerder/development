import os
import sys
sys.path.append('/Users/joerg/repos/development/utilities_functions')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from mnt_functions import mnt_WERDERNAS
from mnt_functions import mnt_WERDERNAS2
from mnt_functions import mnt_WERDERNASX
from mnt_functions import mnt_WERDERNAS2X
mnt_WERDERNAS()
print("Connected to WERDERNAS")
mnt_WERDERNAS2()
print("Connected to WERDERNAS2")
mnt_WERDERNASX()
print("Connected to WERDERNASX")
mnt_WERDERNAS2X()
print("Connected to WERDERNAS2X")
import sys
sys.path.append('/Users/joerg/repos/development/utilities_functions')

from mnt_functions import mnt_WERDERNAS
from mnt_functions import mnt_WERDERNAS2
from mnt_functions import mnt_WERDERNASX
from mnt_functions import mnt_WERDERNAS2X


if __name__ == '__main__':
    mnt_WERDERNAS()
    print('Connected to WERDERNAS')
    mnt_WERDERNAS2()
    print('Connected to WERDERNAS2')
    mnt_WERDERNASX()
    print('Connected to WERDERNASX')
    mnt_WERDERNAS2X()
    print('Connected to WERDERNAS2X')
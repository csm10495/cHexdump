'''
Brief:
    __main__.py - Called if you do py -m chexdump

Description:
    Hexdumps data from stdin. If you give a number to argv, will parse that much data from stdin,
        otherwise parses all it sees

Author(s):
    Charles Machalow
'''

from .__init__ import hexdumpFromStdin
import sys
if len(sys.argv) > 1:
    hexdumpFromStdin(int(sys.argv[1]))
else:
    hexdumpFromStdin()
    
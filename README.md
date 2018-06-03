# cHexdump
Python module for creating pretty 'hexdumps' of data sequences.

# Install
cHexdump should work on all Python 2.7's and Python 3's. To install, use pip
```
python -m pip install chexdump
```
The in Python do something like:
```
from chexdump import hexdump, sideBySideHexdump
```

# Functionality
For full explanations of functionallity use help() on the given function. Here are some quick and dirty descriptions:

## hexdump()
hexdump() allows you to dump a sequence in terms of hex with an optional ASCII printout on the right. For example:

```
>>> print hexdump([1,2,3,4,5]* 10)
0000 01 02 03 04 05 01 02 03  04 05 01 02 03 04 05 01  ................
0010 02 03 04 05 01 02 03 04  05 01 02 03 04 05 01 02  ................
0020 03 04 05 01 02 03 04 05  01 02 03 04 05 01 02 03  ................
0030 04 05    

# or

>>> print hexdump([1,2,3,4,5]* 10, showAscii=False)
0000 01 02 03 04 05 01 02 03  04 05 01 02 03 04 05 01
0010 02 03 04 05 01 02 03 04  05 01 02 03 04 05 01 02
0020 03 04 05 01 02 03 04 05  01 02 03 04 05 01 02 03
0030 04 05

# or

>>> print hexdump([1,2,3,4,5]* 10, showAscii=False, showIndexLabel=False)
01 02 03 04 05 01 02 03  04 05 01 02 03 04 05 01
02 03 04 05 01 02 03 04  05 01 02 03 04 05 01 02
03 04 05 01 02 03 04 05  01 02 03 04 05 01 02 03
04 05

# and so on... 
```

## sideBySideHexdump()
sideBySideHexdump() is used to print 2 hexdumps side-by-side and point out to the user lines that differ. For example:

```
>>> a = [10,20,30,40,50] * 10
>>> b = a[:]
>>> b[38] = 12
>>> print sideBySideHexdump(a, b)
0000  0A 14 1E 28 32 0A 14 1E  ...(2... |  0A 14 1E 28 32 0A 14 1E  ...(2... |
0008  28 32 0A 14 1E 28 32 0A  (2...(2. |  28 32 0A 14 1E 28 32 0A  (2...(2. |
0010  14 1E 28 32 0A 14 1E 28  ..(2...( |  14 1E 28 32 0A 14 1E 28  ..(2...( |
0018  32 0A 14 1E 28 32 0A 14  2...(2.. |  32 0A 14 1E 28 32 0A 14  2...(2.. |
0020  1E 28 32 0A 14 1E 28 32  .(2...(2 |  1E 28 32 0A 14 1E 0C 32  .(2....2 | !
0028  0A 14 1E 28 32 0A 14 1E  ...(2... |  0A 14 1E 28 32 0A 14 1E  ...(2... |
0030  28 32                    (2       |  28 32                    (2       |
```
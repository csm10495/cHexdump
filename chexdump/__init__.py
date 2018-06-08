'''
Brief:
    __init__.py - The main file of the cHexdump package

Description:
    cHexdump contains some functions for simple hexdump-like output

Author(s):
    Charles Machalow
'''
import math
import os
import six
import tempfile 

def hexdump(sequence, numItems=0, sequenceOffset=0, indexLabelOffset=0, indexLabelMinWidth=4, showIndexLabel=True, showAscii=True, itemsPerLine=16, itemsTillLineSplit=None, action='return', nonAsciiChar='.'):
    '''
    Brief:
        hexdump(sequence, numItems=0, sequenceOffset=0, indexLabelOffset=0, indexLabelMinWidth=4, showIndexLabel=True, showAscii=True, 
            itemsPerLine=16, itemsTillLineSplit=None, action='return', nonAsciiChar='.') -
                Used to hexdump a particular sequence.

    Description:
        This function contains a bunch of args to help get the desired style

    Argument(s):
        sequence - (Required) - thing to print
        numItems - (Optional; Defaults to 0) - if not 0: the number of items to print. If 0, use len()
        sequenceOffset - (Optional; Defaults to 0) - Offset to start printing in the sequence
        indexLabelOffset - (Optional; Defaults to 0) - Offset to start the left side counter on (for display only)
        indexLabelMinWidth - (Optional; Defaults to 4) - Min width in characters for the index label
        showIndexLabel - (Optional; Defaults to True) - If True, show index label on left
        showAscii - (Optional; Defaults to True) - If True, give ascii printout on the right
        itemsPerLine - (Optional; Defaults to 16) - Number of items per line
        itemsTillLineSplit - (Optional; Defaults to None) - Number of items till extra spacing on a given line. If None, use itemsPerLine / 2
        action - (Optional; Defaults to 'return') - If 'print' print the hexdump, if 'return' return a string of the printout, if 'scroll' page the test via more/less
        nonAsciiChar - (Optional; Defaults to '.') - When printing ASCII dump on the right, use this char if the character is not displayable via normal ASCII

    Return Value(s):
        String or None

    Related:
        sideBySideHexdump()

    Author(s):
        Charles Machalow
    '''
    if numItems is 0:
        numItems = len(sequence)
    sequence = sequence[sequenceOffset:sequenceOffset + numItems]
    if itemsTillLineSplit is None:
        itemsTillLineSplit = int(itemsPerLine / 2)

    indexLabelTemplate = ''
    if showIndexLabel:
        indexLabelTemplate = ("%%0%dX" % indexLabelMinWidth)

    numLines = int(math.ceil(numItems / float(itemsPerLine)))
    buildStr = ''
    offsetToAscii = 0
    for lineNumber in six.moves.range(numLines):
        itemOffset = lineNumber * itemsPerLine
        itemsForThisLine = sequence[itemOffset: itemOffset + itemsPerLine]
        numItemsForThisLine = len(itemsForThisLine)
        lineStr = ''

        # Line num
        if indexLabelTemplate:
            lineStr += indexLabelTemplate % (indexLabelOffset + itemOffset)
            lineStr += " "

        # hex data
        rightSideLen = numItemsForThisLine - itemsTillLineSplit
        hexTemplate = ('%02X ' * min(itemsTillLineSplit, numItemsForThisLine) + " " + ('%02X ' * max(0, rightSideLen)))
        lineStr += hexTemplate % tuple(itemsForThisLine)
        lineStr += " "

        # the ascii offset can change if the indexLabel changes in size... keep track of that to make the last line's ascii line up
        if numItemsForThisLine == itemsPerLine:
            offsetToAscii = len(lineStr)

        # ascii data
        if showAscii:
            lineStr = lineStr.ljust(offsetToAscii, ' ')
            asciiTemplate = '%s' * numItemsForThisLine
            lineStr += asciiTemplate % tuple([chr(i) if (i < 127 and i > 31) else nonAsciiChar for i in itemsForThisLine]) 

            # Fill short lines
            if numItemsForThisLine < itemsPerLine:
                lineStr += ' ' * (itemsPerLine - numItemsForThisLine)

        lineStr += os.linesep
        buildStr += lineStr

    if action == 'print':
        print(buildStr)
    elif action == 'return':
        return buildStr
    elif action == 'scroll':
        scrollText(buildStr)
    else:
        raise NotImplementedError

def scrollText(txt):
    '''
    Brief:
        scrollText(text) - Can display text via a scrollable fashion

    Description:
        This function does differnt thing depending on the OS

    Argument(s):
        txt - (Required) - Text to page/scroll

    Return Value(s):
        None

    Related:
        hexdump()

    Author(s):
        Charles Machalow
    '''
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(txt)
        
    if os.name == 'nt':
        os.system('more < %s' % f.name)
    else:
        os.system('less < %s' % f.name)
    os.remove(f.name)

def sideBySideHexdump(a, b, itemsPerLine=8, itemsTillLineSplit=0, showAscii=True, action='return'):
    '''
    Brief:
        sideBySideHexdump(a, b, itemsPerLine=8, itemsTillLineSplit=0, showAscii=True, action='return') -
            Used to display a side-by-side hex dump of two sequences.

    Description:
        This function contains a bunch of args to help get the desired style

    Argument(s):
        a - (Required) - Left sequence
        b - (Required) - right sequence
        itemsPerLine - (Optional; Defaults to 8) - Number of items per line (per side)
        itemsTillLineSplit - (Optional; Defaults to None) - Number of items till extra spacing on a given line. If None, use itemsPerLine / 2
        showAscii - (Optional; Defaults to True) - If True, give ascii printout on the right        
        action - (Optional; Defaults to 'return') If 'print' print the hexdump, if 'return' return a string of the printout 

    Return Value(s):
        String or None

    Related:
        hexdump()

    Author(s):
        Charles Machalow
    '''
    if len(a) != len(b):
        raise ValueError("len(a) must be equal to len(b)!")

    left = hexdump(a, action='return', itemsPerLine=itemsPerLine, itemsTillLineSplit=itemsTillLineSplit, showAscii=showAscii).splitlines()
    right = hexdump(b, showIndexLabel=False, action='return', itemsPerLine=itemsPerLine, itemsTillLineSplit=itemsTillLineSplit, showAscii=showAscii).splitlines()
    buildStr = ''
    for idx, itm in enumerate(left):
        l = left[idx]
        r = right[idx]
        # when checking for a match, remove the index
        match = l.split(' ', 1)[1] == r
        buildStr += "%s | %s | %s\n" % (left[idx], right[idx], '' if match else '!')
        
    if action == 'print':
        print (buildStr)
    elif action == 'return':
        return buildStr
    elif action == 'scroll':
        scrollText(buildStr)
    else:
        raise NotImplementedError
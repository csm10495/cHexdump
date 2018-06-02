import math
import six

def hexdump(sequence, numItems=0, sequenceOffset=0, indexLabelOffset=0, indexLabelMinWidth=4, showIndexLabel=True, showAscii=True, itemsPerLine=16, itemsTillLineSplit=None, action='print'):
    '''
    sequence: thing to print
    numItems: if not 0: the number of items to print. If 0, use len()
    sequenceOffset: Offset to start printing in the sequence
    indexLabelOffset: Offset to start the left side counter on
    indexLabelMinWidth: Min width in characters for the index label
    showIndexLabel:If True, show index label on left
    showAscii: If True, give ascii printout on the right
    itemsPerLine: Number of items per line
    itemsTillLineSplit: Number of items till extra spacing on a given line. If None, use itemsPerLine / 2
    action: If 'print' print the hexdump, if 'return' return a string of the printout 
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
            lineStr += asciiTemplate % tuple([chr(i) if (i < 127 and i > 31) else '.' for i in itemsForThisLine]) 

        lineStr += "\n"

        buildStr += lineStr

    if action == 'print':
        print(buildStr)
    elif action == 'return':
        return buildStr
    else:
        raise NotImplementedError

def sideBySideHexdump(a, b, itemsPerLine=8, itemsTillLineSplit=0, showAscii=True, action='print'):
    left = hexdump(a, action='return', itemsPerLine=itemsPerLine, itemsTillLineSplit=itemsTillLineSplit, showAscii=showAscii).splitlines()
    right = hexdump(b, showIndexLabel=False, action='return', itemsPerLine=itemsPerLine, itemsTillLineSplit=itemsTillLineSplit, showAscii=showAscii).splitlines()
    buildStr = ''
    for idx, itm in enumerate(left):
        l = left[idx]
        r = right[idx]
        # when checking for a match, remove the index
        match = l.split(' ', 1)[1] == r
        buildStr += "%s | %s | %s\n" % (left[idx], right[idx], 'OK' if match else 'BAD')
        
    if action == 'print':
        print (buildStr)
    elif action == 'return':
        return buildStr
    else:
        raise NotImplementedError

    

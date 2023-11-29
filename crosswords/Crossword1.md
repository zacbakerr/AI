# Crosswords 1

This lab is for the creation of a structure that can hold a valid US-style crossword puzzle.
The command line inputs to the script are:
#x# where the two # symbols represent the height and width of the crossword.  The height will be in [3,15] while the width is in [3,30].

'#' where the '#' represents an integer for the number of blocks (black squares) the puzzle must have.

H#x#chars and V#x#chars where the two # symbols are the vertical and horizontal (0 based) position, respectively, of the indicated chars.  An H indicates a horizontal orientation, while a V indicates a vertical one.  These should be processed in the order encountered in the command line.

Example:
8x10 46 V4x0

If no US-style crossword rule precludes it (see below), and if no prior H or V entry precludes it, then any time characters are placed and there is a run of at least 3 on the crossword grid, the ends may be bracketed by a block (or edge).  This does not mandate placement of blocks at such indicated positions, but it may be done.

There will be a series of 11 problems.

Note that the block character is "#" (the use of # above is to indicate a number, and not as a character) and the open character is "-".  Since this might change, In your code, you should not have these inline, but rather set explicitly with:
BLOCKCHAR = "#"
OPENCHAR = "-"

The rules for US-style crosswords:
Block positions must be symmetric with respect to 180 degree rotation about the center.
All letters must be in both a horizontal and vertical word.
All words must be at least three letters.
All non-block entries should be connected.
No duplicate words in the crossword.

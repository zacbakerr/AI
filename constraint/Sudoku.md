Program a sudoku solver.  The command line argument is a file name which will contain 128 sudoku puzzles.  The first 12 are almost trivial, the remainder through the first 51 are usually handled pretty quickly by code, and the remaining ones can sometimes pose a challenge.

The format for the output must be followed closely:
1) The puzzle number (starting from 1) must be printed.
2) The (unsolved) puzzle in the file must be shown as is, on one line.
3) The solution must be shown on the following line
4) The solution must be aligned with the original puzzle
5) A checksum must follow the solution (and be before any elapsed time)
2 & 3 must both be 1 dimensional (single string of length 81).  If you want to print it in 2D, it should follow the solution or be before item 1
1 and 5 must not abut either puzzle but there also must be no intervening numbers between them and the puzzle.  They are not required to be on the same line as either 2 or 3.

The time limit is currently at 60s.
There are no tabs and only a few allowed imports.

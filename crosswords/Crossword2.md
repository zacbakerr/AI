# Crossword 2

Fill out a crossword structure specified on the command line with words from the specified dictionary.
The arguments, are similar to those in XWord1, EXCEPT there is an additional argument in the first position, that of the dictionary to use:

dictToUse.txt HeightxWidth BlockCt V#x#spec ... H#x#spec

The Height and Width identify the size of the crossword while BlockCt specifies the number of blocks.  dictToUse is a file where each word appears on a distinct line.  Any punctuation should be removed from the dictionary words, and all of them should be upper cased.  The remaining items specify letters and/or blocks to place at specific positions in the crossword.

If V#x# or H#x# is given without a spec following, it implies a single block.

The first eight tests currently use 20k.txt dictionary, while the remaining ones use the dictionary that Mr. Eckel provided.  Each test run gets 30 seconds.

Each problem is worth the same amount, and the score for a problem is a fraction where the denominator is twice the number of letters that are to be filled in.  The numerator is given by the sum, for each letter to be filled in, of how many complete, unique words it is in (either 0, 1, or 2)

The majority of the tests are on a 5x5 grid with at least one letter specified.

The final output crossword output is the one that is examined, even if the script times out.   Letters that are not in two distinct words are lower cased in the output shown to the user.  Because of the grading scheme, it might make sense to only show output that is better than any prior output.

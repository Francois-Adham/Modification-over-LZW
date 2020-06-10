# Modification-over-LZW
A modification over Lzw implemented in python.

The case that I am working on is text files without any constrains on the alphabet used or its number.

# The Idea
The idea is to decrease the alphabet used in the text file by calculating the probability of each character and re-arranging the alphabet to have the most frequent characters at the same distance of a selected pivot (the mid of the array), then replace each character in the text file by the distance to the pivot and a bit indicating whether it was in the upper or lower half, then apply any proper lossless compression algorithm on the array of distances – LZW in the delivered code – since the frequent letters are equidistant, then it is more likely to find sequences in the text.

# Sequential Labeling

- HMM

# Input Format
The first column is the char, the second column is the label(BMEO), there is an empty line between two sentences
>N  B
>
>B	M
>
>A	E
>
>D	O
>
>an empty line
>
>Z	O
>
>Z	O
>
>Z	O
>
>Z	O
>
>Z	O

# Output Format
>NBAD\<@\>NBA
>
>ZZZZZ\<@\>

# Installation Dependencies
- python 2.7
- numpy

# References
- https://github.com/chilynn/sequence-labeling

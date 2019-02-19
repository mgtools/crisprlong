#Repository name: crisprlong
##Purpose of this repository
- This repository contains tools for generating spacer graphs from CRISPR arrays predicted from long reads or other resources
##What included (and not included):
- scripts/ -- scripts for clustering spacers, grouping arrays according to shared spacers, and generate spacer graphs from groups of arrays
- third/ -- third party programs (cd-hit-est)
- examples/ -- a folder contains example input file
- dot for plotting (this is not included in the repository so make sure that dot is available on the computer you use to run our tools
##Main scripts
- scripts/array2group.sh -- a bash wrapper that takes a spacer file and generates grouping of CRISPR arrays
- scripts/group2graph.sh -- a bash wrapper that takes output from array2group.sh, and generates graphs
##Usage
- see examples/commands.sh for the two steps application of our tools (array2group.sh & group2graph2.sh)
- go to examples folder, simply call "sh commands.sh" to call the two steps
- if commands.sh completes sucessfully, you shall be able to see three pdf files (spacer graphs) under the module folder
##Explanation of the inputs
- there are two input files, one is the sequence file, and the other one is the spacer prediction
- sequence file in fasta format (e.g.,  examples/SRR2822456-long-sel.fna)
- spacer sequence file (e.g., examples/SRR2822456-long-sel-spacer.fna)
```
>SRR2822456.854604:c1:p6364
TATGTCAATACCACGACTTTTTAACGCTTGGGC
>SRR2822456.854604:c1:p6429
GGCGGTAGCGAAAACACAGCGAACACGGTCAGCGG
```
The first two lines show the name and sequence of a spacer identified from SRR2822456.854604. The spacer name must contain the name of the source sequence, followed the array id, and where the spacer starts in the sequence; for example, SRR2822456.854604:c1:p6364 means the spacer is predicted from SRR2822456.854604, in CRISPR array 1 (c1), and starts at position 6364.
##Main outputs
- after you run commands.sh in the examples folder, you will see these files among others,
- SRR2822456-long-sel-spacer-group.txt -- grouping of the arrays according to shared spacers 
- spacer graphs for CRISPR array groups under module folder
##Other information
- Developers: Yuzhen Ye (yye@indiana.edu) and Tony Lam (tjlam@indiana.edu)
- It is free software under the terms of the GNU General Public License as published by
the Free Software Foundation.

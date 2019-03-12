# Indel
This python script is used for finding indel. 
Though comparing of reference sequence and sequencing DNA, this script will report the all of possible indel in the sequencing DNA

## Requirements
To run this script, you just need a reference sequence and your DNA from high through sequencing.

## Usage
$ python indel.py -i input.txt -o output.txt -r GTTTTGGCGGCGACAAATTCGGATCTTGGCTCACTGCAACCTCCGCCTCCCAGGTTCAAGCGATTCTCCTGCCTCAGCCTCCTGGGTAGCTGGGATTATAGGCACCTGCCACCACGCC -L 40 -R 60

### The options
#### Required:
##### -i, --ifile
This is your DNA sequence file form our first step of selection.
##### -o, --ofile
This is your output file, you can name it by yourself
##### -r, --reference
This is you reference DNA sequence
##### -L, --min_num
This is possible position before indel
##### -R, --max_num
This is possible position after indel

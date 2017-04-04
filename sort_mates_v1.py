__author__ = 'tricho'


import sys
import os
import argparse

'''


this script will run over two paired, unsorted fasta files and sort them so that each header will be in the same
position of its mate in the mate file. This is a part of the pipeline used to extract pairs of orphan reads from fasta
files of reads extracted from specific taxa in megan. prior to this script, the extracted, weighted fasta files are
collapsed, orphan reads are identified, their mates are extracted, and the uncollapsed files are merged (with cat
command) with the mates of the orphans found in the mate library (see pipeline's manual at "procedure_extracting_reads.txt").
It is highly recommended to count the rows, the ">" signs or both, in both mate libraries. the numbers should be
identical. in most cases, rows number will be double than the number of ">".

Synopsis:

python sort_mates.py [fasta_R1.fa] [fasta_R2.fa]
'''

if len(sys.argv) != 3:
    sys.exit("USAGE: python sort_mates.py [fasta_R1.fa] [fasta_R2.fa]")

def openFa (in_fa):

    print "\n" + " open " + in_fa + "..."

    with open(in_fa) as list:
        readFile   = list.readlines()
        fileHandle = {}
        sequence   = ''
        Seq_ID     = ''


        for line in readFile:
            if line[0] == '>':
                if Seq_ID == '':
                    Seq_ID = line.strip('\n').replace(' ', '_')
                else:
                    fileHandle[Seq_ID] = sequence
                    Seq_ID = line.strip('\n').replace(' ', '_')
                    sequence = ''
            else:
                sequence = sequence + line.strip("\n")
    fileHandle[Seq_ID] = sequence
    return fileHandle

############
### main ###
############

R1           = openFa(sys.argv[1])
R2           = openFa(sys.argv[2])
basename_R1  = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]
basename_R2  = os.path.splitext(os.path.split(sys.argv[2])[-1])[0]
#print basename

#Sorted_R1, Sorted_R2 = sort_fasta(R1, R2)


print "\n" + " writing " + basename_R1 + "_sorted.fa..."

sorted_fasta_R1 = sorted(R1.items())
sorted_fasta_R2 = sorted(R2.items())


with open(basename_R1 + '_sorted.fa', 'w') as outFile1:
    for seq in sorted_fasta_R1:
        outFile1.write(str(seq[0]))
        outFile1.write('\n')
        outFile1.write(str(seq[1]))
        outFile1.write('\n')

print "\n" + " writing " + basename_R2 + "_sorted.fa..."

with open(basename_R2 + '_sorted.fa', 'w') as outFile2:
    for seq in sorted_fasta_R2:
        outFile2.write(str(seq[0]))
        outFile2.write('\n')
        outFile2.write(str(seq[1]))
        outFile2.write('\n')
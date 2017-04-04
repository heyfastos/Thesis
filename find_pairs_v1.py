__author__ = 'tricho'


import sys
import os
import argparse

'''


this script will run over two paired fasta files (normally subset of a paired ends library) and extract a list of orphan
reads. The headers of all orphan reads from R1 and R2 files will be written to two new files (each header in a new raw)
so that it will be obvious from which mate is missing. The mates will be later fished from the adapter-free, non-rRNA
fasta files (not from the clustered files of course). Fishing will be done with a different script.

Synopsis:

python find_pairs.py [fasta_R1.fa] [fasta_R2.fa]
'''

if len(sys.argv) != 3:
    sys.exit("USAGE: python find_pairs.py [fasta_R1.fa] [fasta_R2.fa]")

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
                    fileHandle[Seq_ID] = [sequence]
                    Seq_ID = line.strip('\n').replace(' ', '_')
                    sequence = ''
            else:
                sequence = sequence + line.strip("\n")
    fileHandle[Seq_ID] = [sequence]
    return fileHandle


def find_orphans(Fwd, Rev):
    orphan_Fw_mates = []
    orphan_Rev_mates = []
    i = 0
    j = 0

    for ID in Fwd:
        if ID in Rev:
            i += 1
        else:
            orphan_Fw_mates.append(ID)
    for ID in Rev:
        if ID in Fwd:
            j +=1
        else:
            orphan_Rev_mates.append(ID)

    print str(i) + " sequences from  R1 library found mates in R2"
    print str(j) + " sequences from  R2 library found mates in R1"
    return orphan_Fw_mates, orphan_Rev_mates


############
### main ###
############
R1           = openFa(sys.argv[1])
R2           = openFa(sys.argv[2])
basename_R1  = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]
basename_R2  = os.path.splitext(os.path.split(sys.argv[2])[-1])[0]

Reads_missing_inR1, Reads_missing_inR2 = find_orphans(R1, R2)


print "\n" + "writing " + basename_R1 + "_orphans.txt..."

with open(basename_R1 + '_orphans.txt', 'w') as outFile1:
    for ID in Reads_missing_inR1:
        outFile1.write(ID)
        outFile1.write('\n')

print "\n" + "writing " + basename_R2 + "_orphans.txt..."

with open(basename_R2 + '_orphans.txt', 'w') as outFile2:
    for ID in Reads_missing_inR2:
        outFile2.write(ID)
        outFile2.write('\n')

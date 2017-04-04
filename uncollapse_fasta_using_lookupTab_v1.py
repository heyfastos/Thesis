__author__ = 'tricho'


import sys
import os
#import argparse

'''
I decided to simplify the procedure: This script is meant to deal with a situation in which reads assigned to a certain
taxonomic group are extracted (using MEGAN for example) from both FW and REV libraries. In the next step, i want to
perform mapping to reference genomes using paired ends information, however not always both pairs are assigned to the
taxon. i decided to be permissive - in case a single of a mate is extracted, his mate will be searched for and added to
the mapping input (if the assignment is false, it will be removed from the results in the mapping step). A problem
emerge when using uni-clusters because they make the use of paired ends information impossible. The script will go over
all headers in the fasta and search for headers with wight >1. When finding a header like that, it will find it in the
auto-generated lookup table (nci file - Steffen Lott's uni-clustering script) and uncollapse the cluster. The output
fasta will be sorted according to the headers (normally, SortMeRNA output headers are simply running numbers). The next
step is to compare FW and REV uncollapsed fastas and fish missing sequences in each library. This will be done by a
different script


Synopsis:

python uncollapse_fasta_using_lookupTab_v1.py [fasta.fa] [lookup_table.icn]
'''

if len(sys.argv) != 3:
    sys.exit("USAGE: python uncollapse_fasta_using_lookupTab_v1.py [fasta.fa] [lookup_table.icn]")

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


# The function opening the lookup table will create a dictionary only of clusters with more than one header in them!
# if a sequence appears uniquely in the library, I will just remove the _weight|1 from the header later on

def openTab(lookupTab):

    print "\n" + " open " + lookupTab + "..."

    with open(lookupTab) as table:
        readFile = table.readlines()
        fileHandle = {}

        for line in readFile:
            #print len(line.split('\t')[1].split(';'))
            #check if there is more than one header in cluster
            if len(line.split('\t')[1].split(';')) > 1:
                ID_list = line.split('\t')[1].strip('\n').split(';')
                fileHandle[ID_list[0]] = ID_list
    return fileHandle


def looking_up(fasta, lookup):
    uncollapsed_fasta = {}
    #print lookup
    for header in fasta:
        # Is this a singelton?
        if int(header.split('|')[1]) == 1:
            # Add entry to uncollapsed fasta without the "_weights|1" string of the header
            uncollapsed_fasta[header.split('_')[0]] = fasta[header]
        else:
            if not header.split('_')[0] in lookup:
                sys.exit("WARNING!!!! header " + header + " with weights >1 not in lookup table!!!!!")
            else:
                # All seqs in cluster are identical, so add to uncollapsed fasta all IDs in the cluster, each pointing
                # to the sequence of the cluster (its 100% identity!)
                for ID in lookup[header.split('_')[0]]:
                    uncollapsed_fasta[ID] = fasta[header]

    return uncollapsed_fasta





############
### main ###
############


fasta       = openFa(sys.argv[1])
lookup      = openTab(sys.argv[2])
uncollapsed = looking_up(fasta, lookup)
basename    = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]


print "\n" + " writing " + basename + "_uncollapsed.fa..."

sorted_fasta = sorted(uncollapsed.items())
with open(basename + '_uncollapsed.fa', 'w') as outFile:
    for seq in sorted_fasta:
        outFile.write(str(seq[0]))
        outFile.write('\n')
        outFile.write(uncollapsed[str(seq[0])][0])
        outFile.write('\n')

#!/usr/bin/python

import os,sys, re

'''
This Script runs over one FASTA file and one TAB file and compares them. for each ID that is present in both files the
ID and its sequence will be extracted and written into an output fasta.
The TAB file must contain the headers the user wants to extract in the first column. a single column is allowed.

IMPORTANT!
This script was wrotten to extract mate reads of orphan reads. this means that reads must be fished from the MATE fasta
file (if orphans are from R1, use the fasta of R2)

Synopsis:

python get_reads_from_fasta.py [tab_file] [fasta]
'''

if len(sys.argv) != 3:
    sys.exit("USAGE: python get_reads_from_fasta.py [tab_file] [fasta]")



# open TAB file and create a list of headers
def import_list(inputFileName):
    with open(inputFileName) as list:
        readFile=list.readlines()
        fileHandle = []
        for line in readFile:
            if line.startswith(">"):
                fileHandle.append(line.strip('\n'))
            else:
                print "WARNING! " + line + " is not a valid fasta header!!!!"
    return fileHandle

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
    
    # fileHandle: {ID:seq, ID:seq, ...}
    return fileHandle

def extractSeqs (lTab, dFasta):
    extractedFasta = {}

    #save all ID's in ASC list as dictionary's keys
    for line in lTab:
        if line in dFasta:
            extractedFasta[line] = dFasta[line]
        else:
            print "SEVERE WARNING!!! no mate was found for " + line + "!!!!!"
    return extractedFasta

    ####MAIN####

Header_list = sys.argv[1]
lTab        = import_list(Header_list)
fasta       = sys.argv[2]
dFasta      = openFa(fasta)
dExtracted  = extractSeqs (lTab, dFasta)
basename    = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]

print "\n" + " Writing " +"fished_mates_for_DCM_" + basename +".fa"


with open("fished_mates_for_" + basename +".fa", 'w') as outFile:
    for entry in dExtracted:
        outFile.write(entry)
        outFile.write('\n')
        outFile.write(dExtracted[entry])
        outFile.write('\n')

__author__ = 'tricho'


import sys
import os

'''
this script will run over BLAST tab output and pick only the 10 best hits for each query (in case more than 10 exist)

Command:

python reduce_tab_size.py [alignment_table]
'''

if len(sys.argv) != 2:
    sys.exit('USAGE:  python reduce_tab_size.py [alignment_table]')


############
### main ###
############

print "\n open " + sys.argv[1] + "..."

with open(sys.argv[1]) as list:
    readFile = list.readlines()

basename = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]

print "\n" + " writing " + basename + "_reduced.tab..."
query  = 'foo'

i = 1  # the index will be used to count hits assigned to query, so that the number of hits can be limited to 10

with open(basename + '_reduced.tab', 'w') as outFile:
    for line in readFile:
        if line.startswith('#'):
            continue
        else:          
            if line.split("\t")[0] == query:  # this is not the first hit for this query. check counter!
                if i < 10:        # counter is less than 10 - write the hit's line to the output file.
                    outFile.write(line.split("\t")[0])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[1])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[2])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[3])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[4])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[5])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[6])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[7])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[8])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[9])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[10])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[11])
                    outFile.write('\t')
                    outFile.write(line.split("\t")[12])
                    outFile.write('\n')
                    # now increment counter - limit is 10 hits per query.
                    i += 1
                else:  # counter is >10: this line is of a hit that ia below the 10 best. excluded from the output and check
                       # if next line is still the same query.
                    continue
            else:  # this is the first hit for the respective query : change the query variable, start the counter again and
                   # print this line to output file
                query = line.split("\t")[0]
                i=1
                outFile.write(line.split("\t")[0])
                outFile.write('\t')
                outFile.write(line.split("\t")[1])
                outFile.write('\t')
                outFile.write(line.split("\t")[2])
                outFile.write('\t')
                outFile.write(line.split("\t")[3])
                outFile.write('\t')
                outFile.write(line.split("\t")[4])
                outFile.write('\t')
                outFile.write(line.split("\t")[5])
                outFile.write('\t')
                outFile.write(line.split("\t")[6])
                outFile.write('\t')
                outFile.write(line.split("\t")[7])
                outFile.write('\t')
                outFile.write(line.split("\t")[8])
                outFile.write('\t')
                outFile.write(line.split("\t")[9])
                outFile.write('\t')
                outFile.write(line.split("\t")[10])
                outFile.write('\t')
                outFile.write(line.split("\t")[11])
                outFile.write('\n')
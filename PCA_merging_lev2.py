__author__ = 'Dan'


import sys
import os
import glob
'''
Second step in preparing the input for PCA analysis. This script will receive a table for each treatment and merge them
all to create the Final input format.

make sure the folder you use contain ONLY the script and the relevant tables named with a .tab suffix.

Usage python Whisky_formatting_lev2 [outFile_name]
'''

# if len(sys.argv) != 2:
  #  sys.exit('Usage: python Whisky_formatting_lev2.py [outFile_name]    * please make sure you only include the files '
   #          'you wish to process in your working folder, and that they all have the suffix \'.tab\'')


dOUT = dict()


with open(glob.glob('*C_*')[0]) as list_c:   # open the control table and save for each taxon each time point in a
                                          # separate list
    print 'opening ' + glob.glob('*C_*')[0] + '...'
    readFile   = list_c.readlines()
    for line in readFile[1:]:
        if len(line.split('\t')) != 6:
            sys.exit('Input Error: input format should be Taxon \t rpm_T-1 \t rpm_T1 \t rpm_T3 \t rpm_T6 \t rpm_T10')
        else:
            #print line.strip('\n').split('\t')[1:]
            dOUT[line.split('\t')[0]] = []
            for timeP in line.strip('\n').split('\t')[1:]:
                dOUT[line.split('\t')[0]].append(timeP)    # Taxon = open list for each time point in condition C


with open(glob.glob('*W_*')[0]) as list_w:
    print 'opening ' + glob.glob('*W_*')[0] + '...'
    readFile   = list_w.readlines()
    for line in readFile[1:]:
        if len(line.split('\t')) != 6:
            sys.exit('Input Error: input format should be Taxon \t rpm_T-1 \t rpm_T1 \t rpm_T3 \t rpm_T6 \t rpm_T10')
        else:
            if line.split('\t')[0] in dOUT:   # Taxa / functions that exists in all conditions
                for timeP in line.strip('\n').split('\t')[1:]:
                    dOUT[line.split('\t')[0]].append(timeP)

            else:   # For Taxa / functions that were not detected at all in condition C
                dOUT[line.split('\t')[0]] = [0, 0, 0, 0, 0]
                for timeP in line.strip('\n').split('\t')[1:]:
                        dOUT[line.split('\t')[0]].append(timeP)

    for line in dOUT:
        if not len(dOUT[line]) == 10:
            if len(dOUT[line]) == 5:
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
            else:
                print line
                print dOUT[line]
                sys.exit("Processing error: line contains wrong number of entries")

with open(glob.glob('*OA_*')[0]) as list_oa:
    print 'opening ' + glob.glob('*OA_*')[0] + '...'
    readFile   = list_oa.readlines()
    for line in readFile[1:]:
        if len(line.split('\t')) != 6:
            sys.exit('Input Error: input format should be Taxon \t rpm_T-1 \t rpm_T1 \t rpm_T3 \t rpm_T6 \t rpm_T10')
        else:
            if line.split('\t')[0] in dOUT:    # see the above 'with open' section for details
                for timeP in line.strip('\n').split('\t')[2:]:  # skip taxon name and the T-1 which is the C T-1 sample!
                    dOUT[line.split('\t')[0]].append(timeP)

            else:   # For Taxa / functions that were not detected at all in conditions C and W
                dOUT[line.split('\t')[0]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for timeP in line.strip('\n').split('\t')[2:]:  # skip taxon name and the T-1 which is the C T-1 sample!
                        dOUT[line.split('\t')[0]].append(timeP)

    for line in dOUT:
        if not len(dOUT[line]) == 14:
            if len(dOUT[line]) == 10:
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
            else:
                print line
                print dOUT[line]
                sys.exit("Processing error: line contains wrong number of entries")


with open(glob.glob('*GH_*')[0]) as list_gh:
    print 'opening ' + glob.glob('*GH_*')[0] + '...'
    readFile   = list_gh.readlines()
    for line in readFile[1:]:
        if len(line.strip(',').split('\t')) != 6:
            sys.exit('Input Error: input format should be Taxon \t rpm_T-1 \t rpm_T1 \t rpm_T3 \t rpm_T6 \t rpm_T10')
        else:
            if line.split('\t')[0] in dOUT:    # see the above 'with open' section for details
                for timeP in line.strip('\n').split('\t')[2:]:  # skip taxon name and the T-1 which is the W T-1 sample!
                    dOUT[line.split('\t')[0]].append(timeP)

            else:   # For Taxa / functions that were not detected at all in conditions C, W and OA
                dOUT[line.split('\t')[0]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for timeP in line.strip('\n').split('\t')[2:]:  # skip taxon name and the T-1 which is the W T-1 sample!
                        dOUT[line.split('\t')[0]].append(timeP)
    for line in dOUT:
        if not len(dOUT[line]) == 18:
            if len(dOUT[line]) == 14:
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
                dOUT[line].append(0)
            else:
                print line
                print dOUT[line]
                sys.exit("Processing error: line contains wrong number of entries")

print "\n Writing " + sys.argv[1] +"..."

with open (sys.argv[1], 'w') as outTab:
    outTab.write("Taxon")
    outTab.write("\t")
    outTab.write("C_T-1")
    outTab.write("\t")
    outTab.write("C_T1")
    outTab.write("\t")
    outTab.write("C_T3")
    outTab.write("\t")
    outTab.write("C_T6")
    outTab.write("\t")
    outTab.write("C_T10")
    outTab.write("\t")
    outTab.write("W_T-1")
    outTab.write("\t")
    outTab.write("W_T1")
    outTab.write("\t")
    outTab.write("W_T3")
    outTab.write("\t")
    outTab.write("W_T6")
    outTab.write("\t")
    outTab.write("W_T10")
    outTab.write("\t")
    outTab.write("OA_T1")
    outTab.write("\t")
    outTab.write("OA_T3")
    outTab.write("\t")
    outTab.write("OA_T6")
    outTab.write("\t")
    outTab.write("OA_T10")
    outTab.write("\t")
    outTab.write("GH_T1")
    outTab.write("\t")
    outTab.write("GH_T3")
    outTab.write("\t")
    outTab.write("GH_T16")
    outTab.write("\t")
    outTab.write("GH_T10")
    outTab.write("\n")
    for taxon in dOUT:
        outTab.write(taxon)
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][0]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][1]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][2]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][3]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][4]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][5]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][6]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][7]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][8]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][9]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][10]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][11]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][12]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][13]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][14]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][15]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][16]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][17]))
        outTab.write('\n')
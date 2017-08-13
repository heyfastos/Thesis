__author__ = 'Dan'


import sys
import os
import glob
'''
Second step in preparing the input for the Whisky visualization tool (S. Lott). The tool will recieve a table for each
treatment and merge them all to create the Final input format.

PLEASE NOTE!!! The delta between '0' rpm in T-1 and '0' rpm in T10 is the same delta as '1000' rpm in T-1 and '1000'
rmp in T10. This pipeline does not tell you ANYTHING about the real values (who was abundant and who was not). It
focuses on te changes that occurred in the population.

Input table format:

Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t delta_rpm_T6 \t delta_rpm_T10

Output table format:

Taxon/Function \t C_dT1,W_dT1,OA_dT1,GH_dT1 \t C_dT3,W_dT3,OA_dT3,GH_dT3 \t C_dT6,W_dT6,OA_dT6,GH_dT6 \t
C_dT10,W_dT10,OA_dT10,GH_dT10

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
        if len(line.split('\t')) != 5:
            sys.exit('Input Error: input format should be Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t '
                     'delta_rpm_T6 \t delta_rpm_T10')
        else:
            #print line.strip('\n').split('\t')[1:]
            dOUT [line.split('\t')[0]] = []
            for timeP in line.strip('\n').split('\t')[1:]:
                dOUT[line.split('\t')[0]].append([timeP])    # Taxon = open list for each time point in condition C


with open(glob.glob('*W_*')[0]) as list_w:
    print 'opening ' + glob.glob('*W_*')[0] + '...'
    readFile   = list_w.readlines()
    for line in readFile[1:]:
        if len(line.split('\t')) != 5:
            sys.exit('Input Error: input format should be Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t '
                     'delta_rpm_T6 \t delta_rpm_T10')
        else:
            if line.split('\t')[0] in dOUT:   # Most Taxa / functions are supposed to exists in all conditions but
                                                # this is not a necessity
                dOUT[line.split('\t')[0]][0].append(line.strip(',').split('\t')[1])   # append the value in pos [1]
                                                                                      # (dT1) to the [0]st list
                                                                                      # containing T1 values. repeat for
                                                                                      # all time points.
                dOUT[line.split('\t')[0]][1].append(line.strip(',').split('\t')[2])
                dOUT[line.split('\t')[0]][2].append(line.strip(',').split('\t')[3])
                dOUT[line.split('\t')[0]][3].append(line.strip(',').strip('\n').split('\t')[4])

            else:   # For Taxa / functions that were not detected at all in condition C
                dOUT[line.split('\t')[0]] = []
                for timeP in line.strip('\n').split('\t')[1:]:
                        dOUT [line.split('\t')[0]].append([0, timeP])    # Taxon = add to each list (one for each
                                                                         # time point) a '0' for condition "C" and
                                                                         # the dRPM for condition W.
    for line in dOUT:    # in case of of the time points in the "W" treatment contained a taxon, it will be completely
                         # absent in the "W" table. If this taxon was present in the "C" table, it will result in time
                         # points with only one treatment sub column instead of two after reading the W table. add '0'
                         # to the W values.
        if len(dOUT[line][0]) == 1:
            dOUT[line][0].append(0)
            dOUT[line][1].append(0)
            dOUT[line][2].append(0)
            dOUT[line][3].append(0)

with open(glob.glob('*OA_*')[0]) as list_oa:
    print 'opening ' + glob.glob('*OA_*')[0] + '...'
    readFile   = list_oa.readlines()
    for line in readFile[1:]:
        if len(line.split('\t')) != 5:
            sys.exit('Input Error: input format should be Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t '
                     'delta_rpm_T6 \t delta_rpm_T10')
        else:
            if line.split('\t')[0] in dOUT:    # see the above 'with open' section for details
                dOUT[line.split('\t')[0]][0].append(line.strip(',').split('\t')[1])
                dOUT[line.split('\t')[0]][1].append(line.strip(',').split('\t')[2])
                dOUT[line.split('\t')[0]][2].append(line.strip(',').split('\t')[3])
                dOUT[line.split('\t')[0]][3].append(line.strip(',').strip('\n').split('\t')[4])

            else:   # For Taxa / functions that were not detected at all in conditions C and W
                dOUT[line.split('\t')[0]] = []
                for timeP in line.strip('\n').split('\t')[1:]:
                        dOUT [line.split('\t')[0]].append([0, 0, timeP])    # Taxon = add to each list (one for each
                                                                            # time point) two '0' for all previous
                                                                            # conditions and RPM for condition OA.
    for line in dOUT:
        if len(dOUT[line][0]) == 2:
            dOUT[line][0].append(0)
            dOUT[line][1].append(0)
            dOUT[line][2].append(0)
            dOUT[line][3].append(0)


with open(glob.glob('*GH_*')[0]) as list_gh:
    print 'opening ' + glob.glob('*GH_*')[0] + '...'
    readFile   = list_gh.readlines()
    for line in readFile[1:]:
        if len(line.strip(',').split('\t')) != 5:
            sys.exit('Input Error: input format should be Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t '
                     'delta_rpm_T6 \t delta_rpm_T10')
        else:
            if line.split('\t')[0] in dOUT:    # see the above 'with open' section for details
                dOUT[line.split('\t')[0]][0].append(line.strip(',').split('\t')[1])
                dOUT[line.split('\t')[0]][1].append(line.strip(',').split('\t')[2])
                dOUT[line.split('\t')[0]][2].append(line.strip(',').split('\t')[3])
                dOUT[line.split('\t')[0]][3].append(line.strip(',').strip('\n').split('\t')[4])

            else:   # For Taxa / functions that were not detected at all in conditions C and W
                dOUT[line.split('\t')[0]] = []
                for timeP in line.strip('\n').split('\t')[1:]:
                        dOUT [line.split('\t')[0]].append([0, 0, 0, timeP])    # Taxon = add to each list (one for
                                                                               # each time point) two '0' for all
                                                                               # previous conditions and RPM for
                                                                               # condition GH.
    for line in dOUT:
        if len(dOUT[line][0]) == 3:
            dOUT[line][0].append(0)
            dOUT[line][1].append(0)
            dOUT[line][2].append(0)
            dOUT[line][3].append(0)

print "\n Writing " + sys.argv[1] +"..."

with open (sys.argv[1], 'w') as outTab:
    outTab.write("#all values are given in delta(d) rpm relative to T-1\n")
    outTab.write("#columns: dT1, dT3, dT6,dT10 \n")
    outTab.write("#sub_columns: Control, Warming, Ocean acidification, Green house \n")
    for taxon in dOUT:
        outTab.write(taxon)
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][0][0]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][0][1]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][0][2]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][0][3]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][1][0]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][1][1]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][1][2]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][1][3]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][2][0]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][2][1]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][2][2]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][2][3]))
        outTab.write('\t')
        outTab.write(str(dOUT[taxon][3][0]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][3][1]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][3][2]))
        outTab.write(',')
        outTab.write(str(dOUT[taxon][3][3]))
        outTab.write('\n')
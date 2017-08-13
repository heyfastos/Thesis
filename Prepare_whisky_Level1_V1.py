__author__ = 'Dan'


import sys
import os
import glob

'''
This script is the first step in preparing the input table for "Whisky" (S. Lott)
It will run over all tables (each table is a sample taken in a different time point) of a certain condition and include
them all in one table. Data are presented in difference in rpm relative to T-1.

{Taxon_1 = [delta_rpm_T1 , delta_rpm_T3, delta_rpm_T6, delta_rpm_T10], Taxon_2 = [ ... ]...}

Command: python Prepare_whisky_St1.py [outPut_table_name.tab]

'''

if len(sys.argv) != 2:
    sys.exit("Usage: python Prepare_whisky_St1.py [outPut_table_name.tab]")

# Open T-1 and calculate rpm for each taxon
dTminus1 = dict()
for filename in glob.glob('*T-1*'):

    print "\n open " + filename + "..."

    with open(filename) as list:
        readFile   = list.readlines()
        if not len(readFile[0].split("\t")) == 2:
            sys.exit("ERROR: file format is inappropriate. Note that first line must have the following format - "
                     "Total'\t'X   where X is the total number of reads in the T-1 library")
        elif not readFile[0].split("\t")[0] == "Total":
            sys.exit("ERROR: file format is inappropriate. Note that first line must have the following format - "
                     "Total'\t'X   where X is the total number of reads in the T-1 library")
        else:
            #print readFile[0].split("\t")[0]
            TotalReads = int(readFile[0].split("\t")[1])

        print "\n calculating rpm for all taxa in T-1..."
        for line in readFile[1:]:
            if not len(line.split("\t")) == 2:
                print "\n Format Error in line " + str(readFile.index(line)+1)
                sys.exit("FATAL ERROR: file format is inappropriate. Note that each line must have the following format"
                         " Taxon_X'\t'X   where X is the total number of reads assigned to Taxon_X")

            else:
                Taxon = line.replace(' ', '_').split('\t')[0]
                Tax_reads = int(line.split('\t')[1])

                dTminus1[Taxon] = Tax_reads*1000000/TotalReads  # calculate rpm for each taxon in T-1
dT1  = dict()
dT3  = dict()
dT6  = dict()
dT10 = dict()

for Timepoint in  glob.glob('*T*'):
    if "T-1" not in Timepoint:
        print "\n opening " + Timepoint +"..."

        with open(Timepoint) as list:
            readT = list.readlines()
            if not len(readT[0].split("\t")) == 2:
                sys.exit("ERROR: file format is inappropriate. Note that first line must have the following format "
                         "- Total'\t'X where X is the total number of reads in the library")
            elif not readT[0].split("\t")[0] == "Total":
                sys.exit("ERROR: file format is inappropriate. Note that first line must have the following format"
                         " - Total'\t'X where X is the total number of reads in the library")
            else:
                TotalReads = int(readT[0].split("\t")[1])

            if "T10" in Timepoint:
                print "\n calculating rpm for each taxon in " + Timepoint
                for line in readT[1:]:
                    if not len(line.split("\t")) == 2:
                        print "\n Format Error in line " + str(readT.index(line)+1)
                        sys.exit("FATAL ERROR: file format is inappropriate. Note that each line must have the "
                                 "following format: Taxon_X'\t'X where X is the total number of reads assigned to "
                                 "Taxon_X")
                    else:
                        Taxon = line.replace(' ', '_').split('\t')[0]
                        Tax_reads = int(line.split('\t')[1])

                        dT10[Taxon] = Tax_reads*1000000/TotalReads  # calculate rpm for each taxon in T10

            elif "T3_" in Timepoint:
                print "\n calculating rpm for each taxon in " + Timepoint
                for line in readT[1:]:
                    if not len(line.split("\t")) == 2:
                        print line
                        sys.exit("ERROR: file format is inappropriate. Note that each line must have the following "
                                 "format: Taxon_X'\t'X where X is the total number of reads assigned to Taxon_X")
                    else:
                        Taxon = line.replace(' ', '_').split('\t')[0]
                        Tax_reads = int(line.split('\t')[1])
                        dT3[Taxon] = Tax_reads*1000000/TotalReads  # calculate rpm for each taxon in T3

            elif "T6" in Timepoint:
                print "\n calculating rpm for each taxon in " + Timepoint
                for line in readT[1:]:
                    if not len(line.split("\t")) == 2:
                        print "\n Format Error in line " + str(readT.index(line)+1)
                        sys.exit("FATAL ERROR: file format is inappropriate. Note that each line must have the "
                                 "following format: Taxon_X'\t'X where X is the total number of reads assigned to "
                                 "Taxon_X")
                    else:
                        Taxon = line.replace(' ', '_').split('\t')[0]
                        Tax_reads = int(line.split('\t')[1])

                        dT6[Taxon] = Tax_reads*1000000/TotalReads  # calculate rpm for each taxon in T6

            elif "T1" in Timepoint and "T10" not in Timepoint: # special case for T1 - exclude T10 lines!
                print "\n calculating rpm for each taxon in " + Timepoint
                for line in readT[1:]:
                    if not len(line.split("\t")) == 2:
                        print "\n Format Error in line " + str(readT.index(line)+1)
                        sys.exit("FATAL ERROR: file format is inappropriate. Note that each line must have the "
                                 "following format: Taxon_X'\t'X where X is the total number of reads assigned to "
                                 "Taxon_X")
                    else:
                        Taxon = line.replace(' ', '_').split('\t')[0]
                        Tax_reads = int(line.split('\t')[1])

                        dT1[Taxon] = Tax_reads*1000000/TotalReads  # calculate rpm for each taxon in T1

##########################
### Build output table ###
##########################

Output_table = dict()

for taxon in dT1:
    if taxon in dTminus1:
        Output_table[taxon] = [int(dT1[taxon] - dTminus1[taxon])]
    else:  # if the taxon is not present in T-1 just add the rpm value of the respective time point (its an increase
           # relative to T-1)
        Output_table[taxon] = [int(dT1[taxon])]

for taxon in dT3:
    if taxon in Output_table: # a taxon that appeared in one of the tables iterated over so far.
        if taxon in dTminus1:
            Output_table[taxon].append(int(dT3[taxon] - dTminus1[taxon]))
        else:
            Output_table[taxon].append(int(dT3[taxon]))  # a taxon that did not appear in any table so far.
    else:
        Output_table[taxon] = [0, int(dT3[taxon])]       # add a change of '0' for T1 because in both T-1 and T1
                                                         # this taxon is missing

for taxon in dT6:
    if taxon in Output_table: # a taxon that appeared in one of the tables iterated over so far.
        if taxon in dTminus1:
            Output_table[taxon].append(int(dT6[taxon] - dTminus1[taxon]))
        else:
            Output_table[taxon].append(int(dT6[taxon]))
    else:
        Output_table[taxon] = [0, 0, int(dT6[taxon])]    # add a change of '0' for T1 and T3 because in both T-1, T1
                                                             # and T3 this taxon is missing

for taxon in dT10:
    if taxon in Output_table: # a taxon that appeared in one of the tables iterated over so far.
        if taxon in dTminus1:
            Output_table[taxon].append(int(dT10[taxon] - dTminus1[taxon]))
        else:
            Output_table[taxon].append(int(dT10[taxon]))
    else:
        Output_table[taxon] = [0, 0, 0, int(dT10[taxon])]    # add a change of '0' for T1 T3 and T6 because in both
                                                                 # T-1,T1, T3 and T6 this taxon is missing


# The code above may lead to a situation in which a taxon that exist in the early time points and disappears later will
# have less delta numbers in its respective slot in the dictionary (if there is a taxon in T1 but not in the others, it
# will receive a delta for T1 but further slots will remain empty. The next chunk of code will fix it - but not in a
# very "elegant" way.

for key in Output_table:
    if len(Output_table[key]) == 1:
        Output_table[key].append(0)
        Output_table[key].append(0)
        Output_table[key].append(0)
    elif len(Output_table[key]) == 2:
        Output_table[key].append(0)
        Output_table[key].append(0)
    elif len(Output_table[key]) == 3:
        Output_table[key].append(0)
    elif len(Output_table[key]) > 4:
        sys.exit("ERROR: bad output. please check line " + Output_table[key])

OutName = sys.argv[1]

print "\n Writing " + OutName + "..."

with open(OutName , 'w') as outTab:
    outTab.write("Taxon")
    outTab.write('\t')
    outTab.write('delta_rpm_T1')
    outTab.write('\t')
    outTab.write('delta_rpm_T3')
    outTab.write('\t')
    outTab.write('delta_rpm_T6')
    outTab.write('\t')
    outTab.write('delta_rpm_T10')
    outTab.write('\n')
    for taxon in Output_table:
        outTab.write(taxon)
        outTab.write('\t')
        outTab.write(str(Output_table[taxon][0]))
        outTab.write('\t')
        outTab.write(str(Output_table[taxon][1]))
        outTab.write('\t')
        outTab.write(str(Output_table[taxon][2]))
        outTab.write('\t')
        outTab.write(str(Output_table[taxon][3]))
        outTab.write('\n')
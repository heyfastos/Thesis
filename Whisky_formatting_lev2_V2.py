__author__ = 'Dan'


import sys
import os
import glob
import argparse
from math import fabs, log, pow, exp
'''
Second step in preparing the input for the Whisky visualization tool (S. Lott). The tool will recieve a table for each
treatment and merge them all to create the Final input format.

PLEASE NOTE!!! The delta between '0' rpm in T-1 and '0' rpm in T10 is the same delta as '1000' rpm in T-1 and '1000'
rmp in T10. This pipeline does not tell you ANYTHING about the real values (who was abundant and who was not). It
focuses only on changes in abundances.

Input table format:

Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t delta_rpm_T6 \t delta_rpm_T10

Output table format:

Taxon/Function \t C_dT1,W_dT1,OA_dT1,GH_dT1 \t C_dT3,W_dT3,OA_dT3,GH_dT3 \t C_dT6,W_dT6,OA_dT6,GH_dT6 \t
C_dT10,W_dT10,OA_dT10,GH_dT10

make sure the folder you use contain ONLY the script and the relevant tables named with a .tab suffix.

Usage python Whisky_formatting_lev2 -l [type of log to apply. script supports: log2, log10, ln and no log - na]
-o [outFile_name]
'''

#if len(sys.argv) != 2:
#   sys.exit('Usage: python Whisky_formatting_lev2.py [outFile_name]    * please make sure you only include the files '
#           'you wish to process in your working folder, and that they all have the suffix \'.tab\'')

dOUT = dict()

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log_type", help="log-type: 'na' , 'log2' , 'log10' , 'ln' (default: log2)", type=str,
                    required=True, default="log2")
parser.add_argument("-o", "--output_file", help="output file name. default: WhiskyOut.txt", type=str,
                    default="WhiskyOut.txt")
parser.add_argument("-t", "--Title", help = "This argument will determine the Title of your graphic when later using "
                    "WHISKY", type = str, required = True)
args = parser.parse_args()

with open(glob.glob('*C_*')[0]) as list_c:   # open the control table and save for each taxon each time point in a
                                          # separate list
    print 'opening ' + glob.glob('*C_*')[0] + '...'
    readFile   = list_c.readlines()
    for line in readFile[1:]:
        if len(line.split('\t')) != 5:
            sys.exit('Input Error: input format should be Taxon/Function \t delta_rpm_T1 \t delta_rpm_T3 \t '
                     'delta_rpm_T6 \t delta_rpm_T10')
        else:
            # create an entry in the dOUT dictionary
            dOUT [line.split('\t')[0]] = []
            if args.log_type == 'log2':
                for timeP in line.strip('\n').split('\t')[1:]:
                    # Taxon = open list for each time point in condition C (that's the reason for the square brackets)
                    if int(timeP) > 0:
                        dOUT[line.split('\t')[0]].append([log(int(timeP), 2)])
                    elif int(timeP) < 0:
                        dOUT[line.split('\t')[0]].append([-log(abs(int(timeP)), 2)])
                    else:
                        dOUT[line.split('\t')[0]].append([0])

            elif args.log_type == 'log10':
                for timeP in line.strip('\n').split('\t')[1:]:
                    if int(timeP) > 0:
                        dOUT[line.split('\t')[0]].append([log(int(timeP), 10)])
                    elif int(timeP) < 0:
                        dOUT[line.split('\t')[0]].append([-log(abs(int(timeP)), 10)])
                    else:
                        dOUT[line.split('\t')[0]].append([0])

            elif args.log_type == 'ln':
                for timeP in line.strip('\n').split('\t')[1:]:
                    if int(timeP) > 0:
                        dOUT[line.split('\t')[0]].append([log(int(timeP))])
                    elif int(timeP) < 0:
                        dOUT[line.split('\t')[0]].append([-log(abs(int(timeP)))])
                    else:
                        dOUT[line.split('\t')[0]].append([0])
            elif args.log_type == 'na':  # if you are not using "log" there is no reason to perform all this circus of
                                         # negative numbers ect.
                for timeP in line.strip('\n').split('\t')[1:]:
                    dOUT[line.split('\t')[0]].append([timeP])

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
                # 1) append value in pos [1] (dT1) to the [0]st list containing T1 values. repeat for all time points.
                # 2) consider log type!
                if args.log_type == 'log2':
                    # following 3 statements only regard the first timepoint in the line...
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1]), 2))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1])), 2))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2]), 2))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2])), 2))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3]), 2))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3])), 2))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4]), 2))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4])), 2))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'log10':
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1]), 10))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1])), 10))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2]), 10))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2])), 10))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3]), 10))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3])), 10))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4]), 10))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4])), 10))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'ln':
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1])))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1]))))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2])))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2]))))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3])))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3]))))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4])))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4]))))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'na':  # if you are not using "log" there is no reason to perform all this circus
                                                     # of negative numbers ect.
                    dOUT[line.split('\t')[0]][0].append(line.strip(',').split('\t')[1])
                    dOUT[line.split('\t')[0]][1].append(line.strip(',').split('\t')[2])
                    dOUT[line.split('\t')[0]][2].append(line.strip(',').split('\t')[3])
                    dOUT[line.split('\t')[0]][3].append(line.strip(',').strip('\n').split('\t')[4])



            else:   # For Taxa / functions that were not detected at all in condition C.
                dOUT[line.split('\t')[0]] = []
                for timeP in line.strip('\n').split('\t')[1:]:
                    # Add to each list (one for each time point) a '0' for condition "C" and the logged dRPM value for
                    # condition W.
                    if args.log_type == 'log2':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, log(int(timeP), 2)])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, -log(abs(int(timeP)), 2)])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0])

                    elif args.log_type == 'log10':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, log(int(timeP), 10)])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, -log(abs(int(timeP)), 10)])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0])

                    elif args.log_type == 'ln':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, log(int(timeP))])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, -log(abs(int(timeP)))])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0])

                    elif args.log_type == 'na':
                        dOUT[line.split('\t')[0]].append([0, int(timeP)])

    for line in dOUT:    # If a taxon was absent in the "W" treatment but present in the "C" table, dOUT will contain
                         # time points with only one treatment sub column instead of two after reading the W table.
                         # Add '0' to the W values in such cases.
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
            if line.split('\t')[0] in dOUT:    # add for each taxon its values to the respective time point in dOUT.
                                               # Consider the log type!
                if args.log_type == 'log2':
                    # following 3 statements only regard the first timepoint in the line...
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1]), 2))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1])), 2))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2]), 2))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2])), 2))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3]), 2))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3])), 2))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4]), 2))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4])), 2))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'log10':
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1]), 10))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1])), 10))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2]), 10))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2])), 10))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3]), 10))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3])), 10))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4]), 10))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4])), 10))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'ln':
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1])))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1]))))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2])))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2]))))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3])))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3]))))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4])))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4]))))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'na':  # if you are not using "log" there is no reason to perform all this circus
                                                     # of negative numbers ect.
                    dOUT[line.split('\t')[0]][0].append(line.strip(',').split('\t')[1])
                    dOUT[line.split('\t')[0]][1].append(line.strip(',').split('\t')[2])
                    dOUT[line.split('\t')[0]][2].append(line.strip(',').split('\t')[3])
                    dOUT[line.split('\t')[0]][3].append(line.strip(',').strip('\n').split('\t')[4])

            else:   # For Taxa / functions that were not detected at all in conditions C and W. Consider log type!
                dOUT[line.split('\t')[0]] = []
                for timeP in line.strip('\n').split('\t')[1:]:
                    if args.log_type == 'log2':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, 0, log(int(timeP), 2)])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, 0, -log(abs(int(timeP)), 2)])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0, 0])

                    elif args.log_type == 'log10':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, 0, log(int(timeP), 10)])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, 0, -log(abs(int(timeP)), 10)])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0, 0])

                    elif args.log_type == 'ln':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, 0, log(int(timeP))])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, 0, -log(abs(int(timeP)))])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0, 0])

                    elif args.log_type == 'na':
                        dOUT[line.split('\t')[0]].append([0, 0, int(timeP)])

    for line in dOUT:  # for entries that are present in dOUT but not in OA.
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
        else: # for OK input files
            if line.split('\t')[0] in dOUT:   # for entries that are found in both dOUT and GH
                if args.log_type == 'log2':
                    # following 3 statements only regard the first timepoint in the line...
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1]), 2))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1])), 2))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2]), 2))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2])), 2))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3]), 2))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3])), 2))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4]), 2))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4])), 2))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'log10':
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1]), 10))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1])), 10))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2]), 10))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2])), 10))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3]), 10))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3])), 10))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4]), 10))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4])), 10))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'ln':
                    if int(line.strip(',').split('\t')[1]) > 0:
                        dOUT[line.split('\t')[0]][0].append(log(int(line.strip(',').split('\t')[1])))
                    elif int(line.strip(',').split('\t')[1]) < 0:
                        dOUT[line.split('\t')[0]][0].append(-log(abs(int(line.strip(',').split('\t')[1]))))
                    else:
                        dOUT[line.split('\t')[0]][0].append(0)

                    if int(line.strip(',').split('\t')[2]) > 0:
                        dOUT[line.split('\t')[0]][1].append(log(int(line.strip(',').split('\t')[2])))
                    elif int(line.strip(',').split('\t')[2]) < 0:
                        dOUT[line.split('\t')[0]][1].append(-log(abs(int(line.strip(',').split('\t')[2]))))
                    else:
                        dOUT[line.split('\t')[0]][1].append(0)

                    if int(line.strip(',').split('\t')[3]) > 0:
                        dOUT[line.split('\t')[0]][2].append(log(int(line.strip(',').split('\t')[3])))
                    elif int(line.strip(',').split('\t')[3]) < 0:
                        dOUT[line.split('\t')[0]][2].append(-log(abs(int(line.strip(',').split('\t')[3]))))
                    else:
                        dOUT[line.split('\t')[0]][2].append(0)

                    if int(line.strip(',').split('\t')[4]) > 0:
                        dOUT[line.split('\t')[0]][3].append(log(int(line.strip(',').split('\t')[4])))
                    elif int(line.strip(',').split('\t')[4]) < 0:
                        dOUT[line.split('\t')[0]][3].append(-log(abs(int(line.strip(',').strip('\n').split('\t')[4]))))
                    else:
                        dOUT[line.split('\t')[0]][3].append(0)

                elif args.log_type == 'na':  # if you are not using "log" there is no reason to perform all this circus
                                                     # of negative numbers ect.
                    dOUT[line.split('\t')[0]][0].append(line.strip(',').split('\t')[1])
                    dOUT[line.split('\t')[0]][1].append(line.strip(',').split('\t')[2])
                    dOUT[line.split('\t')[0]][2].append(line.strip(',').split('\t')[3])
                    dOUT[line.split('\t')[0]][3].append(line.strip(',').strip('\n').split('\t')[4])

            else:   # For Taxa / functions that were not detected at all in conditions C  W and OA
                dOUT[line.split('\t')[0]] = []
                for timeP in line.strip('\n').split('\t')[1:]:
                    if args.log_type == 'log2':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, 0, log(int(timeP), 2)])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, 0, -log(abs(int(timeP)), 2)])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0, 0])

                    elif args.log_type == 'log10':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, 0, log(int(timeP), 10)])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, 0, -log(abs(int(timeP)), 10)])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0, 0])

                    elif args.log_type == 'ln':
                        if int(timeP) > 0:
                            dOUT[line.split('\t')[0]].append([0, 0, log(int(timeP))])
                        elif int(timeP) < 0:
                            dOUT[line.split('\t')[0]].append([0, 0, -log(abs(int(timeP)))])
                        else:
                            dOUT[line.split('\t')[0]].append([0, 0, 0])

                    elif args.log_type == 'na':
                        dOUT[line.split('\t')[0]].append([0, 0, int(timeP)])

    for line in dOUT:
        if len(dOUT[line][0]) == 3:
            dOUT[line][0].append(0)
            dOUT[line][1].append(0)
            dOUT[line][2].append(0)
            dOUT[line][3].append(0)

print "\n Writing " + args.output_file +"..."

with open(args.output_file, 'w') as outTab:
    outTab.write("#title:\t" + str(args.Title) + "\n")
    outTab.write("#col_names:\tdT1\tdT3\tdT6\tdT10\n")
    outTab.write("#sub_col:\tControl\tWarming\tOcean acidification\tGreen house\n")
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
__author__ = 'Dan'

#import argparse
import sys
import os


'''
This script will run over a KOs table returned from KAAS containing the nr_IDs and the KOs. each KO appearing more than
once will be assigned to one of the nr_IDs (they all point to the smae kind of enzyme anyway) and the weights of all IDs
will be added.

USAGE: python Cluster_KOs.py [KO list from KAAS with weights]

'''

if len(sys.argv) != 2:
    sys.exit('USAGE: python Cluster_KOs.py [KO list from KAAS with weights]')

if __name__ == "__main__":
    KO_dict = dict()

    print "\n opening " + sys.argv[1] + "..."

    with open (sys.argv[1], "r") as KO_tab:
        for line in KO_tab:
            if len(line.strip('\n').split("\t")) < 2:
                continue
            elif line.strip('\n').split("\t")[1] in KO_dict:
                weight = int(line.strip('\n').split("\t")[0].split('|')[1])
                KO_dict[line.strip('\n').split("\t")[1]][1] = int(KO_dict[line.strip('\n').split("\t")[1]][1]) + weight
            else:
                KO_dict[line.strip('\n').split("\t")[1]] = [line.strip('\n').split("\t")[0].split("|")[0],
                                                            line.strip('\n').split("\t")[0].split("|")[1]]




    #print KO_dict
############################################## write Output ############################################################

    basename = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]


    print "\n writing " + basename + "_KOs_clustered.tab"


    # this index will count all raw reads that were summed up in the output file
    i = 0
    with open(basename + "_KOs_clustered.tab" , 'w') as outFile1:
        outFile1.write('representative ID')
        outFile1.write('\t')
        outFile1.write('KO')
        outFile1.write('\n')
        for KO in KO_dict:
            i = i + int(KO_dict[KO][1])
            outFile1.write(KO_dict[KO][0])
            outFile1.write("|")
            outFile1.write(str(KO_dict[KO][1]))
            outFile1.write('\t')
            outFile1.write(KO)
            outFile1.write('\n')
        outFile1.write("A total number of " + str(i) + " reads are summed up in this list of KOs")
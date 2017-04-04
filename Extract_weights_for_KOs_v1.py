__author__ = 'Dan'

#import argparse
import sys
import os


'''
This script will run over a table with the following structure: nr_prot_Identifyer_weight|xxx \t KO and over a pathways
list returned from KAAS which looks like that:

ko01100 PATHWAY (nr_of_KOs_found)
ko:KOXXXX gene_name enzyme_name/Product [E_nr_level_4]
ko:K00003 E1.1.1.3; homoserine dehydrogenase [EC:1.1.1.3]
ko:K00005 gldA; glycerol dehydrogenase [EC:1.1.1.6]

The output will contain all pathways information plus nr_prot_ID and weights

USAGE: python Extract_wiehts_for_KOs.py [KO list from KAAS with weights] [pathways_list_including_all details]

'''

if len(sys.argv) != 3:
    sys.exit('USAGE: python Extract_wiehts_for_KOs.py [KO list from KAAS with weights] [pathways_list_including_all '
             'details]')

if __name__ == "__main__":
    KO_dict = dict()
    #no_KOs = dict()
    pathways = dict()
    pathways_KOs = dict()

    print "\n opening " + sys.argv[1] + "..."

    with open(sys.argv[1], "r") as KO_tab:
        for line in KO_tab:
            #print line.strip('\n').split("\t")

            if len(line.strip('\n').split("\t")) == 2:
                if len(line.strip('\n').split("\t")[0].split("|")) == 2:
                    KO_dict[line.strip('\n').split("\t")[1]] = [line.strip('\n').split("\t")[0],
                                                                line.strip('\n').split("\t")[0].split("|")[1]]

    print "\n opening " + sys.argv[2] + "..."
    with open(sys.argv[2], 'r') as pathways_list:
        for line in pathways_list:
            if line[7] == ' ':
                line = line[:7] + '\t' + line[8:]
                i = 0
                for char in line:
                    i += 1
                    if char == "(":
                        line = line[:i-1] + '\t' + line[i:]
                pathways[line.split('\t')[0]] = line.strip('\n').strip(')').split('\t')[1:]

            elif line[9] == ' ':
                line = line[:9] + '\t' + line[10:]
                for char in line:
                    #i += 1
                    if char == ";":
                        line = line[:int(line.index(char))] + '\t' + line[int(line.index(char)+1):-1]
                # In all lines the EC number appears inside []. however using the '[' for splitting is problematic since
                # some lines have it in other contexts. therefore i used '[' and next position is E. this shouldn't be
                # happening in other situations (I hope...).
                    elif char == "[" and not line[line.index(char)+1] == "E":
                        line = line[:int(line.index(char))] + '(' + line[int(line.index(char)+1):-1]
                    elif char == "[" and line[line.index(char)+1] == "E":
                        line = line[:int(line.index(char))] + '\t' + line[int(line.index(char)+1):-1]
                # the 'replace(']', ')')' in the next line of code is for the square brackets inside the product
                # description. all other ']' chars in the strings are the last char in the line (which is excluded from
                # the line in the for loop:  line = line[some int()] + '(' + line[some int() :-1].
                pathways_KOs[line.split('\t')[0].split(":")[1]] = line.replace(']', ')').split('\t')[1:]

    for KO in pathways_KOs:
        if KO in KO_dict:
            pathways_KOs[KO].append(KO_dict[KO][0])
        else:
            print "\n warning! KO " + KO +" not found in the KO list! This should not happen so please check the " \
                                          "source of input files!!!"
    #print pathways_KOs

############################################## write Output ############################################################

    basename = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]


    print "\n writing " + basename + "_with_nr_IDs_and_weights.tab"

    with open(basename + "_with_nr_IDs_and_weights.tab", 'w') as outFile1:
        outFile1.write('KO number')
        outFile1.write('\t')
        outFile1.write('gene name')
        outFile1.write('\t')
        outFile1.write('product')
        outFile1.write('\t')
        outFile1.write('EC number')
        outFile1.write('\t')
        outFile1.write('nr_ID')
        outFile1.write('\t')
        outFile1.write('weight')
        outFile1.write('\n')
        for KO in pathways_KOs:
            #print KO
            #print pathways_KOs[KO]
            if len(pathways_KOs[KO]) == 4:
                outFile1.write(KO)
                outFile1.write('\t')
                for item in pathways_KOs[KO][:-1]:
                    outFile1.write(item.strip('\n'))
                    outFile1.write('\t')
                outFile1.write(pathways_KOs[KO][-1].split('|')[0].strip('_weights'))
                outFile1.write('\t')
                outFile1.write(pathways_KOs[KO][-1].split('|')[1])
                outFile1.write('\n')
            elif len(pathways_KOs[KO]) == 3:
                outFile1.write(KO)
                outFile1.write('\t')
                outFile1.write(pathways_KOs[KO][0])
                outFile1.write('\t')
                outFile1.write(pathways_KOs[KO][1].strip('\n'))
                outFile1.write('\t')
                outFile1.write('no E number')
                outFile1.write('\t')
                outFile1.write(pathways_KOs[KO][-1].split('|')[0].strip('_weights'))
                outFile1.write('\t')
                outFile1.write(pathways_KOs[KO][-1].split('|')[1])
                outFile1.write('\n')
            else:
               print '\n WARNING! the entry assigned to ' + KO + ' is not listed correctly. Check pathways list and ' \
                                                                 'correct format in all lines containing this KO!!!'
               print ###
               print '\n ' + KO
               print '\n ' + str(pathways_KOs[KO])
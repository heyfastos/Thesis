__author__ = 'tricho'

import sys
import os


'''
the last step of data reduction? this script will run over a table produced by "Extract_weights_for_KOs_v1.py" and over
a pathways file downloaded from KAAS including all KOs assigned to each pathway. It will return a list of all pathways as
listed in the pathways file, the KKEGG nr for each pathway, the nr of KOs assigned to it and a weighted number that will
reflect the true number of sequences assigned to each pathway. It will not return a list of KOs assigned to each pathway
because this can be obtained from the pathways file itself

USAGE:  python group_KOs_in_pthways.py [weighted_KOs_table] [pathways_with_KOs_list]
'''


if len(sys.argv) != 3:
    sys.exit('\n USAGE:  python group_KOs_in_pthways.py [weighted_KOs_table] [pathways_with_KOs_list]')

if __name__ == "__main__":
    KO_dict = dict()

    print "\n opening " + sys.argv[1] + "..."

    with open (sys.argv[1], "r") as KO_tab:
        for line in KO_tab:
            KO_dict[line.strip('\n').split("\t")[0]] = line.strip('\n').split("\t")[1:]
    for KO in KO_dict:
        if len(KO_dict[KO]) != 5:
            sys.exit('\n WFT is wrong with you bro?! your KO input table is FUCKED!!! here, i found this line:' + KO +
                     str(KO_dict[KO]) + ' you probably want to check why this has happened. Please, come back to me '
                                        'when you are older and wiser.')
    pathways = dict()

    print "\n opening " + sys.argv[2] + "..."
    with open (sys.argv[2], "r") as pathway_list:
        for line in pathway_list:
            # Lines listing pathway names and not individual KOs have ' ' in [7]
            if line[7] == ' ':
                line = line[:6] + '\t' + line[8:]
                current_pathway = line.replace('(','\t').strip('\n').strip(')').split('\t')[1]
                pathways[current_pathway] = [line.replace('(','\t').strip('\n').strip(')').split('\t')[0],
                                             line.replace('(','\t').strip('\n').strip(')').split('\t')[2]]
            # Lines listing KOs assigned to pathways have ' ' in [9]. as long as the next pathway name is not
            # encountered, the KOs are assigned to the pathway saved under "current pathway".
            elif line[9] == ' ':
                gene_name = line.replace(';', ' ').split(' ')[1]
                KO_nr = line.replace(':', ' ').split(' ')[1]
                if KO_nr in KO_dict:
                    weight = KO_dict[KO_nr][-1]
                else:
                    sys.exit('\n FATAL ERROR! ' + KO_nr + ' was not found in the pathways list!!! are you sure you '
                                                            'used this list to generate your table???')
                pathways[current_pathway].append([gene_name, KO_nr, weight])

    # the structure of {pathways} is the following: {'pathway_name':['pathway_kegg_ID', 'nr_of_KOs_assigned',
    # ['geneName_KO1', 'KO_nr_KO1', 'weight 1'],['geneName_KO2', 'KO_nr_KO2', 'weight_2'] ...
    # ['geneName_KOn','KO_nr_KOn', 'weight_n']...}.    Basically, each pathway's name points to a list of lists that
    # starts with two elements that are not lists- the ID number of tha pathway (KEGG ID) and the number of lists (KOs)
    # assigned to the pathway. each KO is represented by a list including only the gene name, KO nr, and weight

    basename = os.path.splitext(os.path.split(sys.argv[1])[-1])[0]

    print '\n writing ' + basename + '_pathways.txt...'

    with open(basename + '_pathways.txt...', 'w') as outFile:
        outFile.write('pathway')
        outFile.write('\t')
        outFile.write('#KOs_assigned')
        outFile.write('\t')
        outFile.write('pathway\'s_KEGG_nr')
        outFile.write('\t')
        outFile.write('#reads_assigned')
        outFile.write('\n')
        for pathway in pathways:
            outFile.write(pathway)
            outFile.write('\t')
            outFile.write(pathways[pathway][0])
            outFile.write('\t')
            outFile.write(pathways[pathway][1])
            outFile.write('\t')
            weight = 0
            for entry in pathways[pathway][2:]:
                weight += int(entry[2])
            outFile.write(str(weight))
            outFile.write('\n')


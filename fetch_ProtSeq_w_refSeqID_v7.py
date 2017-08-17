__author__ = 'Dan'
from Bio import Entrez, SeqIO
import argparse
import sys
import os

'''
Script will select only best hit (if exceeding threshold  - line 61) and fetch its protein sequence from NCBI. 
the difference to the previous versions is that this one will include weights for each protID in the output files, in
case the specific protein is the hit of more than one query in the fasta file used to produce the tab file handled here
Version 6 will take weights (in the headers) into account and will add them to the final weights in the output.
Version 7 will print the number of protein IDs that were not fetched from NCBI (I saw many of them, that I was able to 
call out when searching the NCBI website). It will also create a file of all uncalled protein IDs and their weights
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_table", help="table from beckers", type=str, required=True)
    parser.add_argument("-t", "--nt_nr", help="nucleotide nt, or protein nr", type=str, default="nr")
    parser.add_argument("-o", "--output", help="output file", type=str, default="./myOutput.fa")
    parser.add_argument("-e", "--email", help="email for ncbi", type=str, default="dan-robin.miller@biu.ac.il")
    args = parser.parse_args()



    # setup email for ncbi
    if args.email == "":
        print("Pleas specify a valid email address! ... -e my@mail.com")
        exit()
    else:
        Entrez.email = args.email

        
        # read input file
    genome_lookup = dict()
    Seqs_found = dict()
    uncalled_seqs = dict()
    print "\n opening " + args.in_table + "..."
    with open(args.in_table, "r") as f_in:
        for line in f_in:
            line = line.strip()
            seqID = line.split('\t')[0]
            uncalled_index = 0
            # following "if" will make sure no more than one hit from each seqID will be included in the output.
            if seqID in Seqs_found:
                continue
            else:
                if len(seqID.split("weight|")) == 2:
                    weight = int(seqID.split("weight|")[1])
                    #print weight
                else:
                    weight = 1
                seq = line.split('\t')
                # the following elif statement is meant for protein IDs like the following: 1EA0_A. They are annotated
                # with a "|" char instead of "_" from the pdb database (RCSB PDB) which creates a confusion in the
                # interpretation of the input strings: I was using "|" to separate the second column in the diamond
                # output containing the gi and the refseq IDs. In the case that the column creates 5 elements instead of
                # 4 after splitting it using "|" it probably means that the respective ID contain a "|" char.
                # The additional "|" should be replaced with a "_" char.
                if len(seq[1].split('|')) > 3 and seq[1].split('|')[2] == 'pdb':
                    seq[1] = seq[1][:-2] + "_" + seq[1][-1]
                    dbID = str(seq[1].split('|')[3])
                    if dbID in genome_lookup:
                        genome_lookup[dbID][1] += weight
                        Seqs_found[seqID] = True
                    # if protein ID is encountered for the first time - check quality and try to find protein sequence
                    # that will be added to the output with the weight "1". if quality check fails- go to next line in
                    # the input table.
                    elif float(seq[2]) < 60 or float(seq[3]) < 30 or float(seq[11]) < 60:
                        continue
                    else:
                        try:
                            if args.nt_nr == "nt":
                                handle = Entrez.efetch(db='nucleotide', id=dbID, rettype='fasta')
                            elif args.nt_nr == "nr":
                                 handle = Entrez.efetch(db='protein', id=dbID, rettype='fasta')
                            else:
                                sys.exit('the specified database is not accepted. please apply the -t flag using '
                                         'either nt or nr')
                            record = SeqIO.read(handle, 'fasta')
                            genome_lookup[dbID] = [record.seq, weight]
                            Seqs_found[seqID] = True
                        except:
                            print("\n " + seq[1] + " is not a valid RefSeqID. Check it in the NCBI web platform! Moving"
                                                   "to the next hit in the table")
                            uncalled_index += weight
                            uncalled_seqs[dbID] = weight
                # another type of weird IDs that were found have the following structure: "gi|226374|prf||1508255A".
                # These are handled in the following "elif" block
                elif len(seq[1].split('|')) > 3 and seq[1].split('|')[3] == '':
                    dbID = seq[1].split("|")[-1]
                    if dbID in genome_lookup:
                        genome_lookup[dbID][1] += weight
                        Seqs_found[seqID] = True
                    # if protein ID is encountered for the first time - check quality and try to find protein sequence
                    # that will be added to the output with the weight "1". if quality check fails- go to next line in
                    # the input table.
                    elif float(seq[2]) < 60 or float(seq[3]) < 30 or float(seq[11]) < 60:
                        continue
                    else:
                        try:
                            if args.nt_nr == "nt":
                                handle = Entrez.efetch(db='nucleotide', id=dbID, rettype='fasta')
                            elif args.nt_nr == "nr":
                                 handle = Entrez.efetch(db='protein', id=dbID, rettype='fasta')
                            else:
                                sys.exit('the specified database is not accepted. please apply the -t flag using '
                                         'either nt or nr')
                            record = SeqIO.read(handle, 'fasta')
                            genome_lookup[dbID] = [record.seq, weight]
                            Seqs_found[seqID] = True
                        except:
                            print("\n " + seq[1] + " is not a valid RefSeqID. Check it in the NCBI web platform! Moving"
                                                   "to the next hit in the table")
                            uncalled_index += weight
                            uncalled_seqs[dbID] = weight
                # If the refSeq ID handled is a "regular" ID that doesn't contain a "|" char, the fourth element of the
                # second column separated using "|" will be the database ID. the case is handled in the following block.
                else:
                    dbID = str(seq[1].split('|')[3])
                    # in case the protein ID was already found before-  just add one to its weight and move to next
                    # query in the table
                    if dbID in genome_lookup:
                        genome_lookup[dbID][1] += weight
                        Seqs_found[seqID] = True
                    elif float(seq[2]) < 60 or float(seq[3]) < 30 or float(seq[11]) < 60:
                        continue
                    else:
                        try:
                            if args.nt_nr == "nt":
                                handle = Entrez.efetch(db='nucleotide', id=dbID, rettype='fasta')
                            elif args.nt_nr == "nr":
                                handle = Entrez.efetch(db='protein', id=dbID, rettype='fasta')
                            else:
                                sys.exit('the specified database is not accepted. please apply the -t flag using '
                                         'either nt or nr')
                            record = SeqIO.read(handle, 'fasta')
                            genome_lookup[dbID] = [record.seq, weight]
                            Seqs_found[seqID] = True
                        except:
                            print("\n " + seq[1] + " is not a valid RefSeqID. Check it in the NCBI web platform! Moving "
                                                 "to the next hit in the table")
                            uncalled_index += weight
                            uncalled_seqs[dbID] = weight

    basename = os.path.splitext(args.in_table)[0]

    print "\n writing " + args.output +"..."

    with open(args.output, 'w') as outFile:

        for entry in genome_lookup:
            outFile.write(">")
            outFile.write(str(entry)+"_weights|" + str(genome_lookup[entry][1]))
            outFile.write("\n")
            outFile.write(str(genome_lookup[entry][0]))
            outFile.write("\n")

    print "\n writing " + basename + "_uncalled_seqs_list.txt"

    with open(basename + "uncalled_sequs_list.txt" , 'w') as uncalled:
        for ID in uncalled_seqs:
            uncalled.write(ID)
            uncalled.write("\t")
            uncalled.write(uncalled_seqs[ID])
            uncalled.write("\n")

    if args.nt_nr == "nt":
        print " \n the summed weight of all reads that matched a hit in your blast search, but their nucleotide " \
              "sequence could not be retrieved is: " + str(uncalled_index)
    elif args.nt_nr == "nr":
        print " \n the summed weight of all reads that matched a hit in your blast search, but their protein " \
              "sequence could not be retrieved is: " + str(uncalled_index)

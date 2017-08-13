__author__ = 'steffen'
import argparse
import os
import re
import shlex
import subprocess
from subprocess import Popen, PIPE
from Bio import SeqIO

# DESCRIPTION: Count number of sequences in a given fastq file
# INPUT: fastq-file
# OUTPUT: <int> number of sequences
def count_fastq(fastq_file):
    act_args = shlex.split("grep -c '@' " + str(fastq_file))
    p = subprocess.Popen(act_args, stdout=PIPE)
    (output, err) = p.communicate()
    p.wait()
    count = output.decode('utf-8').rstrip()
    return count

# DESCRIPTION: Count Spikes
# INPUT: file name + sam suffix
# OUTPUT: <string> counts for each spike name (tab separated)
def count_sam(in_file, sam_suffix):
    tmp_input = str(in_file) + str(sam_suffix)
    fh = open(tmp_input, "r")
    spike_hash = dict()
    spike_arr = list()
    for line in fh:
        line = line.rstrip()
        line_arr = line.split("\t")
        if line_arr[0] == "@SQ":
            tmp_id = line_arr[1].split(":")[1]
            spike_hash[tmp_id] = 0
            spike_arr.append(tmp_id)
        if str(line_arr[0])[0] != "@":
            if line_arr[2] in spike_hash:
                spike_hash[line_arr[2]] += 1
    fh.close()
    # create final output
    counts = ""
    for key in spike_arr:
        counts += "\t" + str(spike_hash[key])
    return counts

# DESCRIPTION: Execute Cutadapt to a given input file. Quality will checked and barcode will be removed
# INPUT: file path (fastq files), file with barcodes, path to Cutadapt
# OUTPUT: Creates new files directly in the given input folder
def remove_adapter_from_seq_quality_trimming(in_file_path, in_barcode_file, path_cutadapt,
                                             min_seq_qual=28, min_length=20, quality_base=33):
    # setup command
    cmd_cutadapt = str(path_cutadapt) + " -f fastq"
    # fwd-reads
    with open(in_barcode_file, "r") as barcode_fh:
        for tmp_barcode in barcode_fh:
            cmd_cutadapt += " -b " + str(tmp_barcode.strip())
    # rev-reads
    with open(in_barcode_file, "r") as barcode_fh:
        for tmp_barcode in barcode_fh:
            cmd_cutadapt += " -B " + str(tmp_barcode.strip())
    # additional parameters
    cmd_cutadapt += " -O 10 -e 0.2 -n 3 -q " + str(min_seq_qual) + "," + str(min_seq_qual)
    cmd_cutadapt += " --quality-base=" + str(quality_base)
    cmd_cutadapt += " --match-read-wildcards -m " + str(min_length) + " --trim-n -o"
    # iterate over all pairs R1/R2
    for group in in_file_path:
        tmp_cmd_cutadapt = cmd_cutadapt
        tmp_fwd = ""
        tmp_rev = ""
        for file in in_file_path[group]:
            if re.search("_R1_",file):
                tmp_fwd = str(file)
            else:
                tmp_rev = str(file)
        tmp_cmd_cutadapt += " " + str(tmp_fwd) + "-cutadapt.fastq" + " -p " + str(tmp_rev) + "-cutadapt.fastq"
        tmp_cmd_cutadapt += " " + str(tmp_fwd) + " " + str(tmp_rev)
        os.system(str(tmp_cmd_cutadapt))
    return 0

# DESCRIPTION: Before Cutadapt can be applied on paired end reads, the 2 sets must be merged together
# INPUT: path to sortmerna, path to fastq files, path to forward file, path to reverse file
# OUTPUT: returns path to merged file
def merge_fwd_rev_for_sortmerna(path_sortmerna, path_to_fastqs, fwd_fastq, rev_fastq):
    fwd_fastq_cmp = str(fwd_fastq) + "-cutadapt.fastq"
    rev_fastq_cmp = str(rev_fastq) + "-cutadapt.fastq"
    merged_reads_out = str(path_to_fastqs) + "merged.fastq"
    os.system("bash " + str(path_sortmerna) + "scripts/merge-paired-reads.sh " + str(fwd_fastq_cmp) + " "
                                                                               + str(rev_fastq_cmp) + " "
                                                                               + str(merged_reads_out))
    return merged_reads_out

# DESCRIPTION: After Cutadapt was applied the merged file must be splitted into the origin format (fwd, rev)
#              Temporary files will also deleted!
# INPUT: path to sortmerna, path to fastq files, path to forward file, path to reverse file, merged-nonrRNA, merged-rRNA
# OUTPUT: Splits the merged result (merged-nonrRNA, merged-rRNA) to merged-nonrRNA (fwd, rev), merged-rRNA (fwd, rev)
def demerge_fwd_rev_for_sortmerna(path_sortmerna, path_to_fastqs, fwd_fastq, rev_fastq, nonrRNA, rRNA):
    # unmerge rRNA
    fwd_fastq_cmp = str(fwd_fastq) + "-cutadapt.fastq-sortmerna-rRNA.fastq"
    rev_fastq_cmp = str(rev_fastq) + "-cutadapt.fastq-sortmerna-rRNA.fastq"
    merged_reads_in = str(path_to_fastqs) + str(rRNA)
    os.system("bash " + str(path_sortmerna) + "scripts/unmerge-paired-reads.sh " + str(merged_reads_in) + " "
                                                                                 + str(fwd_fastq_cmp) + " "
                                                                                 + str(rev_fastq_cmp))
    # unmerge non-rRNA
    fwd_fastq_cmp = str(fwd_fastq) + "-cutadapt.fastq-sortmerna-non-rRNA.fastq"
    rev_fastq_cmp = str(rev_fastq) + "-cutadapt.fastq-sortmerna-non-rRNA.fastq"
    merged_reads_in = str(path_to_fastqs) + str(nonrRNA)
    os.system("bash " + str(path_sortmerna) + "scripts/unmerge-paired-reads.sh " + str(merged_reads_in) + " "
                                                                                 + str(fwd_fastq_cmp) + " "
                                                                                 + str(rev_fastq_cmp))
    os.system("rm " + path_to_fastqs + "merged.fastq")
    os.system("rm " + path_to_fastqs + "non-rRNA.fastq")
    os.system("rm " + path_to_fastqs + "rRNA.fastq")

# DESCRIPTION: Executes sortmerna
# INPUT: file path to fastq files, path to sortmerna, path to fastq files, number of threads
# OUTPUT: well processed files, two files for each library -> rRNA-(fwd,rev), non-rRNA-(fwd,rev)
def call_sortmerna(in_file_path, path_sortmerna, raw_dir, num_threads):
    # setup sortmerna command
    sortmerna_cmd = str(path_sortmerna) + "sortmerna" + " --ref "
    # iterate overall rRNA DBs
    rRNAdb_path = str(path_sortmerna) + "rRNA_databases/"
    index_path = str(path_sortmerna) + "index/"
    files_in_dir = os.listdir(rRNAdb_path)
    for file_in_dir in files_in_dir:
        sortmerna_cmd += rRNAdb_path + str(file_in_dir) + ","
        cor_index_file = file_in_dir.split(".fasta")[0]
        sortmerna_cmd += index_path + str(cor_index_file) + ":"
    sortmerna_cmd = sortmerna_cmd[:-1]
    sortmerna_cmd += " --fastx --paired_in -v -a " + str(num_threads) + " --aligned " + str(raw_dir) + "rRNA " + "--other " + str(raw_dir) + "non-rRNA"

    # iterate through all pairs (FWD/REV)
    # create merge file as input for sortmerna
    for group in in_file_path:
        for file in in_file_path[group]:
            if re.search("_R1_",file):
                fwd_fastq = str(file)
            else:
                rev_fastq = str(file)
        merged_reads_file_path = merge_fwd_rev_for_sortmerna(path_sortmerna, raw_dir, fwd_fastq, rev_fastq)
        # call sortmerna
        mod_sortmerna_cmd = sortmerna_cmd
        mod_sortmerna_cmd += " --reads " + str(merged_reads_file_path)
        os.system(mod_sortmerna_cmd)
        # unmerge fastqs
        demerge_fwd_rev_for_sortmerna(path_sortmerna, raw_dir, fwd_fastq, rev_fastq, "non-rRNA.fastq", "rRNA.fastq")

# DESCRIPTION: Search for pairs (fwd,rev) in the given directory. Keyword is ..._R...
# INPUT: path to fastq libraries (fwd, rev)
# OUTPUT: file path hash
def setup_file_pair_hash(in_file_path):
    file_path_hash = dict()
    counter_per_file = dict()
    files_in_dir = os.listdir(in_file_path)
    for file_in_dir in files_in_dir:
        tmp_file_name = file_in_dir.split("_R")[0]
        if tmp_file_name in file_path_hash:
            tmp_path = in_file_path + file_in_dir
            file_path_hash[tmp_file_name].append(tmp_path)
        else:
            file_path_hash[tmp_file_name] = list()
            tmp_path = in_file_path + file_in_dir
            counter_per_file[tmp_path] = list()
            file_path_hash[tmp_file_name].append(tmp_path)
    return file_path_hash, counter_per_file

# DESCRIPTION: Converts a "fastq" file -> "fasta" file
# INPUT: file path hash, suffix name (e.g. "-cutadapt.fastq-sortmerna-non-rRNA.fastq")
# OUTPUT: files converted into fasta and stored in the fastq file path
def call_fastq_to_fasta(in_file_path, suffix_name, encoding=33):
    for group in in_file_path:
        for file in in_file_path[group]:
            os.system("fastq_to_fasta -Q " + str(encoding) + " -n -r -i " + str(file) + str(suffix_name) + " -o " + str(file) + str(suffix_name) + ".fasta")

# DESCRIPTION: Count the number of sequences or spikes of all produced files
# INPUT: original path to fastq files, fastq pair hash, spike file,
#        "raw,cutadapt,non-rRNA,rRNA,spikes", "-cutadapt.fastq-sortmerna-non-rRNA.fastq.fasta.sam"
# OUTPUT: statistics.txt
def count_everything(original_path, in_file_path, in_spikes_file, to_count, sam_suffix):
    tmp_arr = to_count.split(",")
    # copy into hash
    tmp_hash = dict()
    for i in tmp_arr:
        tmp_hash[i] = 0
    # loop over all files
    out_file = original_path + str("statistics.txt")
    fh = open(out_file, "w")
    if "spikes" in tmp_hash:
        fh.write("input-file" + "\t" + "raw-reads" + "\t" + "after-cutadapt" + "\t" + "non-rRNA" + "\t" + "rRNA")
        # search in spike file and extract spike names
        for record in SeqIO.parse(in_spikes_file, "fasta"):
            fh.write("\t" + str(record.id))
        fh.write("\n")
    else:
        fh.write("input-file" + "\t" + "raw-reads" + "\t" + "after-cutadapt" + "\t" + "non-rRNA" + "\t" + "rRNA" + "\n")
    out_line = ""
    for group in in_file_path:
        for file in in_file_path[group]:
            out_line = str(file)
            # count raw
            if "raw" in tmp_hash:
                count = count_fastq(str(file))
                out_line += "\t" + str(count)
            else:
                out_line += "\t" + "na"
            # count after-cutadapt
            if "cutadapt" in tmp_hash:
                count = count_fastq((str(file) + "-cutadapt.fastq"))
                out_line += "\t" + str(count)
            else:
                out_line += "\t" + "na"
            # count non-rRNA-reads
            if "non-rRNA" in tmp_hash:
                count = count_fastq((str(file) + "-cutadapt.fastq" + "-sortmerna-non-rRNA.fastq"))
                out_line += "\t" + str(count)
            else:
                out_line += "\t" + "na"
            # count rRNA-reads
            if "rRNA" in tmp_hash:
                count = count_fastq((str(file) + "-cutadapt.fastq" + "-sortmerna-rRNA.fastq"))
                out_line += "\t" + str(count)
            else:
                out_line += "\t" + "na"
            # count spikes (load spike file)
            if "spikes" in tmp_hash:
                count = count_sam(file, sam_suffix)
                out_line += str(count)
            # write to statistic file
            fh.write(out_line + "\n")
    fh.close()

# DESCRIPTION: Prepare Spike DB for Segemehl
# INPUT: path to segemehl, path to fastq files, file with spikes
# OUTPUT: returns DB file path
def setup_spike_DB(segemehl_location, original_path, spikes_file):
    file_path = str(original_path) + "segemehl-spikesDB/"
    os.system("mkdir " + str(file_path))
    db_file_path = file_path + "index.idx"
    os.system(str(segemehl_location) + " -x " + str(db_file_path) + " -d " + str(spikes_file))
    return db_file_path

# DESCRIPTION: Executes a DB search with Segemehl to find Spikes
# INPUT: path to segemehl, path to fastq files, file hash, path to segemehl DB,
#        path to spike file, number of threads, "-cutadapt.fastq-sortmerna-non-rRNA.fastq.fasta"
# OUTPUT: one sam file for each given input
def search_file_vs_spike_DB(segemehl_location, original_path, in_file_path, db_path, spikes_file, num_threads, suffix):
    for group in in_file_path:
        for file in in_file_path[group]:
            tmp_in_file = file + str(suffix)
            tmp_out_file = file + str(suffix) + ".sam"
            os.system(str(segemehl_location) + " -t " + str(num_threads) + " -i " + str(db_path) + " -d " + str(spikes_file) + " -q " +
                      str(tmp_in_file) + " > " + str(tmp_out_file))



# DESCRIPTION: fastqStatistics.py analyses a directory with paired fastq files and takes also barcodes, spikes and
#              rRNA/ non-rRNA intp account
# INPUT: Directory with paired end fastq-files
#
# OUTPUT: For each input File => input.cutadapt , input.cutadapt.sortmerna,
#                                input.cutadapt.sortmerna.fasta, input.cutadapt.sortmerna.fasta.spikes
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_dir", help="directory with fastq files (./path_to_fastqs/)", type=str, required=True)
    parser.add_argument("-s", "--spikes", help="spikes in fasta-format", type=str, default="empty")
    parser.add_argument("-b", "--barcodes", help="one barcode per line", type=str, required=True)
    parser.add_argument("-p", "--sortmerna", help="path to sortmerna", type=str, default="/data/steffenL/tools/sortmerna_v2/sortmerna-2.0-linux-64/")
    parser.add_argument("-c", "--cutadapt", help="path to cutadapt", type=str, default="~/.local/bin/cutadapt")
    parser.add_argument("-m", "--segemehl", help="path to segemehl", type=str, default="segemehl.x")
    parser.add_argument("-t", "--threads", help="number of threads", type=int, default=1)
    parser.add_argument("-q", "--min_quality", help="cutadapt : minimum allowed quality (PHRED-score)", type=int, default=20)
    parser.add_argument("-l", "--min_length", help="cutadapt : minimum allowed sequence length", type=int, default=20)
    parser.add_argument("-r", "--encoding", help="cutadapt : quality encoding 33/64", type=int, default=33)
    args = parser.parse_args()

    # check encoding parameter
    if args.encoding != 33 or args.encoding != 64:
        print(args.encoding + " encoding value is not supported")
        exit()

    # init variables
    file_path_hash = dict()
    counter_per_file = dict()
    # read all file names and create pair-paths (R1 & R2)
    (file_path_hash, counter_per_file) = setup_file_pair_hash(args.in_dir)

    # *** START WORKFLOW ***
    # remove adapter from sequences and quality trimming
    remove_adapter_from_seq_quality_trimming(file_path_hash, args.barcodes, args.cutadapt,
                                             args.min_quality, args.min_length, args.encoding)
    # SortmeRNA
    call_sortmerna(file_path_hash, args.sortmerna, args.in_dir, args.threads)
    # fastq to fasta (only ...raw.fastq-cutadapt.fastq-sortmerna-non-rRNA.fastq)
    call_fastq_to_fasta(file_path_hash, "-cutadapt.fastq-sortmerna-non-rRNA.fastq", args.encoding)
    # setup spike database
    if args.spikes != "empty":
        db_name = setup_spike_DB(args.segemehl, args.in_dir, args.spikes)
        # search reads against spikeDB and count hits per spike (only FWD reads [1])
        search_file_vs_spike_DB(args.segemehl, args.in_dir, file_path_hash, db_name, args.spikes, args.threads, "-cutadapt.fastq-sortmerna-non-rRNA.fastq.fasta")
        # count everything in the path
        # "raw-reads (fastq)"  "after-cutadapt (fastq)"  "non-rRNA-reads (fastq)"  "rRNA-reads (fastq)"  "spikes_in_non-rRNA (sam)"
        count_everything(args.in_dir, file_path_hash, args.spikes, "raw,cutadapt,non-rRNA,rRNA,spikes", "-cutadapt.fastq-sortmerna-non-rRNA.fastq.fasta.sam")
    else:
        # count everything in the path
        # "raw-reads (fastq)"  "after-cutadapt (fastq)"  "non-rRNA-reads (fastq)"  "rRNA-reads (fastq)"  "spikes_in_non-rRNA (sam)"
        count_everything(args.in_dir, file_path_hash, args.spikes, "raw,cutadapt,non-rRNA,rRNA", "")

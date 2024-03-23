#!/usr/bin/env python

"""
run-kallisto-on-SK36.py Rohan Maddamsetti.

This script estimates RNA copy number for all genes + Obelisk.S.s in SK36.

kallisto must be in the $PATH.

"""

import subprocess
from Bio import SeqIO
import os
from os.path import basename, exists
import numpy as np


################################################################################
## Functions.

def generate_SK36_fasta_reference_for_kallisto(gbk_path, obelisk_fasta_path, outfile):
    ## make a FASTA file with all the genomic genes as well as the Obelisk sequence.
    print("making as output: ", outfile)
    print("reading in as genome input:", gbk_path)
    print("reading in as Obelisk fasta input:", obelisk_fasta_path)
    with open(outfile, "w") as outfh:
        ## First, write out all the genes found in the genome.
        with open(gbk_path, 'rt') as gbk_fh:
            SeqID = None
            SeqType = None
            for i, record in enumerate(SeqIO.parse(gbk_fh, "genbank")):
                SeqID = record.id
                if "complete" in record.description:
                    if "plasmid" in record.description:
                        SeqType = "plasmid"
                    elif "chromosome" in record.description or i == 0:
                        ## IMPORTANT: we assume here that the first record is a chromosome.
                        SeqType = "chromosome"
                    else:
                        continue
                else:
                    continue
                for feature in record.features:
                    ## only analyze protein-coding genes.
                    if feature.type != "CDS": continue
                    locus_tag = feature.qualifiers["locus_tag"][0]
                    ## Important: for kallisto, we need to replace spaces with underscores in the product annotation field.
                    product = feature.qualifiers["product"][0].replace(" ","_")
                    DNAseq = feature.extract(record.seq)
                    header = ">" + "|".join(["SeqID="+SeqID,"SeqType="+SeqType,"locus_tag="+locus_tag,"product="+product])
                    outfh.write(header + "\n")
                    outfh.write(str(DNAseq) + "\n")
        ## Now write out the Obelisk_00003 sequence.
        with open(obelisk_fasta_path, 'rt') as obelisk_fasta_fh:
            for line in obelisk_fasta_fh:
                ## this line already has new line characters-- just write out verbatim.
                outfh.write(line)
    return


def generate_SK36_kallisto_index(ref_fasta_path, index_path):
    kallisto_index_args = ["kallisto", "index", "-i", index_path, ref_fasta_path]
    subprocess.run(kallisto_index_args)
    return


def run_kallisto_single_reads_quant(index_path, read_path, output_dir_path):
    ## fragment length mean and sd must be supplied for single-end reads using -l and -s.
    ## just make a guess for now: -l 300 -s 100
    ## note that the fragment length is DIFFERENT from read length:
    
    ## run with 10 threads by default.
    kallisto_quant_args = ["kallisto", "quant", "--single","--fragment-length=300", "--sd=100", "-t", "10", "-i", index_path, "-o", output_dir_path, "-b", "100", read_path]
    print(" ".join(kallisto_quant_args))
    subprocess.run(kallisto_quant_args)
    return


def run_kallisto_paired_reads_quant(index_path, read1_path, read2_path, output_dir_path):    
    ## run with 10 threads by default.
    kallisto_quant_args = ["kallisto", "quant", "-t", "10", "-i", index_path, "-o", output_dir_path, "-b", "100", read1_path, read2_path]
    print(" ".join(kallisto_quant_args))
    subprocess.run(kallisto_quant_args)
    return


def parse_metadata_in_header(target_id):
    fields = target_id.split("|")
    SeqID = fields[0].split("=")[-1]
    SeqType = fields[1].split("=")[-1]
    locus_tag = fields[2].split("=")[-1]
    ## convert underscores back into spaces.
    product = fields[3].split("=")[-1].replace("_", " ")
    metadata_tuple = (SeqID, SeqType, locus_tag, product)
    return(metadata_tuple)

def make_CSV_quant_file(quant_dir, csv_outfile):
    quant_file_path = os.path.join(quant_dir, "abundance.tsv")
    with open(csv_outfile, "w") as csv_fh:
        header = "SeqID,SeqType,locus_tag,product,length,eff_length,est_count,tpm"
        csv_fh.write(header + "\n")
        with open(quant_file_path, "rt") as quant_tsv_fh:
            for i, line in enumerate(quant_tsv_fh):
                if i == 0: continue ## don't parse the header.
                line = line.strip()
                target_id, length, eff_length, est_counts, tpm = line.split("\t")
                SeqID, SeqType, locus_tag, product = parse_metadata_in_header(target_id)
                row = [SeqID, SeqType, locus_tag, product, length, eff_length, est_counts, tpm]
                ## product fields contain commas! to get the parsing right, double-quote all fields.
                quoted_row = ["\"" + x +"\"" for x in row]
                csv_line = ",".join(quoted_row)
                csv_fh.write(csv_line + "\n")
    return


def merge_kallisto_quant_CSVs(results_dir, merged_csv_outfile):
    kallisto_abundance_csvs = [x for x in os.listdir(results_dir) if "SK36_kallisto_abundance" in x and x.endswith(".csv")]
    csv_paths = [os.path.join(results_dir, x) for x in kallisto_abundance_csvs]

    with open(merged_csv_outfile, "w") as merged_csv_fh:
        header = "RunID,SeqID,SeqType,locus_tag,product,length,eff_length,est_count,tpm"
        merged_csv_fh.write(header + "\n")
        for csvpath in csv_paths:
            ## get the Run ID for this file, and don't forget to double-quote for consistency.
            if "original" in csvpath:
                Run_ID = "\"SRR1713039\""
            else:
                unquoted_Run_ID = os.path.basename(csvpath).split(".")[0].split("_")[-1]
                Run_ID = "\"" + unquoted_Run_ID + "\""
            with open(csvpath, "rt") as csv_fh:
                for i, line in enumerate(csv_fh):
                    if i == 0: continue ## don't parse the header.
                    updated_line = Run_ID + "," + line
                    merged_csv_fh.write(updated_line)
    return


################################################################################

def main():

    kallisto_fasta_reference = "../results/SK36-kallisto-reference.fna"
    if exists(kallisto_fasta_reference):
        print(f"{kallisto_fasta_reference} exists on disk-- skipping step.")
    else:
        generate_SK36_fasta_reference_for_kallisto("../data/SK36-genome.gbk", "../data/Obelisk_000003.fna", kallisto_fasta_reference)

    
    kallisto_index = "../results/SK36-kallisto-index.idx"
    if exists(kallisto_index):
        print(f"{kallisto_index} exists on disk-- skipping step.")
    else:
        generate_SK36_kallisto_index(kallisto_fasta_reference, kallisto_index)

    ## run kallisto in single-read mode on the original RNAseq data used in the Obelisk paper.
    original_SK36_RNAseq_reads = "../data/SRR1713039.fastq"
    original_kallisto_quant_results_dir = "../results/SK36_kallisto_quant_SRR1713039/"
    if not exists(original_kallisto_quant_results_dir):
        os.makedirs(original_kallisto_quant_results_dir)
        run_kallisto_single_reads_quant(kallisto_index, original_SK36_RNAseq_reads, original_kallisto_quant_results_dir)
        original_kallisto_quant_CSV_path = "../results/original_SK36_kallisto_abundance.csv"
        make_CSV_quant_file(original_kallisto_quant_results_dir, original_kallisto_quant_CSV_path)

    ## run kallisto in paired-read mode on newer SK36 RNAseq datasets.
    newer_SK36_RNAseq_run_ids = ["SRR20627698", "SRR20627697", "SRR20627696",
                                 "SRR24302371", "SRR24302370", "SRR24302369",
                                 "SRR23591557", "SRR23591555", "SRR23591553",
                                 "SRR23591551", "SRR23591549", "SRR23591547",
                                 "SRR23591545", "SRR23591543", "SRR23591541", "SRR23591539"]
    
    for RunID in newer_SK36_RNAseq_run_ids:
        my_kallisto_quant_results_dir = "../results/SK36_kallisto_quant_" + RunID + "/"
        my_SK36_RNAseq_reads1 = "../data/" + RunID + "_1.fastq"
        my_SK36_RNAseq_reads2 = "../data/" + RunID + "_2.fastq"
        
        if not exists(my_kallisto_quant_results_dir):
            os.makedirs(my_kallisto_quant_results_dir)
            run_kallisto_paired_reads_quant(kallisto_index, my_SK36_RNAseq_reads1, my_SK36_RNAseq_reads2, my_kallisto_quant_results_dir)
            my_kallisto_quant_CSV_path = "../results/SK36_kallisto_abundance_" + RunID + ".csv"
            make_CSV_quant_file(my_kallisto_quant_results_dir, my_kallisto_quant_CSV_path)

    ## now combine these CSV files into one big CSV file for analysis in R.
    merge_kallisto_quant_CSVs("../results/", "../results/SK36_combined_kallisto_abundance.csv")
    return

main()



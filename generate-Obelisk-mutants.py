#!/usr/bin/env python

"""
generate-Obelisk-mutants.py by Rohan Maddamsetti.

This script generates 1137 input files for RNAfold, one for each position in Obelisk.S.s.
Each file contains 3 FASTA sequences, one for each possible single mutant.

This script also generates 4 additional input files for RNAfold:

1) WT + mutation A
2) WT + mutation B
3) WT + mutation C
4) WT + mutations B+C

where mutations A, B, C are:

A) Position 546 R162R (CGA -> CGG) A->G mutation in Oblin-1
B) Position 194 I48I (ATC -> ATA) C->A mutation in Oblin-1
C) Position 1014 A->G mutation downstream of Oblin-1

Polymorphisms B & C have similar frequencies in all samples that have them--
they may be linked in a single haplotype.

Usage: python generate-Obelisk-mutants.py

"""

import os
from Bio import SeqIO


def generate_single_mutant_tuples(sequence, pos, seqname_prefix, new_base=None):
    """
    Inputs:
    sequence: a Biopython Seq Object representing the Obelisk to mutate.
    pos: 1-based index of the position to mutate
    seqname_prefix: name of the sequence being mutated, like 'ObeliskWT'.

    Output:
    header_seq_mutant_tuples: a list of (FASTA header, Seq object) tuples.
    """
    header_seq_mutant_tuples = []
    bases = ['A', 'C', 'G', 'T']
    ## quick hack to make a specific point mutation
    ## using the optional new_base parameter.
    if new_base is not None:
        assert new_base in bases
        bases = [new_base]
        
    ## Iterate over each possible base at the given position.
    i = pos - 1 ## convert to zero-based indexing for python.
    for base in bases:
        ## Skip if the base is the same as the original base
        if base == sequence[i]:
            continue
        ## Create mutant sequence by replacing the base
        mutant = sequence[:i] + base + sequence[i+1:]
        ## make a FASTA header
        header = ">" + seqname_prefix + "_MutantPosition-" + str(pos) + "_AncestralBase-" + sequence[i] + "_MutantBase-" + base
        header_seq_tuple = (header, mutant)
        header_seq_mutant_tuples.append(header_seq_tuple)
    return header_seq_mutant_tuples


def write_single_mutants_to_file(single_mutant_tuples, outfile):
    with open(outfile, 'w') as fh:
        for tup in single_mutant_tuples:
            header, seq = tup
            print(header, file=fh)
            print(seq, file=fh)
            print("", file=fh)
    return


def main():

    ## make the directory containing the single mutant input files for RNAfold.
    single_mutant_input_file_dir = "../results/Obelisk_single_mutant_RNAfold_input/"
    if not os.path.exists(single_mutant_input_file_dir):
        os.mkdir(single_mutant_input_file_dir)

    ## get the wildtype Obelisk (DNA) sequence.
    WTobelisk = SeqIO.read("../data/Obelisk_000003.fna", "fasta")
    WTseq = WTobelisk.seq

    ## generate all possible single mutant input files from the WT obelisk.
    WTprefix = "ObeliskWT"
    for my_pos in range(1,len(WTseq)+1):
        WT_single_mutant_tuples = generate_single_mutant_tuples(WTseq, my_pos, WTprefix)
        ## write the mutant tuples to disk for RNAfold.
        outfname = WTprefix + "_MutantPosition" + str(my_pos) + ".fna"
        outfile = os.path.join(single_mutant_input_file_dir, outfname)
        write_single_mutants_to_file(WT_single_mutant_tuples, outfile)

    ## make the 546 A->G mutant and write to disk.
    mutantAprefix = "ObeliskMutantA"
    mutantA_tuples = generate_single_mutant_tuples(WTseq, 546, mutantAprefix, new_base='G')
    mutantA_outfname = mutantAprefix + "_MutantPosition546_AtoG.fna"
    mutantA_outfile = os.path.join("../results/", mutantA_outfname)
    write_single_mutants_to_file(mutantA_tuples, mutantA_outfile)

    ## make the 194 C->A mutant and write to disk.
    mutantBprefix = "ObeliskMutantB"
    mutantB_tuples = generate_single_mutant_tuples(WTseq, 194, mutantBprefix, new_base='A')
    mutantB_outfname = mutantBprefix + "_MutantPosition194_CtoA.fna"
    mutantB_outfile = os.path.join("../results/", mutantB_outfname)
    write_single_mutants_to_file(mutantB_tuples, mutantB_outfile)
    
    ## make the 1014 A->G mutant and write to disk.
    mutantCprefix = "ObeliskMutantC"
    mutantC_tuples = generate_single_mutant_tuples(WTseq, 1014, mutantCprefix, new_base='G')
    mutantC_outfname = mutantCprefix + "_MutantPosition1014_AtoG.fna"
    mutantC_outfile = os.path.join("../results/", mutantC_outfname)
    write_single_mutants_to_file(mutantC_tuples, mutantC_outfile)

    ## make the 194 C->A + 1014 A->G double mutant and write to disk.
    mutantBCprefix = "ObeliskMutantBC"
    ## get the mutant B sequence,
    mutantBseq = mutantB_tuples[0][1] ## mutantB_tuples is a list of tuples containing one tuple.
    ## and add mutant C on top.
    mutantBC_tuples = generate_single_mutant_tuples(mutantBseq, 1014, mutantBCprefix, new_base='G')
    mutantBC_outfname = mutantBCprefix + ".fna"
    mutantBC_outfile = os.path.join("../results/", mutantBC_outfname)
    write_single_mutants_to_file(mutantBC_tuples, mutantBC_outfile)
    return


main()


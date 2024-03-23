#!/usr/bin/env python

"""
tabulate-Obelisk-single-mutant-free-energies.py by Rohan Maddamsetti.

This script tabulates the RNAfold single-mutant output in
../results/Obelisk_single_mutant_RNAfold_output/

in a CSV file for easy analysis with a downstream R script called
analyze-Obelisk-single-mutant-free-energies.R.

Usage: python tabulate-Obelisk-single-mutant-free-energies.py > ../results/Obelisk-single-mutant-ensemble-free-energies.csv

"""

import os


def parse_header(mut_header):
    mut_fields = mut_header.split("_")
    mut_pos = mut_fields[1].split("-")[-1]
    mut_ancestral_base = mut_fields[2].split("-")[-1]
    mut_evolved_base = mut_fields[3].split("-")[-1]
    return (mut_pos, mut_ancestral_base, mut_evolved_base)


def main():

    ## print the header for the CSV file
    CSV_header = "Position,AncestralBase,MutantBase,EnsembleFreeEnergy"
    print(CSV_header)

    ## iterate through the RNAfold 
    RNAfold_single_mutant_results_dir = "../results/Obelisk_single_mutant_RNAfold_output/"
    RNAfold_mutant_files = [os.path.join(RNAfold_single_mutant_results_dir, x) for x in os.listdir(RNAfold_single_mutant_results_dir) if x.endswith(".fold")]

    for my_RNAfold_mutant_file in RNAfold_mutant_files:
        with open(my_RNAfold_mutant_file, "r") as RNAfold_fh:
            ## let's exploit the simple structure of these files to get the data we want.
            ## each file has 3 mutants, taking up 6 lines each, for a total of 18 lines in the file.
            my_mutant_data = [x.strip() for x in RNAfold_fh.readlines()] ## remove newline characters.

            mut1_header = my_mutant_data[0]
            mut1_ensemble_free_energy = my_mutant_data[3].split(" ")[-1].strip("[]")
            mut1_pos, mut1_ancestral_base, mut1_mutant_base = parse_header(mut1_header)
            print(",".join([mut1_pos, mut1_ancestral_base, mut1_mutant_base, mut1_ensemble_free_energy]))
            
            mut2_header = my_mutant_data[6]
            mut2_ensemble_free_energy = my_mutant_data[9].split(" ")[-1].strip("[]")
            mut2_pos, mut2_ancestral_base, mut2_mutant_base = parse_header(mut2_header)
            print(",".join([mut2_pos, mut2_ancestral_base, mut2_mutant_base, mut2_ensemble_free_energy]))

            mut3_header = my_mutant_data[12]
            mut3_ensemble_free_energy = my_mutant_data[15].split(" ")[-1].strip("[]")
            mut3_pos, mut3_ancestral_base, mut3_mutant_base = parse_header(mut3_header)
            print(",".join([mut3_pos, mut3_ancestral_base, mut3_mutant_base, mut3_ensemble_free_energy]))

main()

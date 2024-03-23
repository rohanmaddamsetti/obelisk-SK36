#!/bin/bash
#SBATCH --mem=100M ## 100MB of RAM
#SBATCH --array=1-1137

## submit-Obelisk-single-mutant-RNAfold-jobarray.sh by Rohan Maddamsetti.
## Usage: sbatch submit-Obelisk-single-mutant-RNAfold-jobarray.sh

input_file="../results/Obelisk_single_mutant_RNAfold_input/ObeliskWT_MutantPosition${SLURM_ARRAY_TASK_ID}.fna"
output_file="../results/Obelisk_single_mutant_RNAfold_output/ObeliskWT_MutantPosition${SLURM_ARRAY_TASK_ID}.fold"

echo "Running command: RNAfold -p -d2 --noLP --circ --noPS --noDP $input_file > $output_file"
##  use the parameters used in Obelisk 2024 preprint, and don't create postscript files.
## (note that the '-r' option in the preprint is probably an error).
RNAfold -p -d2 --noLP --circ --noPS --noDP "$input_file" > "$output_file"

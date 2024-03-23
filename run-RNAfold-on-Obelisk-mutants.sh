#!/bin/bash

## run-RNAfold-on-Obelisk-mutants.sh by Rohan Maddamsetti.
## Usage: run-RNAfold-on-Obelisk-mutants.sh

##  use the parameters used in Obelisk 2024 preprint, and don't create postscript files.
## (note that the '-r' option in the preprint is probably an error).

## move to the results folder so that output goes there.
cd ../results
RNAfold -p -d2 --noLP --circ --id-prefix=ObeliskWT ../data/Obelisk_000003.fna > Obelisk_WT.fold
## now move back.
cd ../src

## don't create postscript files for the mutants.
RNAfold -p -d2 --noLP --circ --noPS --noDP ../results/ObeliskMutantA_MutantPosition546_AtoG.fna > ../results/ObeliskMutantA_MutantPosition546_AtoG.fold

RNAfold -p -d2 --noLP --circ --noPS --noDP ../results/ObeliskMutantB_MutantPosition194_CtoA.fna > ../results/ObeliskMutantB_MutantPosition194_CtoA.fold

RNAfold -p -d2 --noLP --circ --noPS --noDP ../results/ObeliskMutantC_MutantPosition1014_AtoG.fna > ../results/ObeliskMutantC_MutantPosition1014_AtoG.fold

RNAfold -p -d2 --noLP --circ --noPS --noDP ../results/ObeliskMutantBC.fna > ../results/ObeliskMutantBC.fold


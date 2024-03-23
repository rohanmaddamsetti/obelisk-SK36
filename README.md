README.md by Rohan Maddamsetti

See Table 4 of the Obelisk paper for details of SK36 data in that paper.
I examined a couple of those datasets, and some additional SK36 monoculture datasets not in Table 4.

## I run the analysis from this directory.
cd Research/active-research/obelisk-SK36/src

##I use pysradb to look up the Run Accession ID for prefetch.

### Initial RNAseq analysis. NCBI Bioproject PRJNA270301.
pysradb metadata SRR1713039
prefetch SRR1713039 -O ../data
cd ../data
fasterq-dump --threads 10 SRR1713039
cd ../src

### Genome sequencing data for SK36
SRR14406732
https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR14406732&display=metadata
pysradb metadata SRR14406732


### I downloaded newer RNAseq data from SK36 to confirm presence of the Obelisk in additional datasets:

#### I downloaded 3 WT SK36 RNAseq replicates in glucose from:
https://www.ncbi.nlm.nih.gov/bioproject/PRJNA862079

pysradb metadata SRX16651438
prefetch SRR20627698 -O ../data
cd ../data
fasterq-dump --threads 10 SRR20627698
cd ../src

pysradb metadata SRX16651439
prefetch SRR20627697 -O ../data
cd ../data
fasterq-dump --threads 10 SRR20627697
cd ../src

pysradb metadata SRX16651440
prefetch SRR20627696 -O ../data
cd ../data
fasterq-dump --threads 10 SRR20627696
cd ../src

#### I downloaded 3 WT SK36 RNAseq replicates in ASS defined media from:
https://www.ncbi.nlm.nih.gov/bioproject/PRJNA961761
pysradb metadata SRX20097554
prefetch SRR24302371 -O ../data
cd ../data
fasterq-dump --threads 10 SRR24302371
cd ../src

pysradb metadata SRX20097555
prefetch SRR24302370 -O ../data
cd ../data
fasterq-dump --threads 10 SRR24302370
cd ../src

pysradb metadata SRX20097556
prefetch SRR24302369 -O ../data
cd ../data
fasterq-dump --threads 10 SRR24302369
cd ../src

#### I downloaded 10 WT SK36 replicates in oxic or anoxic conditions in sucrose or glucose from:
https://www.ncbi.nlm.nih.gov/bioproject/PRJNA937727

pysradb metadata SRX19476645
prefetch SRR23591557 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591557
cd ../src

pysradb metadata SRX19476647
prefetch SRR23591555 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591555
cd ../src

pysradb metadata SRX19476649
prefetch SRR23591553 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591553
cd ../src

pysradb metadata SRX19476651
prefetch SRR23591551 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591551
cd ../src

pysradb metadata SRX19476653
prefetch SRR23591549 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591549
cd ../src

pysradb metadata SRX19476655
prefetch SRR23591547 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591547
cd ../src

pysradb metadata SRX19476657
prefetch SRR23591545 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591545
cd ../src

pysradb metadata SRX19476659
prefetch SRR23591543 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591543
cd ../src

pysradb metadata SRX19476661
prefetch SRR23591541 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591541
cd ../src

pysradb metadata SRX19476663
prefetch SRR23591539 -O ../data
cd ../data
fasterq-dump --threads 10 SRR23591539
cd ../src


#### analysis of mutation effects on RNA secondary structure.

##### Description of analysis plan.

I found 3 polymorphisms in the Obelisk across RNAseq samples.

A) Position 546 R162R (CGA -> CGG) A->G mutation in Oblin-1
B) Position 194 I48I (ATC -> ATA) C->A mutation in Oblin-1
C) Position 1014 A->G mutation downstream of Oblin-1

Polymorphisms B+C have similar frequencies in all samples that have them--
they may be linked in a single haplotype.

By inspection using the FORNA web browser (http://rna.tbi.univie.ac.at/forna/forna.html),
positions 194 and 1014 do not interact in the Obelisk structure.
They are pretty far apart in the hairpin.
Indeed, an explicit check shows that the free energy for the double mutant is additive (no epistasis).

In this analysis, I use RNAfold to calculate secondary structures and changes in
minimum free energy of folding for:

1) WT + mutation A
2) WT + mutation B
3) WT + mutation C

For (1,2,3) I compare the free energy changes to all possible single mutants from WT.

##### computational protocol to analyze mutation effects on RNA secondary structure.

RNAfold is in the the ViennaRNA package, which was installed using conda:
conda install bioconda::viennarna

See RNAfold documentation here to see how to extract ensemble free energy for a given Obelisk sequence:
https://www.tbi.univie.ac.at/RNA/ViennaRNA/refman/tutorial/RNAfold.html#equilibrium-ensemble-properties

It takes about 10s to run RNAfold on one sequence on my laptop. Therefore, we need to use a job array
on the Duke Compute Cluster.

cd to the src/ directory.

$ cd src/

then generate input files for RNAfold:

$ python generate-Obelisk-mutants.py

Now run RNAfold on the WT and observed mutants:

$ ./run-RNAfold-on-Obelisk-mutants.sh

And run a job array script to run RNAfold on each input file.

$ ./submit-Obelisk-single-mutant-RNAfold-jobarray.sh

Now tabulate the ensemble free energy for each single mutant.

$ python tabulate-Obelisk-single-mutant-free-energies.py

Now compare the free energy differences for the observed mutants to the distribution
of all single-mutant free energy differences using the following R script:

$ analyze-Obelisk-single-mutant-free-energies.R

#### Mathematical model.

obelisk-abundance-model.jl is a Pluto notebook written in Julia 1.10.
This notebook can be run by installing and running Pluto.jl within Julia 1.10+ 
(see instructions at: https://plutojl.org/) and then opening the notebook using the
Pluto web browser interface. 


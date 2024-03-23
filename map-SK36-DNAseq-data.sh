#!/usr/bin/env bash
## map-SK36-DNAseq-data.sh by Rohan Maddamsetti
## I manually annotated the Oblin-1 protein on the Obelisk as saved as a genbank file
## called Obelisk_000003.gbk using Benchling.

## map to whole genome as well as the obelisk.
breseq -j 10 -p -o ../results/SK36-DNAseq-breseq-polymorphism -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR14406732.fastq.gz


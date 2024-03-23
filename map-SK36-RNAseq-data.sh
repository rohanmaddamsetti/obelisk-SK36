#!/usr/bin/env bash
## map-SK36-RNAseq-data.sh by Rohan Maddamsetti
## I manually annotated the Oblin-1 protein on the Obelisk as saved as a genbank file
## called Obelisk_000003.gbk using Benchling.

## map to whole genome as well as the obelisk, using the original RNAseq data from South Korea.
breseq -j 10 -p -o ../results/original-SK36-RNAseq-breseq-polymorphism -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR1713039.fastq

## repeat, running on all 16 new RNAseq data.
breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR20627696 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR20627696_1.fastq ../data/SRR20627696_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR20627697 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR20627697_1.fastq ../data/SRR20627697_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR20627698 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR20627698_1.fastq ../data/SRR20627698_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591539 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591539_1.fastq ../data/SRR23591539_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591541 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591541_1.fastq ../data/SRR23591541_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591543 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591543_1.fastq ../data/SRR23591543_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591545 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591545_1.fastq ../data/SRR23591545_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591547 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591547_1.fastq ../data/SRR23591547_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591549 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591549_1.fastq ../data/SRR23591549_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591551 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591551_1.fastq ../data/SRR23591551_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591553 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591553_1.fastq ../data/SRR23591553_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591555 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591555_1.fastq ../data/SRR23591555_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR23591557 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR23591557_1.fastq ../data/SRR23591557_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR24302369 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR24302369_1.fastq ../data/SRR24302369_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR24302370 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR24302370_1.fastq ../data/SRR24302370_2.fastq

breseq -j 10 -p -o ../results/SK36-RNAseq-breseq-polymorphism-SRR24302371 -r ../data/SK36-genome.gbk -r ../data/Obelisk_000003.gbk ../data/SRR24302371_1.fastq ../data/SRR24302371_2.fastq


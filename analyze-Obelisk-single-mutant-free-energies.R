## analyze-Obelisk-single-mutant-free-energies.R by Rohan Maddamsetti

## I found 3 polymorphisms in the Obelisk across RNAseq samples.

## A) Position 546 R162R (CGA -> CGG) A->G mutation in Oblin-1
## B) Position 194 I48I (ATC -> ATA) C->A mutation in Oblin-1
## C) Position 1014 A->G mutation downstream of Oblin-1

## Let's examine how the differences in energy for these three mutations compares
## to the distribution of ensemble free energy changes for all possible single mutants.

library(tidyverse)

## delta G for WT is -394.56 -- see ../results/Obelisk_WT.fold.
WT_ENSEMBLE_MFE <- -394.56

single.mutant.ensemble.mfe.data <- read.csv("../results/Obelisk-single-mutant-ensemble-free-energies.csv") %>%
    arrange(Position) %>%
    ## calculate the delta delta G from WT. 
    mutate(MFE_diff_from_WT = (EnsembleFreeEnergy - WT_ENSEMBLE_MFE))

mutA.ensemble.mfe.data <- single.mutant.ensemble.mfe.data %>%
    filter(Position == 546) %>%
    filter(MutantBase == 'G')

mutB.ensemble.mfe.data <- single.mutant.ensemble.mfe.data %>%
    filter(Position == 194) %>%
    filter(MutantBase == 'A')

mutC.ensemble.mfe.data <- single.mutant.ensemble.mfe.data %>%
    filter(Position == 1014) %>%
    filter(MutantBase == 'G')


## let's plot the distribution of ensemble MFE differences from WT.
MFE.diff.plot <- ggplot(single.mutant.ensemble.mfe.data, aes(x=MFE_diff_from_WT)) +
    geom_histogram() +
    theme_classic() +
    ## draw vertical dashed lines at the MFE_diff_from_WT for the three mutations of interest.
    ## Mutant A
    geom_vline(xintercept=mutA.ensemble.mfe.data$MFE_diff_from_WT,
               color="red", linetype="dashed") +
    ## Mutant B
    geom_vline(xintercept=mutB.ensemble.mfe.data$MFE_diff_from_WT,
               color="yellow", linetype="dashed") +
    ## Mutant C
    geom_vline(xintercept=mutC.ensemble.mfe.data$MFE_diff_from_WT,
                   color="green", linetype="dashed")
## save the plot.
## hard to draw a definitive conclusion about selection from these limited data.
ggsave("../results/MFE_diff_from_WT_distribution.pdf", MFE.diff.plot)

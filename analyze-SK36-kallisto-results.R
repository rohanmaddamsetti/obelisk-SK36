## analyze-SK36-kallisto-results.R by Rohan Maddamsetti.

library(tidyverse)

ranked.kallisto.results <- read.csv("../results/SK36_combined_kallisto_abundance.csv") %>%
group_by(RunID) %>%
    mutate(Rank = rank(desc(tpm))) %>%
    ungroup() %>%
    arrange(Rank)
write.csv(ranked.kallisto.results, "../results/SupplementaryDataFile_ranked_SK36_combined_kallisto_abundance.csv")

obelisk.rank.results <- ranked.kallisto.results %>%
    filter(SeqType == "Obelisk")
write.csv(obelisk.rank.results, "../results/Obelisk_RNA_abundance_ranks.csv")

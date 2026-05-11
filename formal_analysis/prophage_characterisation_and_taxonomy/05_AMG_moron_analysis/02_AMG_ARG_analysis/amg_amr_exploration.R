## Load libraries
library(tidyverse)

## Load db 
v_scores <- read.csv("../data/dataFixed.csv", header=TRUE)

## Load data
annotations <- read.table("../data/results/results_protein_alldbs/final/annotations-Protein_james_longum_phages_prepocessed/final_annotation_summary.tsv", header=TRUE, sep='\t', quote = "")

## Start preprocessing
annotations$virus <- sub("_CDS.*$", "", annotations$target)
length(unique(annotations$virus))  # 28878 VIRUSES
colnames(annotations)[colnames(annotations) == "best_hit"] <- "Accession"
annotations <- merge(annotations, v_scores, by="Accession", all.x=T)

# Defining viral hallmark genes
keywords_vhg <- c('portal', 'terminase', 'spike', 'capsid', 'sheath', 'tail', 'coat', 'virion', 'lysin', 'holin', 'base plate', 'baseplate', 'lysozyme', 'head', 'structural', 'phage', 'vir')
annotations$VHG <- NA

for (i in keywords_vhg){
  annotations$VHG[grep(i, annotations$product, ignore.case = TRUE)] <- 'vhg_by_keyword'
}
unique(annotations$product[!(is.na(annotations$VHG))])  # Manual check of the proteins assigned as "VHG" on a previous step
wrong_assingned <- c("Abortive infection bacteriophage resistance protein", "Lysophospholipase L1 or related esterase. Includes spore coat protein LipC/YcsK", 
                     "Uncharacterized protein RhuM, Salmonella virulence factor")

annotations$VHG[annotations$product %in% wrong_assingned] <- NA

annotations$VHG[annotations$Log10.Hit.Number. > 4 & !is.na(annotations$Log10.Hit.Number.)] <- 'vhg_by_vscore'

## AMG & other protein search
# Removing Hypothetical proteins
annotations_working <- annotations[annotations$HMM != "", ]  # removing unannotated proteins
annotations_working <- annotations_working[!(annotations_working$product %in% c("hypothetical", "Hypothetical protein", "hypothetical protein") & is.na(annotations_working$VHG)), ]  # removing hypothetical proteins
annotations_working <- annotations_working[is.na(annotations_working$VHG), ]  # removing VHGs

unique(annotations_working$product)

# Manual sort
# Do not considering genes that are known to be viral and genes that are involved in DNA interaction
potential_amgs <- c("S-adenosylmethionine synthetase", "Glycerophosphoryl diester phosphodiesterase", "Beta-galactosidase GanA", "Homoserine O-succinyltransferase", 
                    "Holo-[acyl-carrier protein] synthase", "3-oxoadipate enol-lactonase", "Fatty acid synthase, bacteria type", "phosphoadenosine phosphosulfate reductase")  # genes that are involved in metabolism as in KEGG annotations


potential_amrs <- c("Glycopeptide antibiotics resistance protein", "MFS transporter, DHA1 family, tetracycline resistance protein", "Ribosomal protection tetracycline resistance protein", 
                    "TetR/AcrR family transcriptional regulator, tetracycline repressor protein")  # genes that are involved in antibiotic resistance


potential_intersting_genes <- c("Lysophospholipase L1 or related esterase. Includes spore coat protein LipC/YcsK", "Uncharacterized protein RhuM, Salmonella virulence factor",
                                "N-acetylmuramoyl-L-alanine amidase CwlA", "SpaH/EbpB family LPXTG-anchored major pilin", "WhiB family transcriptional regulator, redox-sensing transcriptional regulator", 
                                "Reverse transcriptase", "Transcriptional regulator WhiB2", "Fic family protein", "Abortive infection bacteriophage resistance protein", "DNA-damage-inducible protein J", 
                                "toxin-antitoxin system HicB-like", "Gene 15 protein", "Putative component of the toxin-antitoxin plasmid stabilization module", "CRISPR system Cascade subunit CasE", 
                                "superinfection exclusion", "DNA methyltransferase", "HicB-like antitoxin", "DNA N-6-adenine-methyltransferase")  # genes that are interesting in any other way, or close to amrs/amgs but barely classifiable

## Adding annotations to the overall dataset
annotations$goi <- NA
annotations$goi[annotations$product %in% potential_amgs] <- "amg_potential"
annotations$goi[annotations$product %in% potential_amrs] <- "amr_potential"
annotations$goi[annotations$product %in% potential_intersting_genes] <- "interesting_potential"

## Starting boundary check
annotations <- annotations %>%
  mutate(
    protein_start = str_extract(target, "\\d+(?=\\.\\.)"),
    protein_end = str_extract(target, "(?<=\\.\\.)\\d+"),
    protein_start = as.integer(protein_start),
    protein_end = as.integer(protein_end)
  )

## Boundary check
annotations <- annotations %>%
  group_by(virus) %>%
  mutate(
    locus_start = min(protein_start[!is.na(VHG)], na.rm = TRUE),
    locus_end = max(protein_start[!is.na(VHG)], na.rm = TRUE),
    location = ifelse(
      protein_start >= locus_start & protein_start <= locus_end,
      "inside",
      NA
    )
  ) %>%
  select(-locus_start, -locus_end) %>%  # Clean up helper cols
  ungroup()

## Creating overview

annotations_of_interest <- annotations[!is.na(annotations$goi), ]
annotations_of_interest <- annotations_of_interest[c("Accession", "product", "HMM", "virus", "Protein.Function", "goi", "location")]

gene_summary <- annotations_of_interest %>%
  group_by(Accession, product, HMM, Protein.Function, goi) %>%
  summarise(
    number_of_genes_total = n(),  # count rows per group
    number_of_genes_inside_virus = sum(!is.na(location)),  # count non-NA values in col_11
    found_in_viruses = paste(virus, collapse = ",")  # list entries in col_12
  )


write.table(gene_summary, "../results/genes_of_interest_summary.tsv", sep='\t', row.names=T, col.names=T, quote=F)  # intermediate output
write.table(annotations, "../results/annotations_full.tsv", sep='\t', row.names=T, col.names=T, quote=F)  # intermediate output

# For the PAPS reductase exploration
writeLines(annotations$target[annotations$product == "phosphoadenosine phosphosulfate reductase" & !is.na(annotations$product)], "../results/PAPS_reductases.txt")

## Further exploration of the bacterial genomes: looking for genes related to sulfur assimilation (manually)

# Load data
linking_table <- read.delim("../data/genes_of_interest_with_hosts_long.tsv", header=T)
bacterial_annotations <- read.delim("../data/final_annotation_summary_bacteria_ed.tsv")
viral_annotations <- read.delim("../results/annotations_full.tsv")
viral_metadata <- read.delim("../data/003_phage_metadata_final_final.txt")

# Preprocess data
virus_bug <- viral_metadata[viral_metadata$Prophage != "", c("Prophage", "subsp_cluster", "Host_genome")]
colnames(virus_bug) <- c("virus", "subsp_cluster", "Host_genome")

amg_amr_subset <- viral_annotations[!is.na(viral_annotations$goi) & !is.na(viral_annotations$location) 
                                    & viral_annotations$goi %in% c("amg_potential", "amr_potential") & 
                                      viral_annotations$location == "inside", ]

amg_amr_subset <- merge(amg_amr_subset, virus_bug, all.x = T, by = "virus")
amg_amr_subset <- merge(amg_amr_subset, viral_metadata[], all.x = T, by = "virus")

bacterial_annotations_ed <- bacterial_annotations[!bacterial_annotations$product %in% c("hypothetical", "Hypothetical", "Uncharacterized protein"), ]

# Exploring sulfite expoxrters
PAPS <- amg_amr_subset$Host_genome[amg_amr_subset$Protein.Function == "phosphoadenosine phosphosulfate reductase"]
sulfite_expoxrter <- bacterial_annotations$genome[bacterial_annotations$product == "Sulfite exporter TauE/SafE/YfcA and related permeases, UPF0721 family"]
sum(PAPS %in% sulfite_expoxrter)
PAPS_sulfite_expoxrter <- PAPS[PAPS %in% sulfite_expoxrter]
amg_amr_subset$subsp_cluster[amg_amr_subset$Host_genome %in% PAPS_sulfite_expoxrter]
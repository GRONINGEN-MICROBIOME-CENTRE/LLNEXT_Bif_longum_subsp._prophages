## AMGs and ARGs exploration in Bifidobacterium longum subspecies ##

This document describes the workflow used to annotate and explore auxiliary metabolic genes (AMGs) and antibiotic resistance genes (ARGs) in B. longum subspecies prophages and MAGs.

The workflow includes:

1. Gene annotation of prophage-encoded proteins
2. Gene annotation of MAGs
3. Downstream analysis in R
4. Clustering of PAPS reductase sequences
5. Gene annotation of prophage proteins

1. Gene annotation of prophage-encoded proteins

---

Script: gene_annotation_viruses.sh

Input:

* .faa file with predicted protein sequences from B. longum spp. prophages
* Protein predictions were generated using Pharokka (v1.7.5) and PHOLD (v0.2.0)

Expected output:

* Annotation table for prophage-encoded proteins (including AMGs and ARGs)

2. Gene annotation of B. longum spp. MAGs

---

Script: gene_annotation_bacteria.sh

Input:

* .fna file with nucleotide sequences of the MAGs

Expected output:

* Annotation table for genes in the MAGs

3. Downstream AMGs and ARGs exploration

---

Script: amg_amr_exploration.R

Expected input:

* Output annotation tables from the virus and bacterial annotation steps

Expected output:

* Summary tables describing detected potentially interesting AMGs and ARGs

4. PAPS reductase clustering

---

Input:

* A merged .faa file containing PAPS reductase amino acid sequences:

  * PAPS reductases predicted from B. longum spp. prophages
  * PAPS reductase sequences retrieved from UniProt using the search:
    "phosphoadenosine phosphosulfate reductase" AND (taxonomy_id:2)

Required software:

* CD-HIT (v4.8.1)

Command used:
cd-hit -i PAPS_reductases.faa -o PAPS_reductases_derep_default.faa

Output:

* Dereplicated PAPS reductase sequence file (PAPS_reductases_derep_default.faa)
* CD-HIT cluster file (.clstr)

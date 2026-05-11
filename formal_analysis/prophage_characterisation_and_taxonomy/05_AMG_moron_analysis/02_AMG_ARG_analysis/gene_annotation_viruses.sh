#!/bin/bash
#SBATCH --job-name=nexus_AMG
#SBATCH --output=./job_out/nexus_protein_AMG.out
#SBATCH --error=./job_out/nexus_protein_AMG.err
#SBATCH --time=02:00:00
#SBATCH --mem=10GB
#SBATCH --cpus-per-task=10

module purge; ml Anaconda3/2022.05; conda activate metacerberus_env

cd /scratch/p309176/amg_nexus
mkdir -p ./results/results_protein_alldbs

metacerberus.py \
	--protein ./data/james_longum_phages_prepocessed.faa \
	--hmm ALL \
	--dir-out ./results/results_protein_alldbs \
	--cpus 10


conda deactivate
module purge

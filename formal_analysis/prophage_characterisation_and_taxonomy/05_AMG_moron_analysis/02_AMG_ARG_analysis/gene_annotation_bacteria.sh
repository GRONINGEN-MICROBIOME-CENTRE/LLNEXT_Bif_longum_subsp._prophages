#!/bin/bash
#SBATCH --job-name=nexus_AMG
#SBATCH --output=./job_out/nexus_protein_bacteria_%A_%a.out
#SBATCH --error=./job_out/nexus_protein_bacteria_%A_%a.err
#SBATCH --time=00:59:00
#SBATCH --mem=10GB
#SBATCH --cpus-per-task=10
#SBATCH --open-mode=truncate
#SBATCH --partition=regular

BATCH_LIST=$1
BATCH_ID=$(sed "${SLURM_ARRAY_TASK_ID}q;d" ${BATCH_LIST})

module purge; ml Anaconda3/2022.05; conda activate metacerberus_env

cd /scratch/p309176/amg_nexus
mkdir -p ./results/results_protein_bacteria/${BATCH_ID}

metacerberus.py \
	--prodigal ./data/bacterial_genomes/${BATCH_ID}.fa \
	--hmm ALL \
	--dir-out ./results/results_protein_bacteria/${BATCH_ID} \
	--cpus 10

conda deactivate
module purge

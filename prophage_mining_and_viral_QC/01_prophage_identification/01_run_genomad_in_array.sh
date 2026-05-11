# Submit geNomad analysis to the HPC cluster using a Slurm job array

#!/bin/bash
#SBATCH --job-name=genomad_array
#SBATCH --output=./logs/genomad_%A_%a.out
#SBATCH --error=./logs/genomad_%A_%a.err
#SBATCH --time=12:00:00
#SBATCH --mem=50GB
#SBATCH --cpus-per-task=8
#SBATCH --array=0-212   # Update based on number of genomes
#SBATCH --open-mode=truncate

module load Anaconda3
conda activate /conda_envs/genomad

# Read the genome name corresponding to the current array index
GENOME=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" genomad_genomes.txt)

# Run geNomad on this genome
genomad end-to-end --cleanup ${GENOME}.fa ./genomad_${GENOME} path/to/database/genomad_db_v1.9/ --threads 8

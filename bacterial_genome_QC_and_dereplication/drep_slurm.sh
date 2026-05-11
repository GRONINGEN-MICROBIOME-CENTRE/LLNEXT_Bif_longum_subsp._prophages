# Dereplicate bacterial MAGs at strain level (99.9% ANI)

#!/bin/bash
#SBATCH --job-name=drep_longum_subsp
#SBATCH --output=./drep_longum_subsp.out
#SBATCH --error=./drep_longum_subsp.err
#SBATCH --time=2-00:00:00
#SBATCH --mem=50GB
#SBATCH --cpus-per-task=16
#SBATCH --open-mode=truncate

module load dRep

dRep dereplicate ./drep_output -g ./*.fa -sa 0.999 -p 16

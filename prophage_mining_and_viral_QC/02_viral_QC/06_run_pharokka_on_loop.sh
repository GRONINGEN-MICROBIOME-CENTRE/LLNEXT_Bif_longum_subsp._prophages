#!/bin/bash
#SBATCH --job-name=pharokka_batch
#SBATCH --output=./logs/pharokka_%j.out
#SBATCH --error=./logs/pharokka_%j.err
#SBATCH --time=24:00:00
#SBATCH --mem=50GB
#SBATCH --cpus-per-task=8

module load Anaconda3
conda activate /conda_envs/Pharokka_env/

# Directory containing all your .fna files
FNA_DIR="./"

# Pharokka database path
DB="/path/to/pharokka_db/"

for fna in "${FNA_DIR}"/*.fna; do
    # skip if no .fna files present
    [[ -e "$fna" ]] || continue

    # strip .fna extension to get genome name
    genome=$(basename "$fna" .fna)

    # set output directory to pharokka_<genome>
    outdir="${FNA_DIR}/pharokka_${genome}"

    echo "===== Processing ${genome} ====="
    pharokka.py \
        -i "$fna" \
        -d "$DB" \
        --outdir "$outdir" \
        --force \
        --threads "${SLURM_CPUS_PER_TASK}"
    echo "----- Done ${genome} -----"
done

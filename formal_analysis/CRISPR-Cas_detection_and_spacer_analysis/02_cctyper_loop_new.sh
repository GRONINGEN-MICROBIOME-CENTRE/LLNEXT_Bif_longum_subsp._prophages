#!/bin/bash
#SBATCH --job-name=cctyper_array
#SBATCH --output=./cctyper_array_%A_%a.out
#SBATCH --error=./cctyper_array_%A_%a.err
#SBATCH --time=12:00:00
#SBATCH --mem=30GB
#SBATCH --cpus-per-task=8
#SBATCH --array=0-212  # Update this to match the number of .fa files
#SBATCH --open-mode=truncate

module load Anaconda3
conda activate /path/to/cctyper/env

# List all .fa files in the current directory
FA_FILES=(*.fa)

# Check array index bounds
if [ ${SLURM_ARRAY_TASK_ID} -ge ${#FA_FILES[@]} ]; then
    echo "SLURM_ARRAY_TASK_ID ${SLURM_ARRAY_TASK_ID} is out of bounds"
    exit 1
fi

# Get the .fa file and output base name
FA_FILE="${FA_FILES[$SLURM_ARRAY_TASK_ID]}"
BASE_NAME=$(basename "$FA_FILE" .fa)

# Get the parent directory name
PARENT_NAME=$(basename "$PWD")

# Create the parent-named output folder if it doesn't exist
mkdir -p "$PARENT_NAME"

# Set full output path (parent_folder/base_name)
OUTPUT_PATH="${PARENT_NAME}/${BASE_NAME}"

# Run cctyper
cctyper "$FA_FILE" "$OUTPUT_PATH" --threads 8

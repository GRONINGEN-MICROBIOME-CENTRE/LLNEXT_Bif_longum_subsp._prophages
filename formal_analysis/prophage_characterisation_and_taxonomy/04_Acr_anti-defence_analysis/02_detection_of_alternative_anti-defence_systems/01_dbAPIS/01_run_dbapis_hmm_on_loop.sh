#!/bin/bash

# dbAPIS (run on VM)

# Set the path to your dbAPIS installation
DBAPIS_PATH="/home/ubuntu/dbapis_databases"

# Set the path to your input .faa files
INPUT_DIR="/path/to/faa/files"

# Set the path to store the results
OUTPUT_DIR="/path/to/output/directory"
mkdir -p "$OUTPUT_DIR"

# Loop through all .faa files in the input directory
for file in "$INPUT_DIR"/*.faa; do
    # Extract file name without extension
    filename=$(basename -- "$file")
    filename_no_ext="${filename%.*}"

    echo "Processing $filename"

    # Step 1: Run hmmscan
    hmmscan --domtblout "$OUTPUT_DIR/hmmscan_${filename_no_ext}.out" --noali "$DBAPIS_PATH/dbAPIS.hmm" "$file"

    # Step 2: Parse annotation output (using only the HMMER results)
    bash "$DBAPIS_PATH/parse_annotation_result.sh" "$OUTPUT_DIR/hmmscan_${filename_no_ext}.out"

    echo "Finished processing $filename"
done

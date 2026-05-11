#!/bin/bash

# Set output filename
OUTPUT_FILE="all_parsed_combined.tsv"

# Clear output file if it exists
> "$OUTPUT_FILE"

# Track if header has been added
header_written=false

# Loop through all parsed TSV files
for file in hmmscan_*.out.parsed.tsv; do
    # Skip if file is empty
    if [ ! -s "$file" ]; then
        echo "Skipping empty file: $file"
        continue
    fi

    # Extract cleaned parent file name
    parent_name=$(basename "$file" | sed 's/^hmmscan_//' | sed 's/\.out\.parsed\.tsv$//')

    # If header hasn't been written, write new header with parent_file column
    if [ "$header_written" = false ]; then
        echo -e "parent_file\t$(head -n 1 "$file")" >> "$OUTPUT_FILE"
        header_written=true
    fi

    # Append the file contents with parent_file column prepended
    tail -n +2 "$file" | awk -v pf="$parent_name" -F'\t' -v OFS='\t' '{print pf, $0}' >> "$OUTPUT_FILE"
    echo "Appended: $file"
done

echo "All parsed files concatenated into: $OUTPUT_FILE"

import csv

# File paths
list_file = "List_MAG_BL_cleaned.tsv"
metadata_file = "matched_rows_metadata.tsv"
output_file = "matched_rows_metadata_with_filename.tsv"

# Step 1: Read genome ID to filename mapping
id_to_filename = {}
with open(list_file, 'r') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            genome_id, filename = parts
            id_to_filename[genome_id] = filename

# Step 2: Read metadata and add filename column
with open(metadata_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames + ['filename']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    
    writer.writeheader()
    for row in reader:
        name = row['Name']
        row['filename'] = id_to_filename.get(name, '')  # Add filename if match, else blank
        writer.writerow(row)

print(f"Finished! Output saved to {output_file}")


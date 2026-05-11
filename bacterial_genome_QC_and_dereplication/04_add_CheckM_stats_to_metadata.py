import csv

# File paths
checkm_file = "CheckM_results.txt"
metadata_file = "matched_rows_metadata_with_filename.tsv"
output_file = "metadata_with_checkm.tsv"

# Step 1: Read CheckM data into a dictionary
checkm_data = {}
with open(checkm_file, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        mag_name = row['MAG_name'].replace('.fa', '')  # Normalize by removing .fa if needed
        checkm_data[mag_name] = {
            'Completeness': row['Completeness'],
            'Contamination': row['Contamination'],
            'N50': row['N50']
        }

# Step 2: Read metadata and merge CheckM data
with open(metadata_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames + ['Completeness', 'Contamination', 'N50']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')

    writer.writeheader()
    for row in reader:
        name = row['Name']
        filename = row['filename'].replace('.fa', '')  # Normalize to match MAG_name
        checkm = checkm_data.get(filename, {'Completeness': '', 'Contamination': '', 'N50': ''})
        row.update(checkm)
        writer.writerow(row)

print(f"Merged metadata saved to: {output_file}")


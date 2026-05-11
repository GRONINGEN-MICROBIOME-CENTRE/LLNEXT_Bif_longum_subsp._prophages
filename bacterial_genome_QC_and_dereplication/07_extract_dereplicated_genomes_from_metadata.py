import csv

# File paths
derep_file = "dereplicated_genomes.txt"
metadata_file = "metadata_filtered.tsv"
output_file = "metadata_dereplicated.tsv"

# Step 1: Read dereplicated genome names into a set
with open(derep_file, 'r') as f:
    dereplicated_names = set(line.strip() for line in f if line.strip())

# Step 2: Read metadata and filter matches
with open(metadata_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile, delimiter='\t')
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter='\t')

    writer.writeheader()
    for row in reader:
        if row['Name'] in dereplicated_names:
            writer.writerow(row)

print(f"Dereplicated metadata saved to: {output_file}")

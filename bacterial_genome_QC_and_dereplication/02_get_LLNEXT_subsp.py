import csv

# File paths
genome_list_file = "genomes_list.txt"
metadata_file = "meta_clusters_subsp.tsv"
output_names_file = "matched_names.txt"
output_metadata_file = "matched_rows_metadata.tsv"

# Step 1: Read genome list
with open(genome_list_file, 'r') as f:
    genome_list = set(line.strip() for line in f if line.strip())

# Step 2: Process metadata file and filter matches
matches = []
with open(metadata_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    header = reader.fieldnames
    for row in reader:
        if row['Cohort'] == 'LLNEXT' and row['Name'] in genome_list:
            matches.append(row)

# Step 3: Write matched names to .txt file
with open(output_names_file, 'w') as f:
    for row in matches:
        f.write(row['Name'] + '\n')

# Step 4: Write matched metadata rows to .tsv file
with open(output_metadata_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=header, delimiter='\t')
    writer.writeheader()
    writer.writerows(matches)

print("Matched names and metadata written to output files.")

import csv

# File paths
sts_input_file = 'STS_subspecies_checked.tsv'
bacteria_metadata_file = 'metadata_with_Cas_and_LLNEXT.tsv'
output_file = 'STS_subspecies_filled.tsv'

# Load bacteria metadata into a dictionary
name_to_subspecies = {}

with open(bacteria_metadata_file, 'r') as metafile:
    meta_reader = csv.DictReader(metafile, delimiter='\t')
    for row in meta_reader:
        name = row['Name'].strip()
        subspecies = row['subsp_cluster'].strip()
        name_to_subspecies[name] = subspecies

# Process STS file and fill in missing Bacteria_subspecies
with open(sts_input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for row in reader:
        genome = row['Genome'].strip()
        bacteria_subspecies = row['Bacteria_subspecies'].strip()
        phage_subspecies = row['Phage_host_subspecies'].strip()

        # Fill missing Bacteria_subspecies if possible
        if not bacteria_subspecies and genome in name_to_subspecies:
            row['Bacteria_subspecies'] = name_to_subspecies[genome]
            bacteria_subspecies = name_to_subspecies[genome]

        # Update "Same" column if both subspecies are available
        if bacteria_subspecies and phage_subspecies:
            row['Same'] = 'Yes' if bacteria_subspecies == phage_subspecies else 'No'

        writer.writerow(row)

print(f"Missing Bacteria_subspecies filled. Output saved to {output_file}")

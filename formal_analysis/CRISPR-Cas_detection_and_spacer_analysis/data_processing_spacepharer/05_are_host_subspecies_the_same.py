import csv

# File paths
input_file = 'checked_STS.tsv'
metadata_file = 'metadata_with_metabolism.tsv'
output_file = 'STS_subspecies_checked.tsv'

# Load metadata into dictionaries
genome_to_subspecies = {}
phage_to_subspecies = {}

with open(metadata_file, 'r') as metafile:
    meta_reader = csv.DictReader(metafile, delimiter='\t')
    for row in meta_reader:
        host_genome = row['Host_genome'].strip()
        prophage = row['Prophage'].strip()
        subspecies = row['subsp_cluster'].strip()

        genome_to_subspecies[host_genome] = subspecies
        phage_to_subspecies[prophage] = subspecies

# Process the STS input file
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames + ['Bacteria_subspecies', 'Phage_host_subspecies', 'Same', 'No_prophage']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for row in reader:
        genome = row['Genome'].strip()
        phage = row['Phage'].lstrip('>').strip()

        bacteria_subspecies = genome_to_subspecies.get(genome, '')
        phage_subspecies = phage_to_subspecies.get(phage, '')

        # Determine if subspecies match
        if bacteria_subspecies and phage_subspecies:
            same = 'Yes' if bacteria_subspecies == phage_subspecies else 'No'
            no_prophage = ''
        else:
            same = 'No'
            no_prophage = '1'

        # Add new fields to the row
        row['Bacteria_subspecies'] = bacteria_subspecies
        row['Phage_host_subspecies'] = phage_subspecies
        row['Same'] = same
        row['No_prophage'] = no_prophage

        writer.writerow(row)

print(f"Subspecies matching complete. Output saved to {output_file}")

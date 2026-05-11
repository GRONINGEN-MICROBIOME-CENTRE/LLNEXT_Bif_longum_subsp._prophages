import csv

# File paths
input_file = 'cleaned_matches.tsv'
output_file = 'checked_STS.tsv'
sts_list_file = 'genomes_with_STS.txt'

# Dictionary to track genomes with STS
genomes_with_sts = set()

# Open files
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames + ['STS']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for row in reader:
        genome = row['Genome']
        phage_prefix = row['Phage'].lstrip(">").split('_')[0]

        if genome == phage_prefix:
            row['STS'] = '1'
            genomes_with_sts.add(genome)
        else:
            row['STS'] = '0'

        writer.writerow(row)

# Write the list of genomes with STS = 1 to a separate file
with open(sts_list_file, 'w') as txtfile:
    for genome in sorted(genomes_with_sts):
        txtfile.write(genome + '\n')

print(f"STS analysis complete. Output saved to {output_file}")
print(f"List of genomes with STS saved to {sts_list_file}")

import csv

# Input and output files
input_file = "metadata_with_checkm.tsv"
output_file = "metadata_filtered.tsv"

# Thresholds
min_completeness = 90.0
max_contamination = 5.0
min_n50 = 50000

# Read input and filter
with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile, delimiter='\t')
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter='\t')

    writer.writeheader()
    for row in reader:
        try:
            completeness = float(row['Completeness'])
            contamination = float(row['Contamination'])
            n50 = int(row['N50'])
        except ValueError:
            # Skip rows with invalid numeric data
            continue

        if (completeness >= min_completeness and
            contamination <= max_contamination and
            n50 >= min_n50):
            writer.writerow(row)

print(f"Filtered results saved to: {output_file}")

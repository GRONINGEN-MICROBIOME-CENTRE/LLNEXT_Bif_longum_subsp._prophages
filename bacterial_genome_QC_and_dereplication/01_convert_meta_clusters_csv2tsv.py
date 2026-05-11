import csv

# Define input and output file names
input_file = 'meta_clusters_subsp.csv'
output_file = 'meta_clusters_subsp.tsv'

# Open the input CSV and output TSV files
with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as tsvfile:

    # Create CSV reader and TSV writer
    csv_reader = csv.reader(csvfile)
    tsv_writer = csv.writer(tsvfile, delimiter='\t')

    # Copy rows from CSV to TSV
    for row in csv_reader:
        tsv_writer.writerow(row)

print(f"Conversion complete: '{output_file}' created.")


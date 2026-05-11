import csv

# Input and output file names
input_file = 'extracted_CRISPR_phage_matches.tsv'
output_file = 'modified_CRISPR_phage_matches.tsv'

# Function to create the new first column based on the original first column
def clean_first_column(entry):
    entry = entry.lstrip(">")  # Remove '>' if present
    return entry.split("_")[0]  # Keep only up to the first underscore

# Open the input and output files
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    tsv_reader = csv.reader(infile, delimiter='\t')
    tsv_writer = csv.writer(outfile, delimiter='\t')

    for row in tsv_reader:
        if row:  # Skip empty rows
            new_first_col = clean_first_column(row[0])
            tsv_writer.writerow([new_first_col] + row)  # Insert new column as first

print(f"Transformation complete. Results saved in {output_file}")

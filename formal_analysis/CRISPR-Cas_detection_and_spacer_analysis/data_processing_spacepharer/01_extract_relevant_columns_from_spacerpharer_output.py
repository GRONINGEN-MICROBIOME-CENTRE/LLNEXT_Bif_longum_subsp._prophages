# Open and read the file
input_file = 'CRISPR_phage_matches.tsv'
output_file = 'extracted_CRISPR_phage_matches.tsv'

# Open the input file and output file
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # Check if the line starts with '>'
        if line.startswith('>'):
            outfile.write(line)  # Write the line to the output file
            
print(f"Extraction complete. Results saved in {output_file}")

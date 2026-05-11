input_file = 'extracted_data_x100.tsv'
output_file = 'data_normalised_to_100.tsv'

# Read the input file and create a list of lines
with open(input_file, 'r') as infile:
    lines = infile.readlines()

# Process each line and update the final_result column if qname and tname are 100% match
for i in range(1, len(lines)):  # Start from 1 to skip the header line
    columns = lines[i].strip().split('\t')
    qname = columns[0]
    tname = columns[1]
    final_result = columns[2]

    if qname == tname:
        lines[i] = f"{qname}\t{tname}\t100\n"

# Write the updated data to the output file
with open(output_file, 'w') as outfile:
    outfile.writelines(lines)

print(f"Updated data written to {output_file}")

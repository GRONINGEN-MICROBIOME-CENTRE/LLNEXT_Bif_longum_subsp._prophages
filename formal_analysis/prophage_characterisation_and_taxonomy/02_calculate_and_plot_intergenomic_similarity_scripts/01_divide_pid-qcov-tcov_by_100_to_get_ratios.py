# Input file for this script is the output file from CheckV supporting code
# The purpose of this script is to divide all values by 100 to get ratio values

input_file = "my_ani_species.tsv"
output_file = "my_ani_prophage_data_ratios.tsv"

# Open the input file for reading
with open(input_file, "r") as infile:
    # Read header
    header = infile.readline().strip().split("\t")
    
    # Index of columns to be divided
    pid_index = header.index("pid")
    qcov_index = header.index("qcov")
    tcov_index = header.index("tcov")
    
    # Read and process each line
    lines = infile.readlines()
    modified_lines = []
    modified_header = header + ["pid_ratio", "qcov_ratio", "tcov_ratio"]
    for line in lines:
        fields = line.strip().split("\t")
        
        # Divide columns by 100 and add to new columns
        pid = float(fields[pid_index]) / 100
        qcov = float(fields[qcov_index]) / 100
        tcov = float(fields[tcov_index]) / 100
        
        # Append the original values to the line
        modified_line = fields + [str(pid), str(qcov), str(tcov)]
        modified_lines.append("\t".join(modified_line))

# Open the output file for writing
with open(output_file, "w") as outfile:
    # Write the modified header
    outfile.write("\t".join(modified_header) + "\n")
    
    # Write the modified lines
    outfile.writelines("\n".join(modified_lines))

print(f"File '{output_file}' created successfully.")

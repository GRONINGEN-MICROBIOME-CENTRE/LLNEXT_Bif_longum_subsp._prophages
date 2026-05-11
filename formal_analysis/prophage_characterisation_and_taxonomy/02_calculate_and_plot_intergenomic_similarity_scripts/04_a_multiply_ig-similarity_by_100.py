# Open the input file for reading
with open('extracted_final_result_ig-sim.tsv', 'r') as input_file:
    # Read the lines from the file
    lines = input_file.readlines()

# Open a new file for writing the modified data
with open('extracted_data_x100.tsv', 'w') as output_file:
    # Write the header line unchanged
    output_file.write(lines[0])

    # Iterate through the remaining lines, modify the "final_result" column, and write the modified line
    for line in lines[1:]:
        # Split the line into columns
        columns = line.strip().split('\t')

        # Multiply the value in the "final_result" column by 100
        columns[2] = str(float(columns[2]) * 100)

        # Write the modified line to the output file with proper tab separation
        output_file.write('\t'.join(columns) + '\n')

# Print a message indicating the completion of the operation
print("Script executed successfully. Check 'modified_data.tsv' for the modified data.")

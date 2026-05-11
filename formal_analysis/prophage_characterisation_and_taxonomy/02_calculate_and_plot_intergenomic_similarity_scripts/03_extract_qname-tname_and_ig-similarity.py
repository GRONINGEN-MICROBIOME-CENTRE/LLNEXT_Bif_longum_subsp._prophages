input_file = "my_ani_final_prophage_data_calculations.tsv"
output_file = "extracted_final_result_ig-sim.tsv"

# Open the input file for reading
with open(input_file, "r") as infile:
    # Read the header and find the column indices
    header = infile.readline().strip().split("\t")
    qname_index = header.index("qname")
    tname_index = header.index("tname")
    final_result_index = header.index("final_result")

    # Open the output file for writing
    with open(output_file, "w") as outfile:
        # Write the header to the output file
        outfile.write("qname\ttname\tfinal_result\n")

        # Process each line in the input file
        for line in infile:
            # Split the line into columns
            columns = line.strip().split("\t")

            # Extract the desired columns
            qname = columns[qname_index]
            tname = columns[tname_index]
            final_result = columns[final_result_index]

            # Write the extracted data to the output file
            outfile.write(f"{qname}\t{tname}\t{final_result}\n")

print(f"Extraction complete. Results written to {output_file}")

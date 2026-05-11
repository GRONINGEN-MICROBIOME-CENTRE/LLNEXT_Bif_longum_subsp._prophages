# Concatenate all virus sequence files

import os
import glob

def concatenate_fna_files(input_folder, output_file):
    """
    Concatenates all .fna files in the specified folder into a single output file.

    Parameters:
    input_folder (str): The folder containing .fna files.
    output_file (str): The output file path.
    """
    fna_files = glob.glob(os.path.join(input_folder, "*.fna"))

    if not fna_files:
        print("No .fna files found in the specified directory.")
        return

    with open(output_file, 'w') as outfile:
        for fna_file in fna_files:
            with open(fna_file, 'r') as infile:
                for line in infile:
                    outfile.write(line)
                outfile.write("\n")  # Ensure separation between concatenated sequences

    print(f"Concatenation complete! Output saved to {output_file}")

input_folder = "."  # Change this to your directory containing .fna files
output_file = "concatenated_output.fna"

concatenate_fna_files(input_folder, output_file)

import os

# Define the path to the directory containing the folders
base_directory = "./"

# Define the name of the output file for the concatenated .fa files
output_file = os.path.join(base_directory, "02_concatenated_spacers.fa")

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Loop through each folder in the base directory
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)
        
        # Check if it's a directory
        if os.path.isdir(folder_path):
            # Check if the "spacers" subfolder exists in this directory
            spacers_folder = os.path.join(folder_path, "spacers")
            if os.path.isdir(spacers_folder):
                # Loop through all files in the "spacers" folder
                for file in os.listdir(spacers_folder):
                    if file.endswith(".fa"):
                        # Get the full path to the .fa file
                        file_path = os.path.join(spacers_folder, file)
                        
                        # Open the .fa file and append its content to the output file
                        with open(file_path, 'r') as infile:
                            outfile.write(infile.read())
                            outfile.write("\n")  # Add a newline between files for clarity

print(f"Concatenated spacer files saved to: {output_file}")

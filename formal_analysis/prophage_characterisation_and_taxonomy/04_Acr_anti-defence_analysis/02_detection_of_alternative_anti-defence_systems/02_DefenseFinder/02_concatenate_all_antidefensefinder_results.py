import os
import glob

# Output file name
output_file = "01_combined_defense_finder_systems.tsv"

# Find all matching files inside folders ending with "_pharokka"
matching_files = []
for folder in os.listdir('.'):
    if folder.endswith('_pharokka') and os.path.isdir(folder):
        files = glob.glob(os.path.join(folder, '*_defense_finder_systems.tsv'))
        matching_files.extend(files)

# Sort to keep results consistent (optional)
matching_files.sort()

# Concatenate files, writing header only once
header_written = False
with open(output_file, 'w') as outfile:
    for filepath in matching_files:
        with open(filepath, 'r') as infile:
            lines = infile.readlines()
            if not lines:
                continue  # skip empty files
            if not header_written:
                outfile.write(lines[0])  # write header from first file
                header_written = True
            outfile.writelines(lines[1:])  # skip header in subsequent files

print(f"Combined {len(matching_files)} files into '{output_file}'.")

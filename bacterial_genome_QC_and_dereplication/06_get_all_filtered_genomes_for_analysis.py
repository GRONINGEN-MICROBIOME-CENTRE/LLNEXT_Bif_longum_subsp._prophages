import os
import shutil
import csv

# Paths
metadata_file = "metadata_filtered.tsv"
source_dir = "/source/to/relevant/directory/"
target_dir = os.path.join(source_dir, "filtered_genomes")

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Step 1: Read list of names from the metadata file
names_to_copy = []
with open(metadata_file, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    for row in reader:
        name = row['Name'].strip()
        names_to_copy.append(name)

# Step 2: Copy matching .fa files
copied = 0
for name in names_to_copy:
    source_file = os.path.join(source_dir, f"{name}.fa")
    target_file = os.path.join(target_dir, f"{name}.fa")
    
    if os.path.isfile(source_file):
        shutil.copy2(source_file, target_file)
        copied += 1
    else:
        print(f"File not found: {source_file}")

print(f"Done. {copied} genome files copied to '{target_dir}'")

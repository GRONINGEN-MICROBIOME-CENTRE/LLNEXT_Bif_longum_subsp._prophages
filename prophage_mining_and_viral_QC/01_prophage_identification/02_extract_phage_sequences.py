import os
import shutil
import csv

# Define the base path and output paths
base_path = "./"  # Set this to the root directory where "genomad_*" folders are
virus_output = "./phage_analysis"
summary_tsv = "genomad_file_summary.tsv"

# Ensure output directory exists
os.makedirs(virus_output, exist_ok=True)

summary_data = []

# Walk through the base directory
for root, dirs, files in os.walk(base_path):
    for dir_name in dirs:
        if dir_name.startswith("genomad_"):
            full_genomad_path = os.path.join(root, dir_name)

            # Look for subfolders ending with "_summary"
            for sub in os.listdir(full_genomad_path):
                if sub.endswith("_summary"):
                    summary_path = os.path.join(full_genomad_path, sub)

                    virus_found = 0

                    for file in os.listdir(summary_path):
                        file_path = os.path.join(summary_path, file)

                        if file.endswith("_virus.fna") and os.path.getsize(file_path) > 0:
                            shutil.copy2(file_path, os.path.join(virus_output, file))
                            virus_found = 1

                    summary_data.append([full_genomad_path, virus_found])

# Write summary TSV
with open(summary_tsv, "w", newline="") as tsv_file:
    writer = csv.writer(tsv_file, delimiter="\t")
    writer.writerow(["Parent_Directory", "phage"])
    writer.writerows(summary_data)

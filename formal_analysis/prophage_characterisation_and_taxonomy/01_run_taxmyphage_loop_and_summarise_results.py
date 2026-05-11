######## Script #1 - Run taxmyPHAGE ########

import os
import subprocess

def run_taxmyphage_per_folder():
    base_dir = os.getcwd()
    folders = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        fasta_filename = f"{folder}.fna"
        fasta_path = os.path.join(folder_path, fasta_filename)

        if not os.path.exists(fasta_path):
            print(f"⚠️  {fasta_filename} not found in {folder}, skipping.")
            continue

        os.chdir(folder_path)
        command = f"taxmyphage run -i {fasta_filename} -t 8"
        print(f"🚀 Running in {folder}: {command}")
        subprocess.run(command, shell=True)
        os.chdir(base_dir)

# Run the function
run_taxmyphage_per_folder()


######## Script #2 - Get results summary to check taxonomy ########

import os

def combine_summary_files(base_dir, output_file):
    combined_lines = []
    header_saved = False

    # Loop through each folder in the base directory
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        results_path = os.path.join(folder_path, "taxmyphage_results", "Summary_taxonomy.tsv")

        if os.path.isfile(results_path):
            with open(results_path, "r") as f:
                lines = f.readlines()

                # Save header only once
                if not header_saved:
                    combined_lines.append(lines[0].strip())
                    header_saved = True

                # Add the rest (excluding header)
                combined_lines.extend([line.strip() for line in lines[1:]])
        else:
            print(f"⚠️  Summary_taxonomy.tsv not found in {folder}/taxmyphage_results")

    # Write combined file
    with open(output_file, "w") as out:
        out.write("\n".join(combined_lines))
        out.write("\n")

    print(f"Combined file written to: {output_file}")

# Set your directory and output path here
base_directory = "./"
output_tsv = "combined_summary.tsv"

combine_summary_files(base_directory, output_tsv)

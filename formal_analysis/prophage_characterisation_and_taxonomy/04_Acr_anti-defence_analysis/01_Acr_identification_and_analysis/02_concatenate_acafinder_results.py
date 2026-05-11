import os
import glob

output_file = "All_Aca_operons_combined.tsv"
summary_file = "Aca_operon_entries_summary.tsv"
first_header = True
summary_entries = []

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Find all folders starting with 'acafinder_'
    for folder in sorted(glob.glob("acafinder_*")):
        file_path = os.path.join(folder, "All_Aca_operons.csv")
        has_entries = False  # Track if this CSV has data rows
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()
                # If file has more than just the header
                if len(lines) > 1:
                    has_entries = True
                # Write header only once, with extra column
                if first_header and lines:
                    header = lines[0].strip().split(',')
                    outfile.write('\t'.join(['Parent Directory'] + header) + '\n')
                    first_header = False
                # Write data lines, adding parent dir column
                for line in lines[1:]:
                    outfile.write('\t'.join([folder] + line.strip().split(',')) + '\n')
        # Add summary result for this folder
        summary_entries.append(f"{folder}\t{'Yes' if has_entries else 'No'}")

# Write the summary TSV
with open(summary_file, 'w', encoding='utf-8') as summary_out:
    summary_out.write("Parent Directory\tEntries Found\n")
    summary_out.write('\n'.join(summary_entries) + '\n')

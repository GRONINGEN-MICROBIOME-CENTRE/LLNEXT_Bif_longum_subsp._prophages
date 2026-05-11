import os

def rename_contigs_in_fasta(directory):
    # Loop through all .fa files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".fa") or filename.endswith(".fasta"):
            file_path = os.path.join(directory, filename)
            new_lines = []
            contig_count = 0
            base_name = os.path.splitext(filename)[0]  # Remove .fa or .fasta extension
            
            with open(file_path, 'r') as f:
                for line in f:
                    if line.startswith('>'):
                        contig_count += 1
                        new_lines.append(f'>{base_name}_{contig_count}\n')
                    else:
                        new_lines.append(line)
            
            # Write the updated content back to the file
            with open(file_path, 'w') as f:
                f.writelines(new_lines)

if __name__ == "__main__":
    directory = os.getcwd()  # Use the current working directory
    rename_contigs_in_fasta(directory)
    print("Contig renaming completed successfully.")

import os

# Directory containing the phage .fna files
phage_dir = "./"

# Process each .fna file in the directory
for filename in os.listdir(phage_dir):
    if filename.endswith("_virus.fna"):
        file_path = os.path.join(phage_dir, filename)
        
        # Extract prefix before the first underscore (e.g., "ABC123")
        sample_id = filename.split("_")[0]

        with open(file_path, "r") as f:
            lines = f.readlines()

        # Gather contigs
        contigs = []
        current_header = None
        current_seq = []

        for line in lines:
            if line.startswith(">"):
                if current_header:
                    contigs.append((current_header, "".join(current_seq)))
                current_header = line.strip()
                current_seq = []
            else:
                current_seq.append(line.strip())
        
        # Append last contig
        if current_header:
            contigs.append((current_header, "".join(current_seq)))

        # Rename headers
        renamed_lines = []
        for i, (header, seq) in enumerate(contigs):
            if len(contigs) == 1:
                new_header = f">{sample_id}"
            else:
                new_header = f">{sample_id}_{i+1}"
            renamed_lines.append(new_header)
            renamed_lines.append(seq)

        # Overwrite the file with renamed headers
        with open(file_path, "w") as f:
            f.write("\n".join(renamed_lines) + "\n")

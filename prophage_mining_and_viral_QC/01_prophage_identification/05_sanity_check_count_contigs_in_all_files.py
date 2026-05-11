# Make sure counts from newly concatenated file matches total number of viruses from geNomad output

from pathlib import Path

def count_headers_in_file(file_path):
    count = 0
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                count += 1
    return count

def main():
    directory = Path(".")  # Current directory
    virus_files = list(directory.glob("*_virus.fna"))

    # Count headers in all *_virus.fna files
    virus_count = 0
    for file in virus_files:
        virus_count += count_headers_in_file(file)

    # Count headers in concatenated_longum_phages.fna
    phage_file = directory / "concatenated_longum_phages.fna"
    phage_count = 0
    if phage_file.exists():
        phage_count = count_headers_in_file(phage_file)
    else:
        print("Warning: concatenated_longum_phages.fna not found.")

    # Print the results
    print(f"Total '>' count in *_virus.fna files: {virus_count}")
    print(f"Total '>' count in concatenated_longum_phages.fna: {phage_count}")

if __name__ == "__main__":
    main()

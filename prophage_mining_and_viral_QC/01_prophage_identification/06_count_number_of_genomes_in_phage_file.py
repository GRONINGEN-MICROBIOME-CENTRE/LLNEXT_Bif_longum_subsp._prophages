#!/usr/bin/env python3

def count_unique_genomes(fasta_file):
    unique_genomes = set()
    
    with open(fasta_file, "r") as f:
        for line in f:
            if line.startswith(">"):
                header = line[1:].strip()  # remove ">"
                genome_name = header.split("_")[0]  # take text before first "_"
                unique_genomes.add(genome_name)
    
    return len(unique_genomes), unique_genomes


if __name__ == "__main__":
    fasta_file = "concatenated_longum_phages.fna"  # change if needed
    count, genomes = count_unique_genomes(fasta_file)
    print(f"Number of unique genomes: {count}")
    print("Genomes found:")
    for g in sorted(genomes):
        print(g)


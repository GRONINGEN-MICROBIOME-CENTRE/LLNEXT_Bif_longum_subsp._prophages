# Usage example: python extract_nucleotide_sequences.py combined_filtered_phage_genomes.fasta All_Aca_operons_combined.tsv <input_Acr>.faa

#!/usr/bin/env python3

import sys
import os
from Bio import SeqIO
import pandas as pd

def extract_acrs(phage_fasta, tsv_file, input_faa, output_fasta):
    # Load genome/prophage sequences
    print(f"Loading genome sequences from: {phage_fasta}")
    phage_dict = SeqIO.to_dict(SeqIO.parse(phage_fasta, "fasta"))

    # Read the operon metadata
    print(f"Reading metadata from: {tsv_file}")
    df = pd.read_csv(tsv_file, sep="\t", dtype=str)

    # Get the list of IDs from the .faa file (these correspond to 'Parent Directory' in the TSV)
    print(f"Parsing input protein file: {input_faa}")
    faa_ids = [rec.id for rec in SeqIO.parse(input_faa, "fasta")]

    # Filter rows where Parent Directory matches an ID in the .faa
    matching_rows = df[df["Parent Directory"].isin(faa_ids)]

    # Prepare list of extracted nucleotide sequences
    records = []
    for _, row in matching_rows.iterrows():
        contig_id = row["Contig ID"]
        parent_id = row["Parent Directory"]
        start = int(row["Start"])
        end = int(row["End"])
        strand = row["Strand"]

        # Skip if contig is missing in the genome FASTA
        if contig_id not in phage_dict:
            print(f"Warning: Contig {contig_id} not found in genome file.")
            continue

        full_seq = phage_dict[contig_id].seq
        subseq = full_seq[start - 1:end]  # Adjust to 0-based indexing

        if strand == "-":
            subseq = subseq.reverse_complement()

        # Use parent directory ID as record ID
        record = SeqIO.SeqRecord(subseq, id=parent_id, description="")
        records.append(record)

    print(f"Writing {len(records)} extracted sequences to {output_fasta}")
    SeqIO.write(records, output_fasta, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: extract_acrs.py <phage_fasta> <operons_tsv> <input_faa>")
        sys.exit(1)

    phage_fasta = sys.argv[1]
    tsv_file = sys.argv[2]
    input_faa = sys.argv[3]
    output_fasta = os.path.basename(input_faa)

    extract_acrs(phage_fasta, tsv_file, input_faa, output_fasta)

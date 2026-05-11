# Usage example: python pad_out_cleaned_faa_files.py

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Define max lengths based on seqkit output
protein_max_lengths = {
    'pAcr019665': 116,
    'pAcr024125': 133,
    'pAcr028433': 103,
    'pAcr053517': 138,
    'pAcr054285': 153
}

nucleotide_max_lengths = {
    'pAcr019665': 336,
    'pAcr024125': 402,
    'pAcr028433': 312,
    'pAcr053517': 411,
    'pAcr054285': 426
}

# Loop through each Acr dataset
for acr in protein_max_lengths:
    faa_file = f"{acr}_aligned.faa"
    fasta_file = f"{acr}.fasta"
    padded_faa_out = f"padded_{faa_file}"
    padded_fasta_out = f"padded_{acr}.fasta"

    # First, collect all genome IDs from both files
    protein_ids = {record.id for record in SeqIO.parse(faa_file, "fasta")}
    nucleotide_ids = {record.id for record in SeqIO.parse(fasta_file, "fasta")}
    all_ids = protein_ids.union(nucleotide_ids)

    # Pad protein sequences
    padded_proteins = []
    for seq_id in all_ids:
        seq_record = next((r for r in SeqIO.parse(faa_file, "fasta") if r.id == seq_id), None)
        if seq_record:
            padded_seq = str(seq_record.seq).ljust(protein_max_lengths[acr], "-")
        else:
            padded_seq = "-" * protein_max_lengths[acr]
        padded_proteins.append(SeqRecord(Seq(padded_seq), id=seq_id, description=""))

    SeqIO.write(padded_proteins, padded_faa_out, "fasta")
    print(f"✅ Wrote {padded_faa_out}")

    # Pad nucleotide sequences
    padded_nucleotides = []
    for seq_id in all_ids:
        seq_record = next((r for r in SeqIO.parse(fasta_file, "fasta") if r.id == seq_id), None)
        if seq_record:
            padded_seq = str(seq_record.seq).ljust(nucleotide_max_lengths[acr], "-")
        else:
            padded_seq = "-" * nucleotide_max_lengths[acr]
        padded_nucleotides.append(SeqRecord(Seq(padded_seq), id=seq_id, description=""))

    SeqIO.write(padded_nucleotides, padded_fasta_out, "fasta")
    print(f"✅ Wrote {padded_fasta_out}")


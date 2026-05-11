# Example usage: python remove_identical_acr_sequences.py pAcr019665_codon.fasta pAcr019665_codon.nodup.fasta fasta

from Bio import AlignIO
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
import sys

def remove_duplicates(input_file, output_file, file_format="fasta", report_file="deduplication_report.txt"):
    seen = {}
    duplicates = {}
    unique_records = []

    alignment = AlignIO.read(input_file, file_format)

    for record in alignment:
        seq_str = str(record.seq)

        if seq_str not in seen:
            seen[seq_str] = record.id
            unique_records.append(record)
        else:
            if seq_str not in duplicates:
                duplicates[seq_str] = []
            duplicates[seq_str].append(record.id)

    # Write the deduplicated alignment
    new_align = MultipleSeqAlignment(unique_records)
    AlignIO.write(new_align, output_file, file_format)
    print(f"Written deduplicated alignment to: {output_file}")

    # Write the report
    with open(report_file, 'w') as report:
        for seq_str, kept_id in seen.items():
            if seq_str in duplicates:
                report.write(f"KEPT: {kept_id}\n")
                for dup_id in duplicates[seq_str]:
                    report.write(f"REMOVED: {dup_id}\n")
                report.write("\n")

    print(f"Duplicate report written to: {report_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python remove_duplicate_sequences_with_report.py input_file output_file file_format")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        file_format = sys.argv[3]
        report_file = output_file + ".duplicates.txt"
        remove_duplicates(input_file, output_file, file_format, report_file)


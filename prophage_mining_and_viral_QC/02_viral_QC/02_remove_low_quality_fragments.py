#!/usr/bin/env python3

"""
filter_checkv_quality.py

Reads a CheckV quality summary TSV and writes out only contigs >=5kb with
Medium-quality, High-quality, or Complete status.
"""
import csv
import sys

def filter_quality_summary(input_path, output_path):
    """
    Filter the CheckV quality summary.

    Keeps only rows where contig_length >= 5000 and checkv_quality is one of
    Medium-quality, High-quality, or Complete.
    """
    with open(input_path, newline='') as inf, \
         open(output_path, 'w', newline='') as outf:
        reader = csv.DictReader(inf, delimiter='\t')
        writer = csv.DictWriter(outf, fieldnames=reader.fieldnames, delimiter='\t')

        # Write header
        writer.writeheader()

        for row in reader:
            # Safely parse contig_length
            try:
                length = int(row.get('contig_length', 0))
            except ValueError:
                continue

            # Get and normalize quality
            quality = row.get('checkv_quality', '').strip()

            # Apply filters
            if length >= 5000 and quality in {'Medium-quality', 'High-quality', 'Complete'}:
                writer.writerow(row)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_tsv> <output_tsv>")
        sys.exit(1)

    input_tsv = sys.argv[1]
    output_tsv = sys.argv[2]

    filter_quality_summary(input_tsv, output_tsv)
    print(f"Filtered data written to {output_tsv}")


if __name__ == '__main__':
    main()

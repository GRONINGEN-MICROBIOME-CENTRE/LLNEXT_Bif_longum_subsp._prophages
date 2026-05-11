#!/usr/bin/env python3

"""
clean_fasta_headers.py

Reads an input FASTA file and writes a new FASTA file with headers truncated
at the first space (removes any spaces and following text).

Usage:
    python clean_fasta_headers.py input.fasta output_cleaned.fasta
"""
import sys
import argparse

def clean_headers(input_fasta: str, output_fasta: str) -> None:
    """
    Process FASTA file, stripping headers at first space and writing to output.
    """
    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                # Split at first whitespace and keep only the identifier
                header = line[1:].strip().split(None, 1)[0]
                outfile.write(f">{header}\n")
            else:
                outfile.write(line)


def main():
    parser = argparse.ArgumentParser(
        description="Clean FASTA headers by removing spaces and trailing text"
    )
    parser.add_argument(
        'input_fasta', help='Path to the input FASTA file'
    )
    parser.add_argument(
        'output_fasta', help='Path for the cleaned output FASTA file'
    )
    args = parser.parse_args()

    clean_headers(args.input_fasta, args.output_fasta)
    print(f"Cleaned FASTA written to {args.output_fasta}")

if __name__ == '__main__':
    main()

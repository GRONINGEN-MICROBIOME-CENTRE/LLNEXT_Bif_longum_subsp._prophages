#!/usr/bin/env python3

"""
split_and_extract.py

Combines the following steps into one script:
1. Split `filtered_quality_data.tsv` by provirus column into
   - `filtered_quality_data_no_provirus.tsv` (provirus = No)
   - `filtered_quality_data_just_provirus.tsv` (provirus = Yes)
2. Extract sequences:
   - From `viruses.fna` for non-provirus contigs → `matched_viruses.fna`
   - From `proviruses.fna` for provirus contigs → `matched_proviruses.fna`

Usage:
    python split_and_extract.py
"""
import csv


def split_provirus(input_tsv, no_out, yes_out):
    """
    Split the TSV by the 'provirus' column ('No' vs 'Yes').
    """
    with open(input_tsv, newline='') as inf, \
         open(no_out, 'w', newline='') as nof, \
         open(yes_out, 'w', newline='') as yf:
        reader = csv.reader(inf, delimiter='\t')
        writer_no = csv.writer(nof, delimiter='\t')
        writer_yes = csv.writer(yf, delimiter='\t')
        header = next(reader)
        writer_no.writerow(header)
        writer_yes.writerow(header)
        for row in reader:
            if len(row) < 3:
                continue
            prov = row[2].strip()
            if prov == 'No':
                writer_no.writerow(row)
            elif prov == 'Yes':
                writer_yes.writerow(row)


def read_ids(tsv_file, parse_names=False):
    """
    Read contig IDs (first column) from a TSV. If parse_names=True,
    strip any trailing '_1 ' suffix for matching provirus FASTA headers.
    """
    ids = set()
    with open(tsv_file, newline='') as inf:
        next(inf)  # skip header
        for line in inf:
            parts = line.strip().split('\t')
            if not parts:
                continue
            cid = parts[0]
            if parse_names:
                cid = cid.split('_1 ')[0]
            ids.add(cid)
    return ids


def extract_fasta(input_fasta, output_fasta, id_set, parse_names=False):
    """
    Extract FASTA records whose header (without '>') matches an ID in id_set.
    If parse_names=True, strip trailing '_1 ' before matching.
    """
    with open(input_fasta) as fin, open(output_fasta, 'w') as fout:
        write_flag = False
        for line in fin:
            if line.startswith('>'):
                raw_id = line[1:].strip()
                key = raw_id.split('_1 ')[0] if parse_names else raw_id
                write_flag = (key in id_set)
                if write_flag:
                    fout.write(line)
            else:
                if write_flag:
                    fout.write(line)


def main():
    # Input/Output file paths
    filtered_tsv             = 'filtered_quality_data.tsv'
    no_provirus_tsv          = 'filtered_quality_data_no_provirus.tsv'
    just_provirus_tsv        = 'filtered_quality_data_just_provirus.tsv'
    viruses_fna              = 'viruses.fna'
    proviruses_fna           = 'proviruses.fna'
    matched_viruses_fna      = 'matched_viruses.fna'
    matched_proviruses_fna   = 'matched_proviruses.fna'

    # Step 1: Split TSV by provirus status
    split_provirus(filtered_tsv, no_provirus_tsv, just_provirus_tsv)

    # Step 2: Read contig IDs
    no_ids  = read_ids(no_provirus_tsv,   parse_names=False)
    yes_ids = read_ids(just_provirus_tsv, parse_names=True)

    # Step 3: Extract matching FASTA records
    extract_fasta(viruses_fna, matched_viruses_fna, no_ids, parse_names=False)
    extract_fasta(proviruses_fna, matched_proviruses_fna, yes_ids, parse_names=True)

    print('Extraction complete:')
    print(f'  {no_provirus_tsv} → {matched_viruses_fna} (non-provirus)')
    print(f'  {just_provirus_tsv} → {matched_proviruses_fna} (provirus)')


if __name__ == '__main__':
    main()

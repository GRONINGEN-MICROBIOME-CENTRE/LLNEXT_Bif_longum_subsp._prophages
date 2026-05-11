#!/usr/bin/env python3

"""
Scan every *_all_cds_functions.tsv under a directory,
and for each file report whether the three structural
CDS categories (connector, head and packaging, tail)
sum to ≥3 and make up ≥20% of the total CDS count.
Also, at the end, list all files that did not meet both criteria.
Saves a text report to CDS_summary_output.txt.
Run it like: python3 check_structural_cds.py /path/to/root_dir.
"""

import os
import csv
import argparse
import sys

# Define which rows count as "structural"
STRUCTURAL_CATEGORIES = {
    "connector",
    "head and packaging",
    "tail"
}

def analyze_file(path):
    total_cds = None
    structural_sum = 0

    with open(path, newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in reader:
            desc  = row["Description"].strip().lower()
            count = int(row["Count"])
            if desc == "cds":
                total_cds = count
            elif desc in STRUCTURAL_CATEGORIES:
                structural_sum += count

    if total_cds is None:
        raise ValueError(f"No 'CDS' row found in {path!r}")

    meets_min_count = (structural_sum >= 3)
    meets_min_fraction = (structural_sum >= 0.2 * total_cds)

    return total_cds, structural_sum, meets_min_count, meets_min_fraction


def main(root_dir, output_path):
    non_compliant = []
    output_lines = []

    for dirpath, _, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith("_all_cds_functions.tsv"):
                fullpath = os.path.join(dirpath, fname)
                total, struct_sum, ok_count, ok_frac = analyze_file(fullpath)

                report = (
                    f"File: {fullpath}\n"
                    f"  Total CDS            : {total}\n"
                    f"  Structural CDS total : {struct_sum}\n"
                    f"  ≥ 3 structural?      : {'Yes' if ok_count else 'No'}\n"
                    f"  ≥ 20% of total?      : {'Yes' if ok_frac else 'No'}\n"
                )
                print(report)
                output_lines.append(report)

                if not (ok_count and ok_frac):
                    non_compliant.append(fullpath)

    if non_compliant:
        summary = "Files that did not meet criteria:\n" + "\n".join(f"  {p}" for p in non_compliant)
    else:
        summary = "All files met the criteria."

    print(summary)
    output_lines.append(summary)

    # Write everything to output file
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("\n".join(output_lines))
        out.write("\n")

    print(f"\n✅ Report saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check structural CDS proportions in TSV files and save report"
    )
    parser.add_argument(
        "directory",
        help="Root directory to recurse into"
    )
    parser.add_argument(
        "-o", "--output",
        default="CDS_summary_output.txt",
        help="Path to save the text report (default: CDS_summary_output.txt)"
    )
    args = parser.parse_args()

    main(args.directory, args.output)

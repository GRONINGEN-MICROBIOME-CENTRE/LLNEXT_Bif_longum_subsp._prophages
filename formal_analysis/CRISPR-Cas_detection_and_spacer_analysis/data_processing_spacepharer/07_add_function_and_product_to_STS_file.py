import csv
import os

# File paths
sts_input_file = 'STS_subspecies_filled.tsv'
output_file = 'STS_with_function.tsv'
phage_folder_base = '/path/to/folder/with/prophage/database/'

# Cache for loaded phage annotations
phage_annotations = {}

def load_phage_annotations(phage_name):
    folder_name = f"{phage_name}_phold"
    file_path = os.path.join(phage_folder_base, folder_name, 'phold_per_cds_predictions.tsv')

    if not os.path.isfile(file_path):
        return None

    annotations = []
    with open(file_path, 'r') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        for row in reader:
            try:
                start = int(row['start'])
                end = int(row['end'])
                function = row['function'].strip()
                product = row['product'].strip()
                annotations.append({
                    'start': min(start, end),
                    'end': max(start, end),
                    'function': function,
                    'product': product
                })
            except (KeyError, ValueError):
                continue
    # Sort annotations by start position for intergenic checks
    return sorted(annotations, key=lambda x: x['start'])

# Main processing
with open(sts_input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames + ['Phage_target_function', 'Phage_target_product', 'Match_context']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for row in reader:
        phage_name = row['Phage'].lstrip('>').strip()
        try:
            phage_start = int(row['phage_start'])
            phage_end = int(row['phage_end'])
        except ValueError:
            row['Phage_target_function'] = 'No match'
            row['Phage_target_product'] = 'No match'
            row['Match_context'] = 'Unmatched'
            writer.writerow(row)
            continue

        # Normalize input coordinates
        sts_start = min(phage_start, phage_end)
        sts_end = max(phage_start, phage_end)

        # Load annotations
        if phage_name not in phage_annotations:
            phage_annotations[phage_name] = load_phage_annotations(phage_name)

        annotations = phage_annotations[phage_name]
        best_overlap = 0
        best_function = 'No match'
        best_product = 'No match'
        match_context = 'Unmatched'

        if annotations:
            for annot in annotations:
                gene_start = annot['start']
                gene_end = annot['end']

                overlap_start = max(sts_start, gene_start)
                overlap_end = min(sts_end, gene_end)
                overlap_len = overlap_end - overlap_start + 1

                if overlap_len > best_overlap and overlap_start <= overlap_end:
                    best_overlap = overlap_len
                    best_function = annot['function']
                    best_product = annot['product']
                    match_context = 'CDS'

            if match_context == 'Unmatched':
                # Check if STS lies between any two genes
                for i in range(len(annotations) - 1):
                    end_current = annotations[i]['end']
                    start_next = annotations[i + 1]['start']
                    if end_current < sts_start and sts_end < start_next:
                        match_context = 'Intergenic'
                        break

        row['Phage_target_function'] = best_function
        row['Phage_target_product'] = best_product
        row['Match_context'] = match_context
        writer.writerow(row)

print(f"STS annotation complete with Match_context. Output saved to {output_file}")

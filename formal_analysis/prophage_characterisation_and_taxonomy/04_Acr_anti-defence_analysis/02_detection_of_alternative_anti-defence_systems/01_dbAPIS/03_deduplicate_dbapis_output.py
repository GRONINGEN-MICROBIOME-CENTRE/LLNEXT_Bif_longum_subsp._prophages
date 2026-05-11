import csv

input_file = "all_parsed_combined.tsv"
output_file = "all_parsed_combined_dereplicated.tsv"

# Dictionary to hold best rows by (parent_file, Query)
best_hits = {}

with open(input_file, newline='') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    header = reader.fieldnames

    for row in reader:
        key = (row['parent_file'], row['Query'])
        try:
            evalue = float(row['Domain c-evalue'])
        except ValueError:
            # Skip rows with bad e-values
            continue

        # If new or better (lower e-value), update
        if key not in best_hits or evalue < float(best_hits[key]['Domain c-evalue']):
            best_hits[key] = row

# Write output
with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=header, delimiter='\t')
    writer.writeheader()
    for row in best_hits.values():
        writer.writerow(row)

print(f"Dereplicated output written to: {output_file}")

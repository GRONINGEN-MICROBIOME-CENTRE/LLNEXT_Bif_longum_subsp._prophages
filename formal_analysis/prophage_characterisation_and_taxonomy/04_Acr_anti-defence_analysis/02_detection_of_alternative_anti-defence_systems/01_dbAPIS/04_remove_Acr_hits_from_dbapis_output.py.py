import csv

input_file = "all_parsed_combined_dereplicated.tsv"
output_file = "all_parsed_filtered_final.tsv"

with open(input_file, newline='') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    fieldnames = reader.fieldnames + ['Hit_final']
    rows_to_write = []

    for row in reader:
        # Skip rows with "Acr" in Hit family
        if 'Acr' in row['Hit family']:
            continue

        # Use Defense type columns to create Hit_final
        defense_type = row['Defense type'].strip()
        clan_defense_type = row['Hit CLAN defense type'].strip()

        if defense_type == clan_defense_type and defense_type:
            hit_final = defense_type
        elif defense_type and not clan_defense_type:
            hit_final = defense_type
        elif clan_defense_type and not defense_type:
            hit_final = clan_defense_type
        else:
            hit_final = ''  # ambiguous or both missing

        row['Hit_final'] = hit_final
        rows_to_write.append(row)

# Write filtered and updated output
with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(rows_to_write)

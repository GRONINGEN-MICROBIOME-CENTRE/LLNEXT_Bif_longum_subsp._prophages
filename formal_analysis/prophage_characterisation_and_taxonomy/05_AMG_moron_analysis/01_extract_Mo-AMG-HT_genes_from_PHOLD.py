import os
import csv
from collections import defaultdict, Counter

# Step 1: Load valid folder base names
with open("phages_filtered_all.txt", "r") as f:
    valid_folders = {line.strip() + "_phold" for line in f}

# Step 2: Find matching folders in current directory
all_folders = [name for name in os.listdir('.') if os.path.isdir(name)]
matched_folders = [folder for folder in all_folders if folder in valid_folders]

# Step 3: Initialize data structures
product_counter = Counter()
folder_to_products = defaultdict(list)

# Step 4: Process each matched folder
for folder in matched_folders:
    tsv_path = os.path.join(folder, "phold_per_cds_predictions.tsv")
    if not os.path.isfile(tsv_path):
        continue
    
    with open(tsv_path, newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            if row['function'].strip().lower() == "moron, auxiliary metabolic gene and host takeover":
                product = row['product'].strip()
                product_counter[product] += 1
                folder_to_products[folder].append(product)

# Step 5: Write output files

# File 1: Individual counts of each product
with open("moron_product_counts.tsv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["product", "count"])
    for product, count in product_counter.most_common():
        writer.writerow([product, count])

# File 2: Mapping from parent directory to product list
with open("folder_to_moron_products.tsv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["folder", "products"])
    for folder, products in folder_to_products.items():
        writer.writerow([folder, "; ".join(products)])

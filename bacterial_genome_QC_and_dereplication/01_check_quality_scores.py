import pandas as pd

# Load the first file
with open("file_with_CheckM_QC_scores.txt", "r") as f:
    nexus_genomes = {line.strip() for line in f}

# Load the second file (CheckM_results.txt)
df = pd.read_csv("CheckM_results.txt", sep="\t")

# Filter for the required conditions
filtered_df = df[
    (df["Completeness"] >= 90) &
    (df["Contamination"] <= 5) &
    (df["N50"] >= 50000)
]

# Find matching MAG names for both passed and failed genomes
matching_genomes = filtered_df[filtered_df["MAG_name"].isin(nexus_genomes)]
failed_genomes = df[df["MAG_name"].isin(nexus_genomes) & ~df.index.isin(filtered_df.index)]

# Save filtered results
matching_genomes.to_csv("filtered_genomes.txt", sep="\t", index=False)
failed_genomes.to_csv("failed_genomes.txt", sep="\t", index=False)

# Save just the list of genome names that met the criteria
matching_genomes["MAG_name"].to_csv("filtered_genome_names.txt", sep="\t", index=False, header=False)

# Display results
print("Filtered results saved to 'filtered_genomes.txt'")
print("Failed genomes saved to 'failed_genomes.txt'")
print("Filtered genome names saved to 'filtered_genome_names.txt'")


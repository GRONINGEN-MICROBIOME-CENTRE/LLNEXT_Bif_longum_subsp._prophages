import pandas as pd

# Define the target Acrs
target_acrs = {
    "pAcr019665",
    "pAcr024125",
    "pAcr028433",
    "pAcr053517",
    "pAcr054285"
}

# Load the TSV file
input_file = "All_Aca_operons_combined.tsv"
df = pd.read_csv(input_file, sep="\t", dtype=str)

# Drop rows without an Acr Homolog
df = df.dropna(subset=["Acr Homolog"])

# Filter for rows where Acr Homolog is in the target list
filtered_df = df[df["Acr Homolog"].isin(target_acrs)]

# Group by Acr and write individual .faa files
for acr, group in filtered_df.groupby("Acr Homolog"):
    with open(f"{acr}.faa", "w") as faa_file:
        for _, row in group.iterrows():
            header = f">{row['Parent Directory']}"
            # Remove '*' characters from the protein sequence
            sequence = row["Protein Sequence"].replace("*", "")
            faa_file.write(f"{header}\n{sequence}\n")

print("FASTA files created with '*' removed from sequences.")

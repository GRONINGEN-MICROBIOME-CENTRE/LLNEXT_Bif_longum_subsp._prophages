#!/usr/bin/env python3
import pandas as pd

# 1. Read the input TSVs
sts_df = pd.read_csv("STS_with_function.tsv", sep="\t", dtype=str)
crispr_df = pd.read_csv("concatenated_crisprs_all_cctyper.tsv", sep="\t", dtype=str)

# 2. Normalize Spacer IDs in the STS file
#    Remove leading '>' and drop everything from ':' onward
sts_df['Spacer_id'] = (
    sts_df['Spacer']
    .str.lstrip('>')
    .str.split(':', n=1, expand=True)[0]
)

# 3. Prepare the cctyper table for merging
#    We only need parent_folder, CRISPR, and Subtype
crispr_sub = crispr_df[['parent_folder', 'CRISPR', 'Subtype']].copy()

# 4. Merge on Genome↔parent_folder AND Spacer_id↔CRISPR
merged = pd.merge(
    sts_df,
    crispr_sub,
    how='left',
    left_on=['Genome', 'Spacer_id'],
    right_on=['parent_folder', 'CRISPR']
)

# 5. Rename the imported Subtype column and drop intermediate cols
merged = merged.rename(columns={'Subtype': 'CRISPR_subtype'})
merged = merged.drop(columns=['Spacer_id', 'parent_folder', 'CRISPR'])

# 6. Write out the augmented STS table
merged.to_csv("STS_with_function.with_subtype.tsv", sep="\t", index=False)

print("Done — output written to STS_with_function.with_subtype.tsv")

import pandas as pd

# Read the TSV file into a DataFrame
df = pd.read_csv('my_ani_prophage_data_ratios.tsv', sep='\t')

# Perform the calculations
df['pid_tcov_multiply'] = df['pid_ratio'] * df['tcov_ratio']
df['pid_qcov_multiply'] = df['pid_ratio'] * df['qcov_ratio']

# Add the answers of the multiplications and divide by 2
df['final_result'] = (df['pid_tcov_multiply'] + df['pid_qcov_multiply']) / 2

# Save the modified DataFrame back to a TSV file
df.to_csv('03_my_ani_final_prophage_data_calculations.tsv', sep='\t', index=False)

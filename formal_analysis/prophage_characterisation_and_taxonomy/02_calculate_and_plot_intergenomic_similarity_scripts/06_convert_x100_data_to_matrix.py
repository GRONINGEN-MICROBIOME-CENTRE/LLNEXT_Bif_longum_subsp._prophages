import pandas as pd

# Read the TSV file into a DataFrame
df = pd.read_csv('data_normalised_to_100.tsv', sep='\t')

# Create a pivot table to convert the data into a matrix
matrix_df = df.pivot(index='qname', columns='tname', values='final_result')

# Fill NaN values with 0 if necessary
matrix_df = matrix_df.fillna(0)

# Print or save the resulting matrix DataFrame
print(matrix_df)

# If you want to save the matrix to a new file
matrix_df.to_csv('completed_ani_matrix.csv', index=True)

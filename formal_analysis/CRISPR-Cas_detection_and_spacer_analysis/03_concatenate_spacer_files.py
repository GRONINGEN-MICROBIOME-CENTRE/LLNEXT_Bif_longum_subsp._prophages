import os
import pandas as pd

# Define the path to the directory containing the folders
base_directory = "./"

# Initialize an empty list to hold the data
dataframes = []

# Loop through each folder in the base directory
for folder in os.listdir(base_directory):
    folder_path = os.path.join(base_directory, folder)
    
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Check for crisprs_all.tab in the directory
        file_path = os.path.join(folder_path, 'crisprs_all.tab')
        if os.path.exists(file_path):
            # Read the file into a dataframe
            df = pd.read_csv(file_path, sep="\t")
            
            # Add the parent folder column
            df['parent_folder'] = folder
            
            # Append to the list of dataframes
            dataframes.append(df)

# Concatenate all dataframes and remove duplicate headers
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the concatenated file to a new .tab file
    output_file = os.path.join(base_directory, '01_concatenated_crisprs_all.tsv')
    combined_df.to_csv(output_file, sep="\t", index=False)

    print(f"Concatenated file saved to: {output_file}")
else:
    print("No files found.")

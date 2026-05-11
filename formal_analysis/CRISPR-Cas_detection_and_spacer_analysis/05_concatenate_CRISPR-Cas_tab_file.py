import os
import pandas as pd

def concatenate_crispr_files(root_dir, output_file='combined_CRISPR_Cas.tsv'):
    all_data = []
    for foldername, subfolders, filenames in os.walk(root_dir):
        if 'CRISPR_Cas.tab' in filenames:
            file_path = os.path.join(foldername, 'CRISPR_Cas.tab')
            try:
                df = pd.read_csv(file_path, sep='\t')
                df['Parent_Directory'] = os.path.basename(foldername)
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv(output_file, sep='\t', index=False)
        print(f"Combined file saved to: {output_file}")
    else:
        print("No CRISPR_Cas.tab files found.")

# Example usage
concatenate_crispr_files('.')
